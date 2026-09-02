"""Звіряє incoming/outgoing вузлів із самими sequenceFlow."""
import pathlib
import sys
import xml.etree.ElementTree as ET


def local(tag):
    return tag.split("}", 1)[-1]


root = ET.fromstring(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))

flows = {}
for el in root.iter():
    if local(el.tag) == "sequenceFlow":
        flows[el.get("id")] = (el.get("sourceRef"), el.get("targetRef"))

bad = 0
for el in root.iter():
    node = el.get("id")
    if not node:
        continue
    for kind in ("incoming", "outgoing"):
        for ref in el.findall(f"{{*}}{kind}"):
            fid = (ref.text or "").strip()
            if fid not in flows:
                print(f"   {node}: {kind} -> {fid} — такого потоку немає")
                bad += 1
                continue
            src, dst = flows[fid]
            expect = dst if kind == "incoming" else src
            if expect != node:
                print(f"   {node}: {kind} {fid} веде до {expect}, не сюди")
                bad += 1

for fid, (src, dst) in flows.items():
    for end, kind in ((src, "outgoing"), (dst, "incoming")):
        el = next((e for e in root.iter() if e.get("id") == end), None)
        if el is None:
            print(f"   потік {fid}: вузол {end} не існує")
            bad += 1
        elif not any((r.text or "").strip() == fid
                     for r in el.findall(f"{{*}}{kind}")):
            print(f"   вузол {end} не оголошує {kind} {fid}")
            bad += 1

print(f"розбіжностей у графі: {bad}")
