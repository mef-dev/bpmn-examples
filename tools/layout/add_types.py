"""Додає в модель типи, які крок вживає понад свій вхід і вихід.

Генератор оголошує рівно те, що знає зі специфікації: вхідний тип, тип помилки
й зовнішній тип конфігурації. Але крок може будувати власну проміжну структуру
або звертатися до типу платформи — і тоді компілятор скаже `CS0246: type or
namespace name not found`, хоч у моделі все на вигляд на місці.

Такі типи оголошуються в специфікації поруч із кроками, що їх вживають:

    "types":         { "PageInfo": { … JSON Schema … } }
    "externalTypes": { "ChatMessage": "types://external/…" }

    python add_types.py <модель.bpmn> --spec <модель.spec.json>
"""
import argparse
import html
import json
import pathlib
import re


def esc(value):
    return html.escape(json.dumps(value, ensure_ascii=False), quote=False)


def replace_block(text, block, items):
    return re.sub(
        rf'(<gp:globalParameter name="{block}">).*?(</gp:globalParameter>)',
        lambda m: m.group(1) + esc(items) + m.group(2),
        text, count=1, flags=re.S)


def read_block(text, block):
    m = re.search(rf'<gp:globalParameter name="{block}">(.*?)</gp:globalParameter>',
                  text, re.S)
    return json.loads(html.unescape(m.group(1))) if m else []


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("model")
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    path = pathlib.Path(args.model)
    text = path.read_text(encoding="utf-8")
    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))

    added = []

    inner = read_block(text, "InnerTypes")
    known = {t.get("name") for t in inner}
    for name, schema in (spec.get("types") or {}).items():
        if name in known:
            continue
        # Тип описують або схемою JSON, або оголошенням класу мовою платформи.
        # Друге треба позначити isNativeDefinition, інакше платформа спробує
        # прочитати клас як схему, і компіляція розсиплеться синтаксисом.
        native = isinstance(schema, str)
        inner.insert(0, {
            "name": name,
            "isNativeDefinition": native,
            "definition": schema if native else json.dumps(schema, ensure_ascii=False),
            "dataObjectRefName": name})
        added.append(name)
    if added:
        text = replace_block(text, "InnerTypes", inner)

    external = read_block(text, "ExternalTypes")
    known = {t.get("name") for t in external}
    for name, definition in (spec.get("externalTypes") or {}).items():
        if name in known:
            continue
        external.append({"name": name, "definition": definition})
        added.append(name)
    if spec.get("externalTypes"):
        text = replace_block(text, "ExternalTypes", external)

    # Зовнішній тип живе в бібліотеці, і без її оголошення платформа скаже
    # «Cannot resolve type» на цілком правильне посилання.
    libs = read_block(text, "UsedLibs")
    known = {lib.get("name") for lib in libs}
    for name, link in (spec.get("libs") or {}).items():
        if name in known:
            continue
        libs.append({"name": name, "link": link, "version": "", "entities": []})
        added.append(name)
    if spec.get("libs"):
        text = replace_block(text, "UsedLibs", libs)

    path.write_bytes(text.encode("utf-8"))
    print(f"типів додано: {len(added)}"
          + (f" — {', '.join(added)}" if added else ""))


if __name__ == "__main__":
    main()
