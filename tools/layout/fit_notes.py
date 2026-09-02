"""Форматує текст коментарів і підганяє рамку під нього.

Дві причини, чому попередній вигляд читався погано:
  * приклад входу був злитий в один рядок, тож переглядач ламав йогоде попало;
  * рамку я задавав наосліп, і власні переноси не збігалися з її шириною —
    виходили обірвані рядки на кшталт «cap.» окремо.

Тепер розмір рахується з тексту: ширина за найдовшим рядком, висота за їх
кількістю. Що написано — те й видно.
"""
import html
import json
import pathlib
import re
import sys

CHAR_W = 6.3          # приблизна ширина символу шрифту коментаря
LINE_H = 14
PAD_X, PAD_Y = 22, 18
WRAP = 58             # на скільки символів переносити прозу

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

# Приклад входу, який лягає в коментар біля старту. Адреса й облікові дані —
# заповнювачі: у прикладі має бути видно форму запиту, а не чийсь стенд.
EXAMPLE = {
    "URL": "http://localhost:9010",
    "login": "api_user",
    "password": "***",
    "alias": "bss",
    "pluginname": "BSS.Entities",
    "message": "OK",
    "inputMessage": ["stop"],
}

PROSE = {
    "An_Read": "The wait ends on the stop word, a deadline or a line cap. "
               "Without the last two the read blocks forever when the stop "
               "word never arrives.",
    "An_Raise": "Raise is what this test exercises. It is guarded because the "
                "engine throws inside it in the current build; the verdict "
                "reports whether it worked.",
    "An_Verdict": "success = the posted message came back through the SSE "
                  "channel. Everything else is failed, with a reason.",
}


def wrap(body, width=WRAP):
    lines, cur = [], ""
    for word in body.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines


bodies = {"An_Input": ["Example input:"]
          + json.dumps(EXAMPLE, indent=2, ensure_ascii=False).splitlines()}
for aid, body in PROSE.items():
    bodies[aid] = wrap(body)

changed = 0
for aid, lines in bodies.items():
    body = "\n".join(lines)
    escaped = html.escape(body, quote=False)
    new_text, n = re.subn(
        rf'(<textAnnotation id="{aid}">\s*<text>).*?(</text>)',
        lambda m, b=escaped: m.group(1) + b + m.group(2),
        text, flags=re.S)
    if not n:
        continue
    text = new_text
    width = max(len(line) for line in lines) * CHAR_W + PAD_X
    height = len(lines) * LINE_H + PAD_Y
    text = re.sub(
        rf'(<bpmndi:BPMNShape id="[^"]*" bpmnElement="{aid}">\s*<omgdc:Bounds '
        r'x="[-\d.]+" y="[-\d.]+" )width="[\d.]+" height="[\d.]+"',
        lambda m, w=width, h=height: m.group(1)
        + f'width="{w:.0f}" height="{h:.0f}"',
        text, count=1)
    changed += 1

path.write_bytes(text.encode("utf-8"))
print(f"коментарів переформатовано: {changed}")
for aid, lines in bodies.items():
    print(f"   {aid:<12} рядків: {len(lines):<3} найдовший: "
          f"{max(len(x) for x in lines)} симв.")
