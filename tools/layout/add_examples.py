"""Вписує в модель документацію процесу і приклади відповідей зі специфікації.

Кінцева подія без прикладу лишає читача наодинці з типом: він бачить, що
повертається `TestResult`, і не бачить жодного справжнього тіла. А документація
без посилання на джерело перетворює опублікований `flow` на файл без роду —
знайти, звідки він і як його перезібрати, стає нічим.

Посилання виводиться зі шляху моделі в репозиторії, тому його не треба писати
руками й неможливо забути оновити після переїзду файлу.

    python add_examples.py <модель.bpmn> --spec <модель.spec.json>
"""
import argparse
import html
import json
import pathlib
import re

SOURCE = "https://github.com/mef-dev/bpmn-examples/tree/master"


def esc(value):
    return html.escape(json.dumps(value, ensure_ascii=False), quote=False)


def source_link(model: pathlib.Path) -> str:
    parts = model.resolve().parts
    if "flow-patterns" not in parts:
        return SOURCE
    group = parts[parts.index("flow-patterns"):-1]
    return f"{SOURCE}/{'/'.join(group)}"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("model")
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()

    path = pathlib.Path(args.model)
    text = path.read_text(encoding="utf-8")
    spec = json.loads(pathlib.Path(args.spec).read_text(encoding="utf-8"))

    changed = []

    documentation = spec.get("documentation")
    if documentation:
        body = html.escape(f"{documentation}\nSource: {source_link(path)}",
                           quote=False)
        text, n = re.subn(r"<documentation>.*?</documentation>",
                          lambda m, b=body: f"<documentation>{b}</documentation>",
                          text, count=1, flags=re.S)
        if not n:
            text, n = re.subn(
                r'(<process id="[^"]*"[^>]*>)',
                lambda m, b=body: m.group(1)
                + f"\n    <documentation>{b}</documentation>",
                text, count=1)
        changed.append("документація")

    # Наслідок обирається за кодом маршруту: усе, що менше 400, — успіх.
    outcomes = spec.get("outcomes") or {}
    filled = 0

    def fill(match):
        nonlocal filled
        route = json.loads(html.unescape(match.group(1)))
        key = "success" if int(route.get("code", 200)) < 400 else "failure"
        outcome = outcomes.get(key)
        if not outcome:
            return match.group(0)
        route["exampelsVariants"] = [{"title": outcome["title"],
                                      "value": outcome["value"]}]
        filled += 1
        return ('<ep:elementParameter name="EndSignalRoute">' + esc(route)
                + "</ep:elementParameter>")

    if outcomes:
        text = re.sub(
            r'<ep:elementParameter name="EndSignalRoute">(.*?)</ep:elementParameter>',
            fill, text, flags=re.S)
        changed.append(f"прикладів відповіді {filled}")

    path.write_bytes(text.encode("utf-8"))
    print("додано: " + (", ".join(changed) if changed else "нічого"))


if __name__ == "__main__":
    main()
