"""Забирає зі стенда C#, у який платформа перетворила модель.

Навіщо. Помилку рушія не можна читати по назвах елементів у діаграмі — між
`<task>` у BPMN і рядком, який упав, стоїть генератор коду. Поки не видно
згенерованого тексту, будь-яке пояснення збою лишається здогадкою. Цей крок
робить його фактом: видно, у які виклики перетворився вузол, під яким ключем
зареєстровано граничну подію, які аргументи справді передані в Code Action.

Приклад, заради якого це з'явилось. Виклик
`Action.BoundaryEvents["Ev_Probe"].Raise(...)` падав з NullReferenceException.
За назвами здавалося, що винна модель. У згенерованому коді видно, що вузол
реєструє подію через `WithBoundaryMessageEvent`, а гілку конвеєра рушій бере
з окремого місця — і питання одразу перемістилося з діаграми в платформу.

Маршрут:
    GET {stand}/api/v0/bpmn/flowdefinitions/{id}/{version}/Folder/{resource}
    resource = cs      згенерований C#
    resource = source  вихідний BPMN, як його зберегла платформа

Автентифікація береться з середовища, у репозиторії її немає:
    MEFDEV_BASIC=<логін>:<пароль>     або
    MEFDEV_APIKEY=<токен>

Приклади:
    python fetch_generated.py --stand http://localhost:5000 2113 1
    python fetch_generated.py --stand http://localhost:5000 2113 1 --resource source
    python fetch_generated.py --stand http://localhost:5000 2113 1 --grep Boundary
"""
import argparse
import base64
import os
import pathlib
import sys
import urllib.error
import urllib.request


def auth_header():
    basic = os.environ.get("MEFDEV_BASIC")
    if basic:
        if ":" not in basic:
            raise SystemExit("MEFDEV_BASIC очікує формат <логін>:<пароль>")
        return ("Authorization",
                "Basic " + base64.b64encode(basic.encode("utf-8")).decode("ascii"))
    apikey = os.environ.get("MEFDEV_APIKEY")
    if apikey:
        return ("apikey", apikey)
    raise SystemExit("немає доступу: задайте MEFDEV_BASIC або MEFDEV_APIKEY")


def fetch(stand, workflow_id, version, resource="cs", timeout=120):
    url = (f"{stand.rstrip('/')}/api/v0/bpmn/flowdefinitions"
           f"/{workflow_id}/{version}/Folder/{resource}")
    name, value = auth_header()
    request = urllib.request.Request(url, headers={name: value,
                                                   "Accept": "text/plain, */*"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", "replace")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("workflow_id", type=int)
    parser.add_argument("version", type=int)
    parser.add_argument("--stand", required=True,
                        help="базова адреса стенда, напр. http://localhost:5000")
    parser.add_argument("--resource", default="cs", choices=("cs", "source"))
    parser.add_argument("--out", help="куди зберегти; типово поруч із цим файлом")
    parser.add_argument("--grep", action="append", default=[],
                        help="показати рядки з цим словом і три навколо; "
                             "можна вказати кілька разів")
    args = parser.parse_args()

    status, text = fetch(args.stand, args.workflow_id, args.version, args.resource)
    if status != 200:
        print(f"HTTP {status}: {text[:400]}")
        return 1

    out = pathlib.Path(args.out) if args.out else pathlib.Path(
        f"generated-{args.workflow_id}-{args.version}.{args.resource}")
    out.write_bytes(text.encode("utf-8"))
    lines = text.splitlines()
    print(f"HTTP {status}   {len(lines)} рядків   ->   {out}")

    if not args.grep:
        return 0
    shown = set()
    for index, line in enumerate(lines):
        if not any(word in line for word in args.grep):
            continue
        for near in range(max(0, index - 3), min(len(lines), index + 4)):
            if near not in shown:
                shown.add(near)
                print(f"{near + 1:5}: {lines[near]}")
        print("      ...")
    if not shown:
        print("нічого не знайдено за: " + ", ".join(args.grep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
