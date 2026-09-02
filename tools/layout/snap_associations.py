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
        links[eid] = (src.strip(), dst.strip())

# Розташування коментарів веде place_notes.py; тут лише кінці ліній.
placed = 0

fixed = 0
for eid, (src, dst) in links.items():
    if src not in bounds or dst not in bounds:
        continue
    a, b = bounds[src], bounds[dst]
    data_kinds = ("dataObjectReference", "dataStoreReference",
                  "dataInput", "dataOutput")
    kind_of = lambda n: next((local(e.tag) for e in root.iter()
                              if e.get("id") == n), "")
    skip_a = ("bottom",) if kind_of(src) in data_kinds else ()
    skip_b = ("bottom",) if kind_of(dst) in data_kinds else ()
    start = nearest(a, centre(b), skip_a)
    end = nearest(b, centre(a), skip_b)
    body = (f'\n        <di:waypoint x="{start[0]:.0f}" y="{start[1]:.0f}" />'
            f'\n        <di:waypoint x="{end[0]:.0f}" y="{end[1]:.0f}" />')
    new_text, count = re.subn(
        rf'(<bpmndi:BPMNEdge id="[^"]*" bpmnElement="{eid}">).*?(</bpmndi:BPMNEdge>)',
        lambda m, s=body: m.group(1) + s + "\n      " + m.group(2),
        text, flags=re.S)
    if count:
        text = new_text
        fixed += 1

path.write_bytes(text.encode("utf-8"))
print(f"коментарів вирівняно: {placed};  асоціацій прив'язано: {fixed}")
