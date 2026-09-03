"""Ставить у модель коментарі, оголошені в специфікації.

Дві речі, без яких приклад не вчить нічому:

  * рішення, ухвалене в кроці, пояснене поруч із кроком, а не в тікеті;
  * приклад входу видно одразу, тож перше, що робить новачок, — запускає його,
    а не вгадує форму запиту.

Зміст беруть зі специфікації: `steps[].note` для кроку і `input.example` для
входу (без нього приклад збирається з типів властивостей). Розміри рамок
і розташування далі наводять fit_notes.py і place_notes.py.

    python add_notes.py <модель.bpmn> --spec <модель.spec.json>
"""
import argparse
import html
import json
import pathlib
import re

PLACEHOLDER = {
    "string": "text",
    "integer": 0,
    "number": 0,
    "boolean": False,
}


def example_for(spec):
    """Приклад входу: явний зі специфікації або зібраний із типів."""
    given = (spec.get("input") or {}).get("example")
    if given is not None:
        return given
    body = {}
    for name, kind in ((spec.get("input") or {}).get("properties") or {}).items():
        body[name] = PLACEHOLDER.get(kind, "text")
    return body


def annotation(aid, text, target, x, y):
    """Коментар, стрілка від нього до вузла, і фігури для обох."""
    body = html.escape(text, quote=False)
    process = (f'    <textAnnotation id="{aid}">\n'
               f'      <text>{body}</text>\n'
               f'    </textAnnotation>\n'
               f'    <association id="As_{aid}" sourceRef="{aid}" '
               f'targetRef="{target}" />\n')
    lines = text.splitlines() or [""]
    width = max(len(line) for line in lines) * 6.3 + 22
    height = len(lines) * 14 + 18
    diagram = (f'      <bpmndi:BPMNShape id="Sh_{aid}" bpmnElement="{aid}">\n'
               f'        <omgdc:Bounds x="{x:.0f}" y="{y:.0f}" '
               f'width="{width:.0f}" height="{height:.0f}" />\n'
               f'      </bpmndi:BPMNShape>\n'
               f'      <bpmndi:BPMNEdge id="Ed_As_{aid}" bpmnElement="As_{aid}">\n'
               f'        <di:waypoint x="{x:.0f}" y="{y + height / 2:.0f}" />\n'
               f'        <di:waypoint x="{x - 40:.0f}" y="{y + height / 2:.0f}" />\n'
               f'      </bpmndi:BPMNEdge>\n')
    return process, diagram


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("model")
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    path = pathlib.Path(args.model)
    text = path.read_text(encoding="utf-8")
    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))

    bounds = {m.group(1): (float(m.group(2)), float(m.group(3)),
                           float(m.group(4)), float(m.group(5)))
              for m in re.finditer(
                  r'<bpmndi:BPMNShape id="[^"]*" bpmnElement="([^"]+)">\s*'
                  r'<omgdc:Bounds x="([-\d.]+)" y="([-\d.]+)" '
                  r'width="([\d.]+)" height="([\d.]+)"', text)}

    start = re.search(r'<startEvent id="([^"]+)"', text)
    wanted = []
    if start:
        wanted.append(("An_Input", "Example input:\n"
                       + json.dumps(example_for(spec), indent=2,
                                    ensure_ascii=False), start.group(1)))
    for step in spec.get("steps") or []:
        if step.get("note"):
            wanted.append((f"An_{step['id']}", step["note"], step["id"]))

    process_block, diagram_block, added = "", "", []
    for aid, note, target in wanted:
        if f'id="{aid}"' in text or target not in bounds:
            continue
        tx, ty, tw, th = bounds[target]
        p, d = annotation(aid, note, target, tx + tw + 90, ty)
        process_block += p
        diagram_block += d
        added.append(aid)

    if process_block:
        text = re.sub(r"(\s*</process>)",
                      lambda m, s=process_block: "\n" + s + m.group(1),
                      text, count=1)
        text = re.sub(r"(\s*</bpmndi:BPMNPlane>)",
                      lambda m, s=diagram_block: "\n" + s + m.group(1),
                      text, count=1)

    path.write_bytes(text.encode("utf-8"))
    print(f"коментарів додано: {len(added)}"
          + (f" — {', '.join(added)}" if added else ""))


if __name__ == "__main__":
    main()
