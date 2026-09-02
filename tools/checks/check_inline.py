"""Шукає вбудований код, який переріс вікно Inline.

Довга вставка в Inline не має ні імені, ні підпису, ні типів — її не видно
з переліку Code Actions, не можна перевикористати й важко читати у вузькому
вікні. Такий код має стати Code Action: із назвою, типізованими параметрами
й типізованим поверненням. Саме це й змушує назвати дані типами.
"""
import html
import json
import pathlib
import re
import sys

MAX_LINES = 15
MAX_CHARS = 700


def local(tag):
    return tag.split("}", 1)[-1]


total = 0
for path in [pathlib.Path(a) for a in sys.argv[1:]]:
    text = path.read_text(encoding="utf-8")
    rows = []
    for m in re.finditer(
            r'<(task|scriptTask|serviceTask) id="([^"]+)"[^>]*>.*?'
            r'<ep:elementParameter name="ElementImplementation">(.*?)'
            r"</ep:elementParameter>", text, re.S):
        node = m.group(2)
        try:
            impl = json.loads(html.unescape(m.group(3)))
        except Exception:  # noqa: BLE001
            continue
        if impl.get("actionType") not in ("Expression", "Inline"):
            continue
        body = impl.get("action") or ""
        lines = body.count("\n") + 1
        if lines > MAX_LINES or len(body) > MAX_CHARS:
            rows.append((node, lines, len(body)))
    if rows:
        print(f"{path.name}:")
        for node, lines, size in rows:
            print(f"      {node:<24} {lines} рядків, {size} символів")
        total += len(rows)

print(f"\nвставок, що переросли вікно: {total}"
      f"   (межа: {MAX_LINES} рядків або {MAX_CHARS} символів)")
