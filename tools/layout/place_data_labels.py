"""Ставить підпис елемента даних під його власною фігурою.

Підпис Data Object чи Data Store, що відʼїхав від своєї іконки, читається як
підпис сусіднього вузла — на скріншоті TestResult опинився під кінцевою подією.
За стандартом він центрується під самою фігурою, і жоден інший прохід не має
права його звідти забирати.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

CHAR_W = 6.0
LINE_H = 14
GAP = 6
KINDS = ("dataObjectReference", "dataStoreReference", "dataInput", "dataOutput")


def local(tag):
    return tag.split("}", 1)[-1]


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
root = ET.fromstring(text)

names, shapes = {}, {}
for el in root.iter():
    if local(el.tag) in KINDS and el.get("id"):
        names[el.get("id")] = (el.get("name") or "").strip()
    elif local(el.tag) == "BPMNShape":
        b = el[0]
        shapes[el.get("bpmnElement")] = (
            float(b.get("x")), float(b.get("y")),
            float(b.get("width")), float(b.get("height")))

occupied = [b for k, b in shapes.items() if k not in names]

# Лінії теж зайняті: підпис, що ліг на власну асоціацію, читається як розрив.
segments = []
for el in root.iter():
    if local(el.tag) != "BPMNEdge":
        continue
    pts = [(float(w.get("x")), float(w.get("y"))) for w in el
           if local(w.tag) == "waypoint"]
    segments.extend(zip(pts, pts[1:]))


def hits(p1, p2, box):
    x, y, w, h = box
    for i in range(41):
        t = i / 40
        px, py = p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t
        if x <= px <= x + w and y <= py <= y + h:
            return True
    return False

fixed = 0
for eid, name in names.items():
    if eid not in shapes or not name:
        continue
    x, y, w, h = shapes[eid]
    lw = max(len(name) * CHAR_W + 10, w)
    lh = LINE_H + 4
    lx = x + w / 2 - lw / 2
    ly = y + h + GAP
    # Підпис стоїть під своєю фігурою і ніде більше: горизонтальний зсув
    # перетворив би його на підпис сусіда. Якщо просто під фігурою вже стоїть
    # інша фігура — опускаємось, але тільки вниз. Лінії тут не враховуються:
    # це вони обходять підпис, а не навпаки (див. snap_associations.py).
    for _ in range(8):
        box = (lx, ly, lw, lh)
        if not any(overlap(box, b) for b in occupied):
            break
        ly += lh + 4

    label = (f'\n        <bpmndi:BPMNLabel>\n'
             f'          <omgdc:Bounds x="{lx:.0f}" y="{ly:.0f}" '
             f'width="{lw:.0f}" height="{lh:.0f}" />\n'
             f'        </bpmndi:BPMNLabel>')
    text, n = re.subn(
        rf'(<bpmndi:BPMNShape id="[^"]*" bpmnElement="{eid}"[^>]*>\s*'
        r'<omgdc:Bounds[^/]*/>)(?:\s*<bpmndi:BPMNLabel>.*?</bpmndi:BPMNLabel>)?',
        lambda m, s=label: m.group(1) + s,
        text, count=1, flags=re.S)
    fixed += bool(n)

path.write_bytes(text.encode("utf-8"))
print(f"підписів елементів даних поставлено під власну фігуру: {fixed}")
