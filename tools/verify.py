"""Run every readability and example check over the models in this repository.

This is the one command worth wiring into CI:

    python tools/verify.py                    # all examples
    python tools/verify.py path/to/model.bpmn # just these

Each check lives in tools/checks and can be run on its own; this only collects
them, reads their summary lines, and returns a non-zero exit code when anything
is violated. The checks print their own detail, so a failing run tells you which
node or which edge, not just a count.

What is checked, and why each rule exists:

  layout      shapes do not overlap, arrows do not cross, every edge actually
              reaches the shape it connects (a line ending in empty space reads
              as a broken model, and reviewers stop trusting the diagram)
  labels      no label sits on top of a line or another label, and a data
              object's caption stays under its own shape (a caption that drifts
              is read as belonging to the neighbour)
  graph       the diagram and the process agree: every flow has an edge, every
              node has a shape
  rules       eleven readability rules, among them: one end event per outcome,
              every exclusive gateway has a default path, every declared type
              used by a task is bound to it, no task without a name, no element
              the engine cannot execute, and no data object that merely repeats
              a type already declared on the process boundary
  examples    five rules about the request/response examples: every end event
              carries one, request and response examples are paired by name, no
              duplicated request examples, documentation links back to source,
              documentation is in English
  inline      no code insert larger than the inline editor window; long bodies
              belong in a Code Action

The engine will not tell you when any of this is wrong. It compiles a model with
overlapping shapes and unreachable branches just as happily as a clean one.
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
CHECKS = HERE / "checks"
EXAMPLES = HERE.parent / "flow-patterns"

# Each check reports its outcome in one of two shapes: a counted summary line,
# or an explicit verdict word per rule. Both are matched here so that adding a
# rule to a check does not need a change in this file.
COUNTED = [
    re.compile(r"обірваних кінців:\s*(\d+)"),
    re.compile(r"розбіжностей у графі:\s*(\d+)"),
    re.compile(r"із накладанням:\s*(\d+)"),
    re.compile(r"підписів елементів даних не на місці:\s*(\d+)"),
    re.compile(r"вставок, що переросли вікно:\s*(\d+)"),
    re.compile(r"справжніх накладань:\s*(\d+)"),
]
VERDICT = re.compile(r"^\s*ПОРУШЕНО", re.M)

PER_MODEL = ["check_rules.py", "check_examples.py", "check_graph.py",
             "check_labels.py"]
OVER_ALL = ["check_edges.py", "check_inline.py", "check_layout.py"]


def run(script, paths):
    proc = subprocess.run(
        [sys.executable, str(CHECKS / script), *[str(p) for p in paths]],
        capture_output=True, text=True, encoding="utf-8", cwd=str(CHECKS))
    output = (proc.stdout or "") + (proc.stderr or "")
    failures = len(VERDICT.findall(output))
    for pattern in COUNTED:
        failures += sum(int(n) for n in pattern.findall(output))
    return failures, output


def main():
    models = ([pathlib.Path(a).resolve() for a in sys.argv[1:]]
              or sorted(EXAMPLES.rglob("*.bpmn")))
    if not models:
        print("no models found")
        return 1

    total = 0
    report = []
    for model in models:
        for script in PER_MODEL:
            failures, output = run(script, [model])
            total += failures
            if failures:
                report.append((model.name, script, output))
    for script in OVER_ALL:
        failures, output = run(script, models)
        total += failures
        if failures:
            report.append(("all models", script, output))

    for name, script, output in report:
        print(f"\n===== {name} :: {script} =====")
        print(output.rstrip())

    print(f"\nmodels checked: {len(models)}   violations: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
