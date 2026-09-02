"""Ставить підписи шлюзів і умов туди, де крізь них не проходить лінія.

Типово переглядач кладе назву шлюза просто під ним — рівно там, де в більшості
схем виходить вниз одна з гілок. Текст опиняється на лінії. Те саме з підписом
умови, якщо його поставити на тій самій стороні.

Кожен підпис шукає собі місце сам: перебираються чверті навколо вузла, і
береться перша, де рамка не перетинає ані фігуру, ані відрізок будь-якої
стрілки, ані вже поставлений підпис.
"""
import html
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

CHAR_W = 6.3
LINE_H = 14
GAP = 12


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


def size(label, width_chars=22):
    words, lines, cur = label.split(), [], ""
    for word in words:
        if cur and len(cur) + 1 + len(word) > width_chars:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return (max(len(x) for x in lines) * CHAR_W + 8, len(lines) * LINE_H + 6)


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

taken = []


def free_spot(anchor, box_size, prefer=None):
    ax, ay, aw, ah = anchor
    lw, lh = box_size
    order = prefer or []
    order += [(aw + GAP, 4), (aw + GAP, -lh - GAP), (-lw - GAP, 4),
              (-lw - GAP, -lh - GAP), (aw / 2 - lw / 2, -lh - GAP),
              (aw / 2 - lw / 2, ah + GAP), (aw + GAP, ah + GAP),
              (-lw - GAP, ah + GAP)]
    for dx, dy in order:
        box = (ax + dx, ay + dy, lw, lh)
        if any(overlap(box, b) for b in shapes.values()):
            continue
        if any(hits(p1, p2, box) for pts in edges.values()
               for p1, p2 in zip(pts, pts[1:])):
            continue
        if any(overlap(box, t) for t in taken):
            continue
        taken.append(box)
        return box
    return None


# --- 1. назви шлюзів ------------------------------------------------------
gateways = [(el.get("id"), el.get("name")) for el in root.iter()
            if local(el.tag).endswith("Gateway") and (el.get("name") or "").strip()]
placed_g = 0
for gid, name in gateways:
    if gid not in shapes:
        continue
    box = free_spot(shapes[gid], size(name))
    if not box:
        continue
    label = (f'\n        <bpmndi:BPMNLabel>\n'
             f'          <omgdc:Bounds x="{box[0]:.0f}" y="{box[1]:.0f}" '
             f'width="{box[2]:.0f}" height="{box[3]:.0f}" />\n'
             f'        </bpmndi:BPMNLabel>')
    text, n = re.subn(
        rf'(<bpmndi:BPMNShape id="[^"]*" bpmnElement="{gid}"[^>]*>\s*'
        r'<omgdc:Bounds[^/]*/>)(\s*)(?:<bpmndi:BPMNLabel>.*?</bpmndi:BPMNLabel>\s*)?',
        lambda m, s=label: m.group(1) + s + "\n      ",
        text, count=1, flags=re.S)
    placed_g += bool(n)

# --- 2. підписи умов ------------------------------------------------------
conditional = [f.get("id") for f in root.iter()
               if local(f.tag) == "sequenceFlow"
               and f.find("{*}conditionExpression") is not None
               and (f.get("name") or "").strip()]
names = {f.get("id"): f.get("name") for f in root.iter()
         if local(f.tag) == "sequenceFlow"}
placed_c = 0
for fid in conditional:
    pts = edges.get(fid)
    if not pts or len(pts) < 2:
        continue
    lw, lh = size(names[fid], 14)
    (x1, y1), (x2, y2) = pts[0], pts[1]
    # рухаємось уздовж гілки і пробуємо обидві сторони від лінії
    box = None
    for along in (40, 70, 100, 130):
        if abs(x2 - x1) < abs(y2 - y1):
            base_y = y1 + (along if y2 > y1 else -along)
            options = [(x1 + GAP, base_y), (x1 - lw - GAP, base_y)]
        else:
            base_x = x1 + (along if x2 > x1 else -along)
            options = [(base_x, y1 - lh - GAP), (base_x, y1 + GAP)]
        for ox, oy in options:
            candidate = (ox, oy, lw, lh)
            if any(overlap(candidate, b) for b in shapes.values()):
                continue
            if any(hits(p1, p2, candidate) for pts2 in edges.values()
                   for p1, p2 in zip(pts2, pts2[1:])):
                continue
            if any(overlap(candidate, t) for t in taken):
                continue
            box = candidate
            break
        if box:
            break
    if not box:
        continue
    taken.append(box)
    text = re.sub(
        rf'(<bpmndi:BPMNEdge id="[^"]*" bpmnElement="{fid}">.*?)'
        r'(?:\s*<bpmndi:BPMNLabel>.*?</bpmndi:BPMNLabel>)?(\s*</bpmndi:BPMNEdge>)',
        lambda m, b=box: m.group(1)
        + f'\n        <bpmndi:BPMNLabel>\n'
          f'          <omgdc:Bounds x="{b[0]:.0f}" y="{b[1]:.0f}" '
          f'width="{b[2]:.0f}" height="{b[3]:.0f}" />\n        </bpmndi:BPMNLabel>'
        + m.group(2),
        text, count=1, flags=re.S)
    placed_c += 1

# --- 3. будь-який інший підпис, що ще лежить на лінії ---------------------
placed_o = 0
for el in ET.fromstring(text).iter():
    if local(el.tag) != "BPMNShape":
        continue
    lab = el.find("{*}BPMNLabel/{*}Bounds")
    node = el.get("bpmnElement")
    if lab is None or node not in shapes:
        continue
    box = (float(lab.get("x")), float(lab.get("y")),
           float(lab.get("width")), float(lab.get("height")))
    clash = (any(hits(p1, p2, box) for pts in edges.values()
                 for p1, p2 in zip(pts, pts[1:]))
             or any(overlap(box, b) for k, b in shapes.items() if k != node))
    if not clash:
        taken.append(box)
        continue
    spot = free_spot(shapes[node], (box[2], box[3]))
    if not spot:
        continue
    text = re.sub(
        rf'(<bpmndi:BPMNShape id="[^"]*" bpmnElement="{node}"[^>]*>\s*'
        r'<omgdc:Bounds[^/]*/>\s*<bpmndi:BPMNLabel>\s*<omgdc:Bounds )'
        r'x="[-\d.]+" y="[-\d.]+"',
        lambda m, b=spot: m.group(1) + f'x="{b[0]:.0f}" y="{b[1]:.0f}"',
        text, count=1, flags=re.S)
    placed_o += 1

path.write_bytes(text.encode("utf-8"))
print(f"назв шлюзів розміщено: {placed_g} із {len(gateways)}")
print(f"підписів умов розміщено: {placed_c} із {len(conditional)}")
print(f"інших підписів пересунуто: {placed_o}")
