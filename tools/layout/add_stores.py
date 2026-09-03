"""Додає сховище даних і привʼязує його до кроку, який ним користується.

`gen` сховищ не створює, а без них файлові приклади неможливі: тека, файл і
архів приходять у модель саме через `dataStoreReference`.

Привʼязка обовʼязкова. Рушій показує кроку лише ті сховища, для яких є
`dataInputAssociation` (`WorkflowNodeAnalyzer.cs:67`): він перебирає всі
оголошені сховища і бере тільки ті, що знайшлися серед вхідних асоціацій
вузла. Сховище без привʼязки скомпілюється й не існуватиме в коді.

Оголошується поруч із кроком:

    "stores": [
      { "id": "DS_Reports", "name": "reports folder", "type": "Folder",
        "connection": "file://documents/tenant", "object": "{Input.folder}",
        "usedBy": "T_Archive" }
    ]

`type` — те саме, що в панелі властивостей: `File`, `Folder`, `MSSQL.Procedure`
та інші. У коді кроку сховище доступне як `DataAssociations.<id>`.

    python add_stores.py <модель.bpmn> --spec <модель.spec.json>
"""
import argparse
import html
import json
import pathlib
import re


def esc(value):
    return html.escape(json.dumps(value, ensure_ascii=False, indent=2),
                       quote=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("model")
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    path = pathlib.Path(args.model)
    text = path.read_text(encoding="utf-8")
    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))

    added = []
    for store in spec.get("stores") or []:
        store_id = store["id"]
        if f'id="{store_id}"' in text:
            continue
        step_id = store["usedBy"]

        setting = {"type": store.get("type", "File"),
                   "connection": store["connection"],
                   "object": store.get("object", ""),
                   "parameters": store.get("parameters", [])}

        # Сам елемент сховища.
        text = re.sub(
            r"(\s*</process>)",
            lambda m, s=store_id, n=store.get("name", ""), cfg=setting:
            f'\n    <dataStoreReference id="{s}" name="{n}">\n'
            f"      <extensionElements>\n"
            f'        <ep:elementParameter name="storeParameters">'
            f"{esc(cfg)}</ep:elementParameter>\n"
            f"      </extensionElements>\n"
            f"    </dataStoreReference>" + m.group(1),
            text, count=1)

        # Привʼязка до кроку: без неї сховища для коду не існує.
        step = re.search(
            rf'(<(?:task|serviceTask) id="{step_id}"[^>]*>)(.*?)'
            r"(</(?:task|serviceTask)>)", text, re.S)
        if not step:
            raise SystemExit(f"крок {step_id} не знайдено — привʼязати нема до чого")
        body = step.group(2)
        # Кожній асоціації потрібна власна властивість-заглушка: спільної на
        # два сховища не буває, targetRef указує рівно на одну.
        body += (f'      <property id="Prop_{store_id}" '
                 f'name="__targetRef_placeholder" />\n')
        body += (f'      <dataInputAssociation id="Dia_{store_id}">\n'
                 f"        <sourceRef>{store_id}</sourceRef>\n"
                 f"        <targetRef>Prop_{store_id}</targetRef>\n"
                 f"      </dataInputAssociation>\n")
        text = text[:step.start()] + step.group(1) + body + step.group(3) \
            + text[step.end():]

        # Фігура сховища під своїм кроком і стрілка до нього.
        shape = re.search(
            rf'<bpmndi:BPMNShape id="[^"]*" bpmnElement="{step_id}">\s*'
            r'<omgdc:Bounds x="([-\d.]+)" y="([-\d.]+)" '
            r'width="([\d.]+)" height="([\d.]+)"', text)
        if not shape:
            raise SystemExit(f"фігури кроку {step_id} немає — нема куди ставити")
        x, y, w, h = (float(shape.group(i)) for i in range(1, 5))

        # Місце під фігуру шукається, а не призначається: під кроком уже може
        # стояти елемент даних або кінцева подія, і накладання ловить власна
        # перевірка розкладки.
        taken = [(float(a), float(b), float(c), float(d)) for a, b, c, d
                 in re.findall(r'<omgdc:Bounds x="([-\d.]+)" y="([-\d.]+)" '
                               r'width="([\d.]+)" height="([\d.]+)"', text)]

        def free(px, py, pw=50, ph=50, pad=20):
            return all(px + pw + pad <= tx or tx + tw + pad <= px
                       or py + ph + pad <= ty or ty + th + pad <= py
                       for tx, ty, tw, th in taken)

        sx, sy = x + w / 2 - 25, y + h + 70
        for dx, dy in ((0, 0), (-110, 0), (110, 0), (0, 90), (-110, 90),
                       (110, 90), (0, 180), (-160, 180)):
            if free(sx + dx, sy + dy):
                sx, sy = sx + dx, sy + dy
                break

        text = re.sub(
            r"(\s*</bpmndi:BPMNPlane>)",
            lambda m, s=store_id:
            f'\n      <bpmndi:BPMNShape id="Sh_{s}" bpmnElement="{s}">\n'
            f'        <omgdc:Bounds x="{sx:.0f}" y="{sy:.0f}" '
            f'width="50" height="50" />\n'
            f"        <bpmndi:BPMNLabel>\n"
            f'          <omgdc:Bounds x="{sx - 7:.0f}" y="{sy + 57:.0f}" '
            f'width="64" height="14" />\n'
            f"        </bpmndi:BPMNLabel>\n"
            f"      </bpmndi:BPMNShape>\n"
            f'      <bpmndi:BPMNEdge id="Ed_Dia_{s}" bpmnElement="Dia_{s}">\n'
            f'        <di:waypoint x="{sx + 25:.0f}" y="{sy:.0f}" />\n'
            f'        <di:waypoint x="{x + w / 2:.0f}" y="{y + h:.0f}" />\n'
            f"      </bpmndi:BPMNEdge>" + m.group(1),
            text, count=1)
        added.append(f"{store_id} ({setting['type']}) -> {step_id}")

    path.write_bytes(text.encode("utf-8"))
    print(f"сховищ даних додано: {len(added)}"
          + (f" — {', '.join(added)}" if added else ""))


if __name__ == "__main__":
    main()
