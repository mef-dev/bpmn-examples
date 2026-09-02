"""Перевіряє приклади запиту й відповіді: чи є вони і чи звʼязані одним іменем.

Платформа тримає їх у двох місцях:
  StartSignalRoute.examples          — словник, ключ = імʼя прикладу запиту;
  EndSignalRoute.exampelsVariants    — список, title = імʼя прикладу відповіді.
Swagger зводить їх за цим іменем, тож розбіжність у назві мовчки розриває пару.
"""
import html
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


def local(tag):
    return tag.split("}", 1)[-1]


def load(raw):
    try:
        return json.loads(html.unescape(raw))
    except Exception:  # noqa: BLE001
        return None


path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
root = ET.fromstring(text)

request_names, response_names, ends = set(), set(), []
request_values = {}
for el in root.iter():
    if local(el.tag) != "elementParameter":
        continue
    data = load(el.text or "")
    if not isinstance(data, dict):
        continue
    if el.get("name") == "StartSignalRoute":
        for _n, _v in (data.get("examples") or {}).items():
            request_names.add(_n)
            request_values[_n] = (_v or {}).get("value")
    elif el.get("name") == "EndSignalRoute":
        titles = [v.get("title") for v in (data.get("exampelsVariants") or [])
                  if isinstance(v, dict) and v.get("title")]
        ends.append((data.get("code"), titles, data.get("producedTypeVariants")))
        response_names |= set(titles)

print(f"# {path.name}\n")
print(f"імен прикладів запиту : {sorted(request_names) or '—'}")
print(f"імен прикладів відповіді: {sorted(response_names) or '—'}")
print()

print("кінцеві події:")
empty = 0
for code, titles, produced in ends:
    mark = "" if titles else "   <- без жодного прикладу"
    empty += not titles
    print(f"   код {str(code):<5} приклади: {titles or '[]'}"
          f"   тип: {produced or '[]'}{mark}")

has_route = bool(request_names)
orphan_req = request_names - response_names
orphan_res = (response_names - request_names) if has_route else set()

print()
print(f"1. кінцевих подій без прикладу: {empty}")
print("   " + ("ОК" if not empty else "ПОРУШЕНО"))
print(f"\n2. імен запиту без пари у відповіді: {sorted(orphan_req) or '—'}")
print("   " + ("ОК" if not orphan_req else "ПОРУШЕНО")
      + ("" if has_route else "  (у Flow немає HTTP-маршруту, прикладів запиту не передбачено)"))
print("   (відповідь без пари в запиті — припустимо: не кожен наслідок "
      "спричиняється входом)")

# Однакові приклади запиту нічого не пояснюють: якщо два імені несуть той
# самий запит, одне з них зайве або відповідь до нього хибна.
seen = {}
duplicates = []
for name, value in request_values.items():
    key = " ".join((value or "").split())
    if key and key in seen:
        duplicates.append(f"{seen[key]} і {name}")
    seen[key] = name
print(f"\n5. однакових прикладів запиту: {len(duplicates)}")
for item in duplicates:
    print(f"      {item}")
print("   " + ("ОК" if not duplicates else "ПОРУШЕНО"))

docs = [d.text for d in root.iter() if local(d.tag) == "documentation" and d.text]
link = any("http" in (d or "") for d in docs)
print(f"\n3. документація: блоків {len(docs)}, посилання на джерело: "
      f"{'є' if link else 'немає'}")
print("   " + ("ОК" if link else "ПОРУШЕНО"))

non_ascii = [d.strip()[:60] for d in docs
             if any(ord(ch) > 127 for ch in (d or ""))]
print(f"\n4. документація не англійською: {len(non_ascii)}")
for item in non_ascii:
    print(f"      {item}")
print("   " + ("ОК" if not non_ascii else "ПОРУШЕНО"))
