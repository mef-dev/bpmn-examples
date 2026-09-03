"""Випрямляє стрілки й ставить підписи умов біля свого шлюзу.

Дві речі, які найдужче псують читання:
  * діагональний відрізок там, де мало бути коліно з двох прямих;
  * підпис умови, що відʼїхав від шлюзу на середину схеми — читач не бачить,
    до якої гілки він належить.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


def local(tag):
    return tag.split("}", 1)[-1]


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

flows = {f.get("id"): (f.get("sourceRef"), f.get("targetRef"))
         for f in root.iter() if local(f.tag) == "sequenceFlow"}
conditional = {f.get("id") for f in root.iter()
               if local(f.tag) == "sequenceFlow"
               and f.find("{*}conditionExpression") is not None}

def label_spot(fid):
    """Точка для підпису умови: уздовж самої гілки, а не під шлюзом.

    Простір просто під шлюзом зайнятий його власною назвою, тому підпис
    відсувається на 45 пікселів уздовж першого відрізка гілки й на 8 убік.
    """
    m = re.search(
        rf'<bpmndi:BPMNEdge id="[^"]*" bpmnElement="{fid}">(.*?)</bpmndi:BPMNEdge>',
        text, re.S)
    if not m:
        return None
    pts = [(float(x), float(y)) for x, y in
           re.findall(r'x="([-\d.]+)" y="([-\d.]+)"', m.group(1))]
    if len(pts) < 2:
        return None
    (x1, y1), (x2, y2) = pts[0], pts[1]
    if abs(x2 - x1) < abs(y2 - y1):          # гілка йде вниз або вгору
        step = 45 if y2 > y1 else -45
        return (x1 + 8, y1 + step)
    step = 45 if x2 > x1 else -45            # гілка йде вбік
    return (x1 + step, y1 - 22)


# --- підпис умови сідає на свою гілку, поруч зі шлюзом ---------------------
moved = 0
for fid in conditional:
    if flows[fid][0] not in bounds:
        continue
    spot = label_spot(fid)
    if not spot:
        continue
    m = re.search(
        rf'(<bpmndi:BPMNEdge id="[^"]*" bpmnElement="{fid}">.*?<bpmndi:BPMNLabel>\s*<omgdc:Bounds )'
        r'x="[-\d.]+" y="[-\d.]+"', text, re.S)
    if not m:
        continue
    text = text[:m.start()] + m.group(1) + f'x="{spot[0]:.0f}" y="{spot[1]:.0f}"' \
        + text[m.end():]
    moved += 1

# --- умовна гілка без підпису читається як безумовна ----------------------
added = 0
for fid in conditional:
    source = flows[fid][0]
    if source not in bounds:
        continue
    if re.search(rf'<sequenceFlow id="{fid}"[^>]*\sname="', text):
        continue
    node = re.search(rf'<sequenceFlow id="{fid}"[^>]*>(.*?)</sequenceFlow>',
                     text, re.S)
    expr = re.search(r"<conditionExpression[^>]*>(.*?)</conditionExpression>",
                     node.group(1), re.S)
    label = (expr.group(1).strip() if expr else "condition")
    label = label.replace("#Previous.StatusCode != 200", "not 200")
    text = re.sub(rf'(<sequenceFlow id="{fid}")',
                  rf'\1 name="{label}"', text, count=1)
    spot = label_spot(fid) or (bounds[source][0], bounds[source][1])
    text = re.sub(
        rf'(<bpmndi:BPMNEdge id="[^"]*" bpmnElement="{fid}">.*?)(\s*</bpmndi:BPMNEdge>)',
        lambda m, s=spot: m.group(1)
        + f'\n        <bpmndi:BPMNLabel>\n'
          f'          <omgdc:Bounds x="{s[0]:.0f}" y="{s[1]:.0f}" '
          f'width="60" height="14" />\n        </bpmndi:BPMNLabel>'
        + m.group(2),
        text, flags=re.S)
    added += 1

# --- прямі коліна замість діагоналей --------------------------------------
ROUTES = {
    # гілка відмови входить у кінцеву подію знизу, двома прямими
    "Flow_13s4qsf": [(1670, 400), (1740, 400), (1740, 58)],
    # елемент даних стоїть рівно над своєю задачею
    "Doa_Response": [(920, 110), (920, 70)],
}
for eid, points in ROUTES.items():
    body = "".join(f'\n        <di:waypoint x="{x}" y="{y}" />' for x, y in points)
    text = re.sub(
        rf'(<bpmndi:BPMNEdge id="[^"]*" bpmnElement="{eid}">).*?(\s*</bpmndi:BPMNEdge>)',
        lambda m, b=body: m.group(1) + b + "\n      </bpmndi:BPMNEdge>",
        text, flags=re.S)

# Елемент даних стоїть збоку-вгорі від своєї задачі, а не строго над нею:
# інакше асоціація йде вертикально і перетинає підпис, що лежить під фігурою.
text = text.replace('<omgdc:Bounds x="892" y="20" width="36" height="50" />',
                    '<omgdc:Bounds x="1000" y="15" width="36" height="50" />')

path.write_bytes(text.encode("utf-8"))

# --- звіт: скільки відрізків лишилося косими ------------------------------
root = ET.fromstring(text)
skew = []
for el in root.iter():
    if local(el.tag) != "BPMNEdge":
        continue
    pts = [(float(w.get("x")), float(w.get("y"))) for w in el
           if local(w.tag) == "waypoint"]
    name = el.get("bpmnElement")
    if name and name.startswith("As_"):
        continue  # асоціація коментаря — пряма лінія до тексту, це норма
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if abs(x1 - x2) > 0.5 and abs(y1 - y2) > 0.5:
            skew.append(name)
            break

print(f"підписів умов присунуто до шлюза: {moved}, дописано: {added}")
print(f"косих відрізків у потоках: {len(skew)}"
      + ("" if not skew else " — " + ", ".join(sorted(set(skew)))))
