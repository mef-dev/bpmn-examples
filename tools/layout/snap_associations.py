"""Прив'язує лінії асоціацій до середини найближчої сторони елемента.

Лінія, що впирається в кут або в довільну точку всередині фігури, читається
як недбалість. Обидва кінці асоціації сідають на середину тієї сторони, яка
ближча до співрозмовника.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


def local(tag):
    return tag.split("}", 1)[-1]


def sides(box):
    x, y, w, h = box
    return {
        "top": (x + w / 2, y),
        "bottom": (x + w / 2, y + h),
        "left": (x, y + h / 2),
        "right": (x + w, y + h / 2),
    }


def nearest(box, toward, skip=()):
    """Найближча середина сторони. Низ елемента даних не беремо: там підпис."""
    options = {k: v for k, v in sides(box).items() if k not in skip}
    return min(options.values(),
               key=lambda p: (p[0] - toward[0]) ** 2 + (p[1] - toward[1]) ** 2)


def crosses(p1, p2, q1, q2):
    """Чи перетинаються два відрізки. Спільний кінець перетином не рахуємо."""
    def side(a, b, c):
        return ((b[0] - a[0]) * (c[1] - a[1])
                - (b[1] - a[1]) * (c[0] - a[0]))

    if p1 in (q1, q2) or p2 in (q1, q2):
        return False
    d1, d2 = side(q1, q2, p1), side(q1, q2, p2)
    d3, d4 = side(p1, p2, q1), side(p1, p2, q2)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def hits_of(route, obstacles):
    segments = list(zip(route, route[1:]))
    return sum(1 for p1, p2 in segments
               for q1, q2 in obstacles if crosses(p1, p2, q1, q2))


def best_route(a, b, skip_a, skip_b, obstacles):
    """Маршрут асоціації, що перетинає найменше чужих ліній.

    Спершу пряма між серединами сторін. Якщо жодна пара сторін не проходить
    чисто, пробується Г-подібний обхід через кут: краще одна ламана, ніж лінія
    поверх чужої стрілки.
    """
    from_a = [v for k, v in sides(a).items() if k not in skip_a]
    from_b = [v for k, v in sides(b).items() if k not in skip_b]
    def crookedness(route):
        """Скільки відрізків ідуть навскіс. Рівна лінія читається краще."""
        return sum(1 for (x1, y1), (x2, y2) in zip(route, route[1:])
                   if x1 != x2 and y1 != y2)

    scored = []
    for start in from_a:
        for end in from_b:
            length = (start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2
            candidates = [[start, end]]
            for corner in ((start[0], end[1]), (end[0], start[1])):
                if corner not in (start, end):
                    candidates.append([start, corner, end])
            for route in candidates:
                scored.append((hits_of(route, obstacles), crookedness(route),
                               length, route))
    return min(scored)[3]


def centre(box):
    x, y, w, h = box
    return (x + w / 2, y + h / 2)


path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
root = ET.fromstring(text)

bounds = {}
for el in root.iter():
    if local(el.tag) == "BPMNShape":
        b = el[0]
        bounds[el.get("bpmnElement")] = (
            float(b.get("x")), float(b.get("y")),
            float(b.get("width")), float(b.get("height")))

# У асоціації даних один кінець не оголошується: ним є сам вузол-власник.
# Без цього ребро не перераховується й лишається висіти в порожнечі.
owner_of = {}
for node in root.iter():
    for child in list(node):
        if local(child.tag) in ("dataInputAssociation", "dataOutputAssociation"):
            owner_of[child.get("id")] = node.get("id")

links = {}
for el in root.iter():
    kind = local(el.tag)
    if kind not in ("association", "dataInputAssociation",
                    "dataOutputAssociation"):
        continue
    eid = el.get("id")
    src = el.get("sourceRef") or el.findtext("{*}sourceRef")
    dst = el.get("targetRef") or el.findtext("{*}targetRef")
    if kind == "dataInputAssociation":
        dst = owner_of.get(eid)            # ціль — вузол, що споживає дані
    elif kind == "dataOutputAssociation":
        src = owner_of.get(eid)            # джерело — вузол, що дані віддає
    if src and dst:
        links[eid] = (src.strip(), dst.strip(), kind)

# Розташування коментарів веде place_notes.py; тут лише кінці ліній.
placed = 0

# Перешкоди, які асоціація не має перетинати, коли є вибір: чужі лінії і
# підписи. Підпис стоїть за правилом і не рухається — обходить лінія.
obstacles = []
for el in root.iter():
    if local(el.tag) == "BPMNEdge":
        pts = [(float(w.get("x")), float(w.get("y"))) for w in el
               if local(w.tag) == "waypoint"]
        obstacles.extend(zip(pts, pts[1:]))
    elif local(el.tag) == "BPMNLabel" and len(el):
        b = el[0]
        x, y = float(b.get("x")), float(b.get("y"))
        w, h = float(b.get("width")), float(b.get("height"))
        corners = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        obstacles.extend(zip(corners, corners[1:] + corners[:1]))

fixed = 0
added = 0
# Спершу асоціації даних, потім лінії коментарів: дані — частина контракту,
# і поступатися дорогою має пояснення, а не воно.
ordered = sorted(links.items(), key=lambda kv: kv[1][2] == "association")

for eid, (src, dst, _kind) in ordered:
    if src not in bounds or dst not in bounds:
        continue
    a, b = bounds[src], bounds[dst]
    data_kinds = ("dataObjectReference", "dataStoreReference",
                  "dataInput", "dataOutput")
    kind_of = lambda n: next((local(e.tag) for e in root.iter()
                              if e.get("id") == n), "")
    skip_a = ("bottom",) if kind_of(src) in data_kinds else ()
    skip_b = ("bottom",) if kind_of(dst) in data_kinds else ()
    route = best_route(a, b, skip_a, skip_b, obstacles)
    # Прокладене стає перешкодою для наступного: інакше дві асоціації з одного
    # елемента даних розходяться навхрест, кожна оминаючи лише чужі лінії.
    obstacles.extend(zip(route, route[1:]))
    body = "".join(f'\n        <di:waypoint x="{x:.0f}" y="{y:.0f}" />'
                   for x, y in route)
    new_text, count = re.subn(
        rf'(<bpmndi:BPMNEdge id="[^"]*" bpmnElement="{eid}">).*?(</bpmndi:BPMNEdge>)',
        lambda m, s=body: m.group(1) + s + "\n      " + m.group(2),
        text, flags=re.S)
    if count:
        text = new_text
        fixed += 1
        continue

    # Оголошена асоціація без ребра — це елемент даних, що висить на схемі
    # сам по собі: читач не бачить, що його породжує. Малюємо.
    edge = (f'\n      <bpmndi:BPMNEdge id="Ed_{eid}" bpmnElement="{eid}">'
            + body + "\n      </bpmndi:BPMNEdge>")
    text, count = re.subn(r"(\s*</bpmndi:BPMNPlane>)",
                          lambda m, s=edge: s + m.group(1), text, count=1)
    added += bool(count)

path.write_bytes(text.encode("utf-8"))
print(f"асоціацій прив'язано: {fixed};  ребер домальовано: {added}")
