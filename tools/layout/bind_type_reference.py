"""Звʼязує оголошений тип з елементом даних, який його несе.

У панелі Types колонка Reference живиться полем dataObjectRefName. Без нього
тип і його аркуш на схемі лишаються двома окремими речами: читач бачить
DataObjectReference з написом TestResult і мусить сам здогадуватись, що це той
самий TestResult зі списку типів.

Звʼязок ставиться тільки там, де він справді є: тип, для якого в моделі немає
елемента даних з таким іменем, лишається без посилання — вигадане посилання
гірше за порожнє.
"""
import html
import json
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")


def esc(value):
    return html.escape(json.dumps(value, ensure_ascii=False), quote=False)


names = {m.group(1) for m in re.finditer(
    r'<(?:\w+:)?dataObjectReference\b[^>]*\bname="([^"]+)"', text)}

m = re.search(r'<gp:globalParameter name="InnerTypes">(.*?)</gp:globalParameter>',
              text, re.S)
if not m:
    print("InnerTypes у моделі немає")
    sys.exit(0)

types = json.loads(html.unescape(m.group(1)))
bound, cleared = [], []
for it in types:
    if it.get("name") in names:
        if it.get("dataObjectRefName") != it["name"]:
            bound.append(it["name"])
        it["dataObjectRefName"] = it["name"]
    elif "dataObjectRefName" in it:
        # посилання на елемент даних, якого в моделі вже немає
        cleared.append(f"{it['name']} -> {it.pop('dataObjectRefName')}")

text = text.replace(m.group(0), '<gp:globalParameter name="InnerTypes">'
                    + esc(types) + "</gp:globalParameter>", 1)
path.write_bytes(text.encode("utf-8"))

unbound = [it["name"] for it in types if "dataObjectRefName" not in it]
if bound:
    print("  звʼязано:", ", ".join(bound))
if cleared:
    print("  знято мертві посилання:", ", ".join(cleared))
if unbound:
    print("  без елемента даних, тому без посилання:", ", ".join(unbound))
print(f"{path.name}: типів {len(types)}, зі звʼязком {len(types) - len(unbound)}")
