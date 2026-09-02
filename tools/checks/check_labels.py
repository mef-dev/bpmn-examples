"""Рахує, чи не лежить якийсь підпис на лінії, фігурі або іншому підписі."""
import pathlib
import sys
import xml.etree.ElementTree as ET


def local(tag):
    return tag.split("}", 1)[-1]


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


def hits(p1, p2, box):
    x, y, w, h = box
    for i in range(41):
        t = i / 40
        px, py = p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t
        if x <= px <= x + w and y <= py <= y + h:
            return True
    return False


root = ET.fromstring(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))

shapes, edges, labels = {}, {}, {}
for el in root.iter():
    if local(el.tag) == "BPMNShape":
        b = el[0]
        shapes[el.get("bpmnElement")] = (
            float(b.get("x")), float(b.get("y")),
            float(b.get("width")), float(b.get("height")))
        lab = el.find("{*}BPMNLabel/{*}Bounds")
        if lab is not None:
            labels[el.get("bpmnElement")] = (
                float(lab.get("x")), float(lab.get("y")),
                float(lab.get("width")), float(lab.get("height")))
    elif local(el.tag) == "BPMNEdge":
        edges[el.get("bpmnElement")] = [
            (float(w.get("x")), float(w.get("y"))) for w in el
            if local(w.tag) == "waypoint"]
        lab = el.find("{*}BPMNLabel/{*}Bounds")
        if lab is not None:
            labels[el.get("bpmnElement")] = (
                float(lab.get("x")), float(lab.get("y")),
                float(lab.get("width")), float(lab.get("height")))

bad = 0
for name, box in labels.items():
    on_shape = [k for k, b in shapes.items() if k != name and overlap(box, b)]
    on_edge = [k for k, pts in edges.items()
               if any(hits(p1, p2, box) for p1, p2 in zip(pts, pts[1:]))]
    on_label = [k for k, b in labels.items() if k != name and overlap(box, b)]
    if on_shape or on_edge or on_label:
        bad += 1
        print(f"   {name}: фігури={on_shape} лінії={on_edge} підписи={on_label}")

print(f"підписів усього: {len(labels)}   із накладанням: {bad}")

# Підпис елемента даних мусить стояти під своєю фігурою, а не поруч із чужою.
KINDS = ("dataObjectReference", "dataStoreReference", "dataInput", "dataOutput")
data_ids = {el.get("id") for el in root.iter()
            if local(el.tag) in KINDS and el.get("id")}
drift = 0
for name in data_ids & set(labels):
    sx, sy, sw, sh = shapes[name]
    lx, ly, lw, lh = labels[name]
    off = abs((lx + lw / 2) - (sx + sw / 2))
    if off > 20 or ly < sy + sh:
        print(f"   {name}: підпис зсунуто на {off:.0f} px убік"
              f"{' і не під фігурою' if ly < sy + sh else ''}")
        drift += 1
print(f"підписів елементів даних не на місці: {drift}")
