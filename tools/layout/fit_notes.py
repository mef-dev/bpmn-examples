"""Формує рамку коментаря під його власний текст.

Дві причини, чому коментарі читалися погано:
  * проза була злита в один рядок, і переглядач ламав її де попало;
  * рамку задавали наосліп, тож власні переноси не збігалися з її шириною —
    виходили обірвані рядки на кшталт «cap.» окремо.

Тепер розмір рахується з тексту: ширина за найдовшим рядком, висота за їх
кількістю. Що написано — те й видно.

Текст береться з самої моделі, а не з цього файлу: інструмент форматує, а не
пише зміст. Проза переноситься за шириною; блок, у якому є структура (JSON,
списки), лишається з власними переносами — там кожен рядок значущий.

    python fit_notes.py <модель.bpmn> [--width 58]
"""
import argparse
import html
import pathlib
import re

CHAR_W = 6.3          # приблизна ширина символу шрифту коментаря
LINE_H = 14
PAD_X, PAD_Y = 22, 18

STRUCTURED = re.compile(r'^\s*[\[\]{}]|"\s*:')


def wrap(body, width):
    lines, current = [], ""
    for word in body.split():
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines


def reflow(raw, width):
    """Проза переноситься; структурований блок лишається як є."""
    lines = [ln.rstrip() for ln in raw.splitlines()]
    if any(STRUCTURED.search(ln) for ln in lines):
        return [ln for ln in lines if ln or lines.index(ln) != len(lines) - 1]
    return wrap(" ".join(lines), width) or [""]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("model")
    parser.add_argument("--width", type=int, default=58,
                        help="на скільки символів переносити прозу")
    args = parser.parse_args()

    path = pathlib.Path(args.model)
    text = path.read_text(encoding="utf-8")

    changed = []
    for match in re.finditer(
            r'<textAnnotation id="([^"]+)">\s*<text>(.*?)</text>', text, re.S):
        aid, raw = match.group(1), html.unescape(match.group(2))
        lines = reflow(raw, args.width)
        body = html.escape("\n".join(lines), quote=False)
        text = re.sub(
            rf'(<textAnnotation id="{aid}">\s*<text>).*?(</text>)',
            lambda m, b=body: m.group(1) + b + m.group(2),
            text, count=1, flags=re.S)
        width = max(len(line) for line in lines) * CHAR_W + PAD_X
        height = len(lines) * LINE_H + PAD_Y
        text = re.sub(
            rf'(<bpmndi:BPMNShape id="[^"]*" bpmnElement="{aid}">\s*'
            r'<omgdc:Bounds x="[-\d.]+" y="[-\d.]+" )'
            r'width="[\d.]+" height="[\d.]+"',
            lambda m, w=width, h=height: m.group(1)
            + f'width="{w:.0f}" height="{h:.0f}"',
            text, count=1)
        changed.append((aid, len(lines), max(len(x) for x in lines)))

    path.write_bytes(text.encode("utf-8"))
    print(f"коментарів переформатовано: {len(changed)}")
    for aid, count, longest in changed:
        print(f"   {aid:<14} рядків: {count:<3} найдовший: {longest} симв.")


if __name__ == "__main__":
    main()
