"""Будує граничну подію-повідомлення, яку крок піднімає з коду.

`gen` створює лише граничні події помилки. Якщо крок кличе
`Action.BoundaryEvents["…"].Raise(…)`, а такої події в моделі немає, модель
однаково скомпілюється — і впаде на першому ж запуску. Тому подія оголошується
в специфікації поруч із кроком, який її піднімає:

    "raises": {
      "id": "Event_Progress",
      "name": "progress",
      "to": { "id": "Event_Notify", "name": "notify subscribers",
              "process": "Server-side events",
              "data": { "alias": "bss", "pluginname": "BSS.Entities" } }
    }

Подія неперервна (`cancelActivity="false"`): крок продовжує роботу, а гілка
події йде своїм шляхом — саме заради цього її й піднімають.

    python add_boundary_event.py <модель.bpmn> --spec <модель.spec.json>
"""
import argparse
import html
import json
import pathlib
import re


def esc(value):
    return html.escape(json.dumps(value, ensure_ascii=False), quote=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("model")
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    path = pathlib.Path(args.model)
    text = path.read_text(encoding="utf-8")
    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))

    added = []
    for step in spec.get("steps") or []:
        raises = step.get("raises")
        if not raises or f'id="{raises["id"]}"' in text:
            continue

        target = raises.get("to") or {}
        throw_id = target.get("id", f"{raises['id']}_Target")
        throw = {"tsk_ProcessName": target.get("process", "Server-side events"),
                 "data": target.get("data", {}), "lang": "en"}

        shape = re.search(
            rf'<bpmndi:BPMNShape id="[^"]*" bpmnElement="{step["id"]}">\s*'
            r'<omgdc:Bounds x="([-\d.]+)" y="([-\d.]+)" '
            r'width="([\d.]+)" height="([\d.]+)"', text)
        if not shape:
            continue
        x, y, w, h = (float(shape.group(i)) for i in range(1, 5))

        text = re.sub(
            r"(\s*</process>)",
            lambda m, r=raises, t=throw_id, cfg=throw:
            f'\n    <boundaryEvent id="{r["id"]}" name="{r.get("name", "")}" '
            f'cancelActivity="false" attachedToRef="{step["id"]}">\n'
            f'      <outgoing>Fl_{r["id"]}</outgoing>\n'
            f'      <messageEventDefinition id="Med_{r["id"]}" />\n'
            f"    </boundaryEvent>\n"
            f'    <intermediateThrowEvent id="{t}" '
            f'name="{target.get("name", "notify")}">\n'
            f"      <extensionElements>\n"
            f'        <ep:elementParameter name="ThrowMessageEvent">'
            f"{esc(cfg)}</ep:elementParameter>\n"
            f"      </extensionElements>\n"
            f'      <incoming>Fl_{r["id"]}</incoming>\n'
            f'      <messageEventDefinition id="Med_{t}" />\n'
            f"    </intermediateThrowEvent>\n"
            f'    <sequenceFlow id="Fl_{r["id"]}" sourceRef="{r["id"]}" '
            f'targetRef="{t}" />' + m.group(1),
            text, count=1)

        ex, ey = x + w / 2 - 18, y + h - 18
        tx, ty = x + w + 120, y + h - 18
        text = re.sub(
            r"(\s*</bpmndi:BPMNPlane>)",
            lambda m, r=raises["id"], t=throw_id:
            f'\n      <bpmndi:BPMNShape id="Sh_{r}" bpmnElement="{r}">\n'
            f'        <omgdc:Bounds x="{ex:.0f}" y="{ey:.0f}" '
            f'width="36" height="36" />\n'
            f"      </bpmndi:BPMNShape>\n"
            f'      <bpmndi:BPMNShape id="Sh_{t}" bpmnElement="{t}">\n'
            f'        <omgdc:Bounds x="{tx:.0f}" y="{ty:.0f}" '
            f'width="36" height="36" />\n'
            f"      </bpmndi:BPMNShape>\n"
            f'      <bpmndi:BPMNEdge id="Ed_Fl_{r}" bpmnElement="Fl_{r}">\n'
            f'        <di:waypoint x="{ex + 36:.0f}" y="{ey + 18:.0f}" />\n'
            f'        <di:waypoint x="{tx:.0f}" y="{ty + 18:.0f}" />\n'
            f"      </bpmndi:BPMNEdge>" + m.group(1),
            text, count=1)
        added.append(f'{raises["id"]} -> {throw_id}')

    path.write_bytes(text.encode("utf-8"))
    print(f"граничних подій додано: {len(added)}"
          + (f" — {', '.join(added)}" if added else ""))


if __name__ == "__main__":
    main()
