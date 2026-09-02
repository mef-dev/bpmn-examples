"""Дає кожній кінцевій події власний елемент даних замість спільного.

Один елемент, від якого стрілки розходяться до двох кінцевих подій, читається
погано з двох причин. По-перше, будь-які два маршрути з однієї точки в різні
боки рано чи пізно перетинаються — і схема виглядає заплутаною там, де логіка
проста. По-друге, він приховує головне: успіх і невдача повертають різні тіла,
хоч і однакового типу.

Копія несе те саме ім'я типу, тож на схемі видно, що тип один, а тіла різні.

    python split_shared_data.py <модель.bpmn>
"""
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

# кінцеві події та елемент даних, який кожна з них читає
readers = {}
for end in re.finditer(r'<endEvent id="([^"]+)".*?</endEvent>', text, re.S):
    src = re.search(r"<sourceRef>([^<]+)</sourceRef>", end.group(0))
    if src:
        readers.setdefault(src.group(1).strip(), []).append(end.group(1))

split = []
for ref, ends in readers.items():
    if len(ends) < 2:
        continue

    declaration = re.search(
        rf'<dataObjectReference id="{ref}" name="([^"]*)" '
        r'dataObjectRef="([^"]+)" />', text)
    shape = re.search(
        rf'<bpmndi:BPMNShape id="[^"]*" bpmnElement="{ref}">\s*'
        r'<omgdc:Bounds x="([-\d.]+)" y="([-\d.]+)" '
        r'width="([\d.]+)" height="([\d.]+)" />', text)
    if not declaration or not shape:
        continue

    name, obj = declaration.group(1), declaration.group(2)
    x, y, w, h = (float(shape.group(i)) for i in range(1, 5))

    # Копія стає біля своєї кінцевої події так само, як оригінал стоїть біля
    # своєї: тоді стрілка коротка й ні з чим не сперечається.
    def bounds_of(node_id):
        m = re.search(
            rf'<bpmndi:BPMNShape id="[^"]*" bpmnElement="{node_id}">\s*'
            r'<omgdc:Bounds x="([-\d.]+)" y="([-\d.]+)"', text)
        return (float(m.group(1)), float(m.group(2))) if m else None

    origin = bounds_of(ends[0])
    offset = (x - origin[0], y - origin[1]) if origin else (0.0, h + 40)

    # перша подія лишається з наявним елементом, решта дістає власні копії
    for index, end_id in enumerate(ends[1:], start=1):
        new_ref, new_obj = f"{ref}_{index}", f"{obj}_{index}"
        text = text.replace(
            f'<dataObjectReference id="{ref}" name="{name}" dataObjectRef="{obj}" />',
            f'<dataObjectReference id="{ref}" name="{name}" dataObjectRef="{obj}" />\n'
            f'    <dataObjectReference id="{new_ref}" name="{name}" '
            f'dataObjectRef="{new_obj}" />\n'
            f'    <dataObject id="{new_obj}" />', 1)

        end_block = re.search(rf'<endEvent id="{end_id}".*?</endEvent>', text, re.S)
        text = text.replace(
            end_block.group(0),
            end_block.group(0).replace(f"<sourceRef>{ref}</sourceRef>",
                                       f"<sourceRef>{new_ref}</sourceRef>"), 1)

        here = bounds_of(end_id) or (x, y + (h + 40) * index)
        nx, ny = here[0] + offset[0], here[1] + offset[1]
        text = re.sub(
            r"(\s*</bpmndi:BPMNPlane>)",
            lambda m, r=new_ref, xx=nx, yy=ny:
            f'\n      <bpmndi:BPMNShape id="Sh_{r}" bpmnElement="{r}">\n'
            f'        <omgdc:Bounds x="{xx:.0f}" y="{yy:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" />\n'
            f"      </bpmndi:BPMNShape>" + m.group(1),
            text, count=1)
        split.append(f"{new_ref} для {end_id}")

path.write_bytes(text.encode("utf-8"))
print(f"елементів даних розділено: {len(split)}"
      + (f" — {', '.join(split)}" if split else ""))
