"""Звіряє кінці кожної стрілки з фігурами, які вона мусить зʼєднувати.

Ребро, що не дотягується до своєї фігури, читається як обрив: лінія йде
в порожнечу. Перевіряються всі види звʼязків — потоки, асоціації коментарів
і асоціації даних.
"""
import pathlib
import sys
import xml.etree.ElementTree as ET

TOLERANCE = 3.0


def local(tag):
    return tag.split("}", 1)[-1]


def distance_to_box(point, box):
    px, py = point
    x, y, w, h = box
    dx = max(x - px, 0, px - (x + w))
    dy = max(y - py, 0, py - (y + h))
    return (dx * dx + dy * dy) ** 0.5


total = 0
for path in [pathlib.Path(a) for a in sys.argv[1:]]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))

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

    links = {}
    for el in root.iter():
        kind = local(el.tag)
        if kind in ("sequenceFlow", "association"):
            links[el.get("id")] = (el.get("sourceRef"), el.get("targetRef"))
        elif kind == "dataInputAssociation":
            src = (el.findtext("{*}sourceRef") or "").strip()
            # ціль — властивість-заглушка на самому вузлі, тож беремо вузол
            owner = None
            for node in root.iter():
                if el in list(node):
                    owner = node.get("id")
                    break
            links[el.get("id")] = (src, owner)
        elif kind == "dataOutputAssociation":
            dst = (el.findtext("{*}targetRef") or "").strip()
            owner = None
            for node in root.iter():
                if el in list(node):
                    owner = node.get("id")
                    break
            links[el.get("id")] = (owner, dst)

    broken = []
    for eid, points in edges.items():
        if eid not in links or len(points) < 2:
            continue
        src, dst = links[eid]
        for end, node, label in ((points[0], src, "початок"),
                                 (points[-1], dst, "кінець")):
            if node not in shapes:
                continue
            gap = distance_to_box(end, shapes[node])
            if gap > TOLERANCE:
                broken.append(f"{eid}: {label} за {gap:.0f} px від {node}")

    if broken:
        print(f"{path.name}:")
        for item in broken:
            print(f"      {item}")
    total += len(broken)

print(f"\nобірваних кінців: {total}   (допуск {TOLERANCE:.0f} px)")
