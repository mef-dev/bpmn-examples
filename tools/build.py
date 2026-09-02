"""Збирає модель зі специфікації, що лежить поруч із нею.

    python tools/build.py flow-patterns/01-basics/first-flow.spec.json
    python tools/build.py                # усі специфікації репозиторію

Кроки одні й ті самі для кожного прикладу:

    gen        каркас зі специфікації — типи, межа процесу, гілка помилки,
               маршрути, виклик конфігураційного Flow
    relayout   зверху вниз, гілки починаються поруч зі своїм джерелом
    straighten ортогональні маршрути, підпис умови біля свого шлюзу
    split_shared_data  кожній кінцевій події — власний елемент даних
    add_types  типи, які крок вживає понад свій вхід і вихід
    add_examples  документація з посиланням на джерело і приклади відповідей
    add_notes  коментарі, оголошені в специфікації, і приклад входу
    fit_notes  рамка коментаря під його текст
    place_notes  коментар біля того, що пояснює, нічого не перекриваючи
    snap_associations  кінці асоціацій на середину сторони; чого не намальовано —
               домальовується, бо елемент даних без стрілки нічого не пояснює
    place_labels  підписи не на лініях і не одне на одному
    place_data_labels  підпис елемента даних під його власною фігурою — останнім,
               бо це правило сильніше за загальне уникання перетинів
    verify     одинадцять правил читабельності і п'ять правил прикладів

Сам `gen` живе в іншому репозиторії; шлях до нього — у змінній середовища
BPMN_FORGE, або поруч у graph-api-files-sync.
"""
import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
FORGE = pathlib.Path(os.environ.get(
    "BPMN_FORGE", REPO.parent / "graph-api-files-sync" / "Tools" / "bpmn_forge.py"))

PASSES = [
    ("relayout.py", False),
    ("straighten.py", False),
    ("split_shared_data.py", False),
    ("add_types.py", True),
    ("add_examples.py", True),
    ("add_notes.py", True),
    ("fit_notes.py", False),
    ("place_notes.py", False),
    ("place_labels.py", False),
    ("place_data_labels.py", False),
    ("snap_associations.py", False),
]


def run(args, label):
    proc = subprocess.run([sys.executable, *args], capture_output=True,
                          text=True, encoding="utf-8")
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    first = out.splitlines()[0] if out else "без виводу"
    print(f"    {label:<22} {first}")
    if proc.returncode:
        print(out)
        raise SystemExit(f"крок {label} не пройшов")


def build(spec_path):
    spec_path = pathlib.Path(spec_path).resolve()
    model = spec_path.with_name(spec_path.name.replace(".spec.json", ".bpmn"))
    print(f"\n{model.relative_to(REPO)}")

    # Конфігураційний Flow сам собі джерело налаштувань, тож `gen` його не
    # зробить: він завжди додає виклик конфігурації. Така модель ведеться
    # руками, а проходи й перевірки застосовуються до неї так само.
    generate = json.loads(spec_path.read_text(encoding="utf-8")).get("generate", True)

    if generate:
        if not FORGE.exists():
            raise SystemExit(f"генератора немає: {FORGE}\n"
                             "задайте BPMN_FORGE=<шлях до bpmn_forge.py>")
        run([str(FORGE), "gen", str(spec_path), "-o", str(model)], "gen")
    else:
        print(f"    {'gen':<22} пропущено: специфікація каже generate: false")
    for name, needs_spec in PASSES:
        args = [str(HERE / "layout" / name), str(model)]
        if needs_spec:
            args += ["--spec", str(spec_path)]
        run(args, name[:-3])
    return model


def main():
    specs = ([pathlib.Path(a) for a in sys.argv[1:]]
             or sorted(x for x in (REPO / "flow-patterns").rglob("*.spec.json")
                       if x.parent.name != "parked"))
    if not specs:
        print("специфікацій не знайдено")
        return 1

    models = [build(spec) for spec in specs]

    print("\n=== перевірка ===")
    proc = subprocess.run(
        [sys.executable, str(HERE / "verify.py"), *[str(m) for m in models]],
        capture_output=True, text=True, encoding="utf-8")
    print((proc.stdout or "") + (proc.stderr or ""))
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
