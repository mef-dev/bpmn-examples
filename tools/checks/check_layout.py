"""Шукає справжні накладання фігур: у межах однієї площини і без урахування
граничної події, яка за стандартом сидить на межі своєї задачі.

Приймає шляхи до моделей; без аргументів бере всі приклади репозиторію."""
import pathlib
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2] / "flow-patterns"


def local(tag):
    return tag.split("}", 1)[-1]


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (ax + aw <= bx or bx + bw <= ax or ay + ah <= by or by + bh <= ay)


models = ([pathlib.Path(a) for a in sys.argv[1:]]
          or sorted(ROOT.rglob("*.bpmn")))

total = 0
for path in models:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    attached = {el.get("id"): el.get("attachedToRef")
                for el in root.iter() if el.get("attachedToRef")}
    print(path.name)
    for plane in root.iter():
        if local(plane.tag) != "BPMNPlane":
            continue
        shapes = []
        for child in plane:
            if local(child.tag) != "BPMNShape":
                continue
            b = child[0]
            shapes.append((child.get("bpmnElement"),
                           (float(b.get("x")), float(b.get("y")),
                            float(b.get("width")), float(b.get("height")))))
        clashes = []
        for i, (na, ba) in enumerate(shapes):
            for nb, bb in shapes[i + 1:]:
                if attached.get(na) == nb or attached.get(nb) == na:
                    continue
                if overlap(ba, bb):
                    clashes.append(f"{na} ↔ {nb}")
        xs = [b[0] for _, b in shapes]
        ys = [b[1] for _, b in shapes]
        size = (f"{max(x + w for _, (x, _, w, _) in shapes):.0f}"
                f"×{max(y + h for _, (_, y, _, h) in shapes):.0f}") if shapes else "—"
        print(f"   площина {plane.get('bpmnElement')}: {len(shapes)} фігур, поле {size}")
        for c in clashes:
            print(f"      НАКЛАДАННЯ: {c}")
        total += len(clashes)
print(f"\nсправжніх накладань: {total}")
