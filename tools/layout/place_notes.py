"""Ставить коментарі так, щоб вони нічого не перекривали, і прибирає зі схеми
елементи без жодної стрілки.

Дві біди на одній схемі:
  * підпис лежить на лінії або на сусідньому вузлі;
  * елемент намальовано, але до нього нічого не веде — читач не розуміє, звідки
    він узявся. Оголошення контракту (ioSpecification) лишається в моделі, але
    на полотні йому робити нічого: рушій його не читає, а стрілок у нього нема.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

GAP = 40
STEP = 45


def local(tag):
    return tag.split("}", 1)[-1]


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


def segment_hits_box(p1, p2, box):
    """Груба, але достатня перевірка: чи проходить відрізок крізь прямокутник."""
    x, y, w, h = box
    steps = 40
    for i in range(steps + 1):
        t = i / steps
        px = p1[0] + (p2[0] - p1[0]) * t
        py = p1[1] + (p2[1] - p1[1]) * t
        if x <= px <= x + w and y <= py <= y + h:
            return True
    return False


path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
root = ET.fromstring(text)

shapes, edges = {}, {}
for el in root.iter():
    if local(el.tag) == "BPMNShape":
        b = el[0]
        shapes[el.get("bpmnElement")] = (
            float(b.get("x")), float(b.get("y")),
            float(b.get("width")), float(b.get("height")))
    elif local(el.tag) == "BPMNEdge":
        edges[el.get("bpmnElement")] = [
            (float(w.get("x")), float(w.get("y"))) for w in el
            if local(w.tag) == "waypoint"]

annotations = {el.get("id") for el in root.iter()
               if local(el.tag) == "textAnnotation"}
links = {}
for el in root.iter():
    if local(el.tag) == "association":
        links[el.get("id")] = (el.get("sourceRef"), el.get("targetRef"))

# --- 1. елементи без жодної стрілки зі схеми зникають ---------------------
connected = set()
for el in root.iter():
    if local(el.tag) in ("sequenceFlow", "association"):
        connected.update({el.get("sourceRef"), el.get("targetRef")})
    elif local(el.tag) in ("dataInputAssociation", "dataOutputAssociation"):
        connected.update({(el.findtext("{*}sourceRef") or "").strip(),
                          (el.findtext("{*}targetRef") or "").strip()})
    elif local(el.tag) == "boundaryEvent":
        connected.add(el.get("id"))

removed = []
for name in list(shapes):
    kind = next((local(e.tag) for e in root.iter() if e.get("id") == name), "")
    if kind in ("dataInput", "dataOutput") and name not in connected:
        text = re.sub(
            rf'\s*<bpmndi:BPMNShape id="[^"]*" bpmnElement="{name}">.*?</bpmndi:BPMNShape>',
            "", text, flags=re.S)
        shapes.pop(name)
        removed.append(name)

# --- 2. коментар шукає місце, де нікому не заважає ------------------------
def candidates(node_box, note_box):
    nx, ny, nw, nh = node_box
    aw, ah = note_box[2], note_box[3]
    cx = nx + nw / 2 - aw / 2
    cy = ny + nh / 2 - ah / 2
    for k in range(6):
        d = GAP + k * STEP
        yield (cx, ny - ah - d)          # згори
        yield (cx, ny + nh + d)          # знизу
        yield (nx - aw - d, cy)          # ліворуч
        yield (nx + nw + d, cy)          # праворуч


moved = 0
for aid, (src, dst) in links.items():
    note = dst if dst in annotations else src
    node = src if note == dst else dst
    if note not in shapes or node not in shapes:
        continue
    others = {k: v for k, v in shapes.items() if k != note}
    for x, y in candidates(shapes[node], shapes[note]):
        box = (x, y, shapes[note][2], shapes[note][3])
        if any(overlap(box, b) for b in others.values()):
            continue
        if any(segment_hits_box(p1, p2, box)
               for name, pts in edges.items() if name != aid
               for p1, p2 in zip(pts, pts[1:])):
            continue
        shapes[note] = box
        text = re.sub(
            rf'(<bpmndi:BPMNShape id="[^"]*" bpmnElement="{note}">\s*<omgdc:Bounds )'
            r'x="[-\d.]+" y="[-\d.]+"',
            lambda m, b=box: m.group(1) + f'x="{b[0]:.0f}" y="{b[1]:.0f}"',
            text, count=1)
        moved += 1
        break

path.write_bytes(text.encode("utf-8"))
print(f"зі схеми прибрано без стрілок: {', '.join(removed) or 'нічого'}")
print(f"коментарів переставлено на вільне місце: {moved}")
