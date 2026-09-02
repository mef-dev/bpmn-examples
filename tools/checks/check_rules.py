"""Перевіряє модель за сімома правилами верстки й читабельності."""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


def local(tag):
    return tag.split("}", 1)[-1]


def segments(points):
    return list(zip(points, points[1:]))


def crosses(s1, s2):
    def orient(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return (v > 1e-9) - (v < -1e-9)

    (p1, p2), (p3, p4) = s1, s2
    if len({p1, p2, p3, p4}) < 4:
        return False
    d1, d2 = orient(p3, p4, p1), orient(p3, p4, p2)
    d3, d4 = orient(p1, p2, p3), orient(p1, p2, p4)
    return d1 != d2 and d3 != d4


path = pathlib.Path(sys.argv[1])
raw = path.read_text(encoding="utf-8")
root = ET.fromstring(raw)

nodes, ends, gateways, tasks = {}, [], [], []
assoc_ids, annotations = [], []
for el in root.iter():
    name = local(el.tag)
    if el.get("id"):
        nodes[el.get("id")] = name
    if name == "endEvent":
        ends.append(el)
    elif name == "exclusiveGateway":
        gateways.append(el)
    elif name in ("task", "serviceTask", "scriptTask", "userTask",
                  "sendTask", "receiveTask", "businessRuleTask",
                  "manualTask", "callActivity"):
        tasks.append(el)
    elif name == "textAnnotation":
        annotations.append(el)
    elif name in ("dataInputAssociation", "dataOutputAssociation"):
        assoc_ids.append(el.get("id"))

edges = {}
for el in root.iter():
    if local(el.tag) != "BPMNEdge":
        continue
    pts = [(float(w.get("x")), float(w.get("y"))) for w in el
           if local(w.tag) == "waypoint"]
    edges[el.get("bpmnElement")] = pts

print(f"# {path.name}\n")

# 1 — кількість кінцевих подій
codes = []
for e in ends:
    route = e.find(".//{*}elementParameter[@name='EndSignalRoute']")
    codes.append(route.text if route is not None else "200 (типовий)")
print(f"1. EndEvent: {len(ends)}")
for e, c in zip(ends, codes):
    print(f"      {e.get('id'):<22} {c}")
print("   " + ("ОК — по одному на тип виходу" if len(set(codes)) == len(ends)
               else f"ПОРУШЕНО — однакових виходів {len(ends) - len(set(codes))}"))

# 2 — старт і кінець привʼязані стрілкою
missing = [a for a in assoc_ids if a not in edges]
print(f"\n2. Асоціацій даних: {len(assoc_ids)}, без BPMNEdge: {len(missing)}")
print("   " + ("ОК" if not missing else "ПОРУШЕНО: " + ", ".join(missing)))

# 3 — default path на кожному exclusive gateway
bad = [g.get("id") for g in gateways
       if len(g.findall("{*}outgoing")) > 1 and not g.get("default")]
print(f"\n3. Exclusive gateway: {len(gateways)}, без default: {len(bad)}")
print("   " + ("ОК" if not bad else "ПОРУШЕНО: " + ", ".join(bad)))

# 4 — перетини стрілок
pairs, items = 0, list(edges.items())
for i, (na, pa) in enumerate(items):
    for nb, pb in items[i + 1:]:
        if any(crosses(s1, s2) for s1 in segments(pa) for s2 in segments(pb)):
            pairs += 1
            print(f"      перетин: {na} ↔ {nb}")
print(f"\n4. Перетинів стрілок: {pairs}")
print("   " + ("ОК" if pairs == 0 else "ПОРУШЕНО"))

# 5 — оголошені типи привʼязані до задач
declared = set()
m = re.search(r'name="InnerTypes"[^>]*>(.*?)</gp:globalParameter>', raw, re.S)
if m:
    try:
        declared = {t["name"] for t in json.loads(
            m.group(1).replace("&quot;", '"').replace("&amp;", "&")
            .replace("&lt;", "<").replace("&gt;", ">"))}
    except Exception:  # noqa: BLE001
        declared = set(re.findall(r'"name":\s*"([A-Za-z_][A-Za-z0-9_]*)"', m.group(1)))
attached = {el.get("name") for el in root.iter()
            if local(el.tag) == "dataObjectReference"}
# Задача, суміжна зі стартом чи кінцем, елемента даних не потребує: він уже
# стоїть на самій події.
flows = [(f.get("sourceRef"), f.get("targetRef")) for f in root.iter()
         if local(f.tag) == "sequenceFlow"]
event_ids = {i for i, k in nodes.items() if k in ("startEvent", "endEvent")}
adjacent = {a for a, b in flows if b in event_ids} | {b for a, b in flows
                                                      if a in event_ids}

unattached = []
for t in tasks:
    impl = t.find(".//{*}elementParameter[@name='ElementImplementation']")
    body = impl.text if impl is not None else ""
    used = {d for d in declared if d and re.search(rf"\b{re.escape(d)}\b", body or "")}
    linked = bool(t.findall("{*}dataInputAssociation")
                  or t.findall("{*}dataOutputAssociation"))
    if used and not linked and t.get("id") not in adjacent:
        unattached.append(f"{t.get('id')} -> {', '.join(sorted(used))}")

# один елемент даних — одна стрілка
targets = [a.findtext("{*}targetRef") or a.findtext("{*}sourceRef")
           for a in root.iter() if local(a.tag) in
           ("dataInputAssociation", "dataOutputAssociation")]
overloaded = {t for t in targets if t and targets.count(t) > 1}
print(f"\n5. Задач, що вживають оголошений тип без привʼязки: {len(unattached)}")
for u in unattached:
    print(f"      {u}")
print("   " + ("ОК" if not unattached else "ПОРУШЕНО"))
print(f"   елементи даних на схемі: {', '.join(sorted(x for x in attached if x))}")
print(f"   елементів даних із кількома стрілками: {len(overloaded)}"
      + (" — " + ", ".join(sorted(overloaded)) if overloaded else ""))

# Прапорець набору й дужки в імені мають казати те саме.
refs = {el.get("dataObjectRef"): (el.get("name") or "")
        for el in root.iter() if local(el.tag) == "dataObjectReference"}
mismatch = []
for el in root.iter():
    if local(el.tag) != "dataObject":
        continue
    flag = (el.get("isCollection") or "false").lower() == "true"
    named = refs.get(el.get("id"), "").strip().endswith("[]")
    if flag != named:
        mismatch.append(f"{el.get('id')} ({refs.get(el.get('id'), '?')}): "
                        f"isCollection={flag}, імʼя з дужками={named}")
print(f"\n10. Незгода прапорця набору й імені: {len(mismatch)}")
for item in mismatch:
    print(f"      {item}")
print("   " + ("ОК" if not mismatch else "ПОРУШЕНО"))

unnamed = [t.get("id") for t in tasks if not (t.get("name") or "").strip()]
print(f"\n8. Задач без імені: {len(unnamed)}"
      + ("" if not unnamed else " — " + ", ".join(unnamed)))
print("   " + ("ОК" if not unnamed else "ПОРУШЕНО"))

# Серед ЗАДАЧ рушій виконує лише task і serviceTask. scriptTask,
# businessRuleTask, userTask, manualTask, sendTask і receiveTask компілюються
# без жодного попередження і мовчки пропускаються: токен іде далі зі старим
# результатом. Доведено на стенді перебором усіх видів задач.
#
# callActivity — не задача, а виклик іншого Flow; він виконується (на ньому
# тримається 01-basics/first-flow). subProcess у цьому наборі не перевірявся,
# тож у список не вписаний і сюди не потрапляє.
RUNNABLE = ("task", "serviceTask", "callActivity")
dead = [f"{t.get('id')} ({local(t.tag)})" for t in tasks
        if local(t.tag) not in RUNNABLE]
noisy = [i for i in nodes if i.startswith(("Activity_", "Gateway_1", "Event_0"))]
print(f"\n9. Задач, які рушій не виконає: {len(dead)}"
      + ("" if not dead else " — " + ", ".join(dead)))
print(f"   службових ідентифікаторів: {len(noisy)}"
      + ("" if not noisy else " — " + ", ".join(sorted(noisy)[:6])))
print("   " + ("ОК" if not dead and not noisy else "ПОРУШЕНО"))

# 6 і 7 — коментарі
print(f"\n6. textAnnotation у моделі: {len(annotations)}")
print("   " + ("ОК" if annotations else "ПОРУШЕНО — рішення не прокоментовані"))
has_input_example = any("{" in (a.findtext("{*}text") or "") for a in annotations)
print(f"\n7. Приклад входу в коментарі: {'є' if has_input_example else 'немає'}")
print("   " + ("ОК" if has_input_example else "ПОРУШЕНО"))

# 11 — межа процесу вже оголошує тип, а gateway його не змінює: другий такий
# самий аркуш поруч із задачею нічого не додає, лише змушує звіряти два.
from rule_redundant_dor import redundant_data_objects  # noqa: E402

extra = redundant_data_objects(root)
print(f"\n11. Елементів даних, що повторюють тип межі: {len(extra)}")
for item in extra:
    print(f"      {item}")
print("   " + ("ОК" if not extra else "ПОРУШЕНО"))
