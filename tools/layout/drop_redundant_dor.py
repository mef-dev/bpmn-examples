"""Прибирає елемент даних, який лише повторює тип межі процесу.

Кінцева і початкова події вже несуть свій DOR — саме з них рушій виводить
типізовану межу. Gateway типу не змінює, він лише розводить токен. Тому DOR,
почеплений на задачу перед кінцем (через самі лише гейтвеї), нічого не додає:
на схемі це другий такий самий аркуш поруч, який читач мусить порівнювати з
першим, щоб зрозуміти, що це одне й те саме.

Те саме дзеркально на вході: задача одразу після старту не має переоголошувати
вхідний тип.

Прибирається сам dataObjectReference, його dataObject, асоціація на задачі та
їхнє зображення — фігура, ребро й підпис.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


def local(tag):
    return tag.split("}", 1)[-1]


GATEWAYS = ("exclusiveGateway", "parallelGateway", "inclusiveGateway",
            "eventBasedGateway", "complexGateway")
TASKS = ("task", "serviceTask", "scriptTask", "businessRuleTask", "userTask",
         "manualTask", "sendTask", "receiveTask", "callActivity", "subProcess")

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
root = ET.fromstring(text)

kind, dor_type = {}, {}
for el in root.iter():
    name = local(el.tag)
    if el.get("id"):
        kind[el.get("id")] = name
    if name == "dataObjectReference":
        dor_type[el.get("id")] = (el.get("name") or "").strip()

out_flows, in_flows = {}, {}
for el in root.iter():
    if local(el.tag) == "sequenceFlow":
        out_flows.setdefault(el.get("sourceRef"), []).append(el.get("targetRef"))
        in_flows.setdefault(el.get("targetRef"), []).append(el.get("sourceRef"))

# який тип оголошено на межі
boundary_type = {}
for el in root.iter():
    if local(el.tag) not in ("endEvent", "startEvent"):
        continue
    for child in el.iter():
        tag = local(child.tag)
        if tag == "dataInputAssociation":
            src = (child.findtext("{*}sourceRef") or "").strip()
            boundary_type[el.get("id")] = dor_type.get(src, "")
        elif tag == "dataOutputAssociation":
            dst = (child.findtext("{*}targetRef") or "").strip()
            boundary_type[el.get("id")] = dor_type.get(dst, "")


def reachable_boundary(node, forward):
    """Куди веде шлях, якщо дорогою трапляються самі лише гейтвеї."""
    edges = out_flows if forward else in_flows
    seen, stack, found = set(), list(edges.get(node, [])), []
    while stack:
        nid = stack.pop()
        if nid in seen:
            continue
        seen.add(nid)
        if kind.get(nid) in GATEWAYS:
            stack.extend(edges.get(nid, []))
        elif kind.get(nid) in ("endEvent", "startEvent"):
            found.append(nid)
        else:
            return []          # дорогою є ще робота — тип міг змінитися
    return found


doomed = []
for el in root.iter():
    if local(el.tag) not in TASKS:
        continue
    task = el.get("id")
    for child in list(el):
        tag = local(child.tag)
        if tag == "dataOutputAssociation":
            ref = (child.findtext("{*}targetRef") or "").strip()
            ends = reachable_boundary(task, forward=True)
        elif tag == "dataInputAssociation":
            ref = (child.findtext("{*}sourceRef") or "").strip()
            ends = reachable_boundary(task, forward=False)
        else:
            continue
        if not ends:
            continue
        mine = dor_type.get(ref)
        if mine and all(boundary_type.get(e) == mine for e in ends):
            doomed.append((task, child.get("id"), ref, mine, ends))

removed = []
for task, assoc, ref, typename, ends in doomed:
    obj = None
    m = re.search(rf'<dataObjectReference id="{ref}"[^>]*dataObjectRef="([^"]+)"', text)
    if m:
        obj = m.group(1)
    text = re.sub(rf'\s*<data(?:Input|Output)Association id="{assoc}">.*?'
                  r"</data(?:Input|Output)Association>", lambda m: "", text, flags=re.S)
    text = re.sub(rf'\s*<dataObjectReference id="{ref}"[^>]*/>', lambda m: "", text)
    if obj:
        text = re.sub(rf'\s*<dataObject id="{obj}" ?/>', lambda m: "", text)
    text = re.sub(rf'\s*<bpmndi:BPMNShape id="[^"]*" bpmnElement="{ref}".*?'
                  r"</bpmndi:BPMNShape>", lambda m: "", text, flags=re.S)
    text = re.sub(rf'\s*<bpmndi:BPMNShape id="[^"]*" bpmnElement="{ref}"[^>]*/>',
                  lambda m: "", text)
    text = re.sub(rf'\s*<bpmndi:BPMNEdge id="[^"]*" bpmnElement="{assoc}">.*?'
                  r"</bpmndi:BPMNEdge>", lambda m: "", text, flags=re.S)
    removed.append(f"{ref} ({typename}) біля {task} → "
                   + ", ".join(ends))

path.write_bytes(text.encode("utf-8"))
for item in removed:
    print("  прибрано:", item)
print(f"зайвих елементів даних прибрано: {len(removed)}")
