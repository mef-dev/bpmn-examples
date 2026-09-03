"""Прив'язує параметри Code Action так, щоб доходило значення, а не текст.

Дослід на стенді: "Input.alias" приходить у код рядком "Input.alias";
значення підставляють тільки записи "{Input.alias}" та "#Input.alias";
береться другий, бо він же передає обʼєкти (#Previous), а не лише текст.
Для рядкового параметра це давало сміття, для HttpResponse і int — тихо
вбивало вузол: flow завершувався попереднім кроком без жодної помилки.
"""
import html
import json
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                    else pathlib.Path(__file__).with_name("sse-test11-semantic.bpmn"))
text = path.read_text(encoding="utf-8")


def esc(value):
    return html.escape(json.dumps(value, ensure_ascii=False), quote=False)


def bind(expr):
    if not isinstance(expr, str):
        return expr
    if expr.startswith(("#", "{")):
        return expr
    if re.match(r"^(Input|Parameters|Global)\b", expr):
        return "#" + expr
    return expr


fixed = []


def patch(match):
    impl = json.loads(html.unescape(match.group(2)))
    if impl.get("actionType") == "Action" and isinstance(impl.get("actionParam"), dict):
        before = dict(impl["actionParam"])
        impl["actionParam"] = {k: bind(v) for k, v in before.items()}
        changed = {k: (before[k], impl["actionParam"][k])
                   for k in before if before[k] != impl["actionParam"][k]}
        if changed:
            fixed.append((match.group(1), changed))
    return f'{match.group(1)}{esc(impl)}{match.group(3)}'


text = re.sub(
    r'(<ep:elementParameter name="ElementImplementation">)(.*?)(</ep:elementParameter>)',
    patch, text, flags=re.S)

path.write_bytes(text.encode("utf-8"))
for _, changed in fixed:
    for key, (was, now) in changed.items():
        print(f"  {key}: {was}  ->  {now}")
print(f"вузлів виправлено: {len(fixed)}")
