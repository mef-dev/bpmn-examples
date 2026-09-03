# tools

Every example here is built from the specification lying next to it, and held
to the rules below.

```bash
python tools/build.py                                      # rebuild every example
python tools/build.py flow-patterns/01-basics/first-flow.spec.json
python tools/verify.py                                     # check without rebuilding
```

A model you cannot regenerate can only be edited by hand, and that is how the
file and the intent drift apart. So the intent lives in `<name>.spec.json`, the
model is what the tools make of it, and `verify.py` decides whether the result
is fit to publish.

## The specification

```json
{
  "name": "first-flow",
  "documentation": "The smallest working Flow: typed input in, typed output out.",
  "config":  { "flow": "flow-patterns-config", "library": "tenant_shared", … },
  "input":   { "title": "GreetingRequest",
               "properties": { "name": "string", "language": "string" },
               "example":    { "name": "Ada", "language": "en" } },
  "types":       { "PageInfo": "public class PageInfo { … }" },
  "externalTypes": { "ChatMessage": "types://external/ai/…" },
  "libs":        { "ai": "libs://common/ai" },
  "steps": [
    { "id": "T_Compose", "name": "compose the greeting",
      "expression": "return new GreetingRequest() { … };",
      "note": "Input is what the caller sent and stays reachable for the whole process." }
  ],
  "outcomes": {
    "success": { "title": "GREETED",          "value": "{ … }" },
    "failure": { "title": "GREETING_FAILED",  "value": "{ … }" }
  }
}
```

| Field | What it decides |
|-------|-----------------|
| `documentation` | the process description; the link back to this repository is derived from the file's own path |
| `input.example` | the request shown in a comment beside the start event, so the first thing a newcomer does is run it |
| `steps[].note` | the comment beside that step — the reason for a decision belongs next to the decision |
| `steps[].raises` | the message boundary event that step raises from code, and the throw event it leads to |
| `steps[].risky` | moves the error boundary event onto that step; the code only has to throw |
| `types`, `externalTypes`, `libs` | what a step uses beyond its own input and output. A type given as text is a class declaration and is marked native; given as an object it is a JSON schema |
| `outcomes` | the response example on each end event, paired with the request by name |
| `generate: false` | the model is kept by hand and only passed through the passes. The configuration Flow is the one case: it is the source of settings, so it has no configuration of its own to call |

Two specifications in `flow-patterns/parked/` have no model: they wait on
platform capabilities (`AI/Completions` callable from a model, `IO/Local/Archive`
exposed to flows).

## The build

`gen` comes from [bpmn_forge](https://dev.azure.com/natecrd/Unibill%20Cloud%20Platform/_git/graph-api-files-sync)
and produces the skeleton — types, the typed process boundary, the error branch,
the routes, the call to the configuration Flow. Point `BPMN_FORGE` at it, or keep
that repository beside this one. Everything after `gen` is in `tools/layout`, in
this order:

```
relayout → straighten → split_shared_data → add_stores → add_types → add_examples
        → add_notes → fit_notes → place_notes → place_labels
        → place_data_labels → snap_associations
```

The order carries two decisions worth knowing. A data element's caption is
anchored under its own shape and does not move; the lines route around it, not
the other way round. And associations are drawn before comment lines, because
data is part of the contract and an explanation is what should give way.

---

The rules these examples are held to, as code you can run.

The platform compiles a model with overlapping shapes, arrows ending in empty
space, unreachable branches and silently skipped nodes exactly as happily as a
clean one. Nothing in the editor warns you. These scripts are the warning.

```bash
python tools/verify.py                     # every example in flow-patterns
python tools/verify.py path/to/model.bpmn  # just this one
```

`verify.py` returns a non-zero exit code when anything is violated, so it can go
straight into CI. Every check also runs on its own and prints its own detail —
which node, which edge — not just a count.

Python 3.11+, no dependencies outside the standard library.

## checks/

### check_rules.py — eleven readability rules

| # | Rule | Why it exists |
|---|------|---------------|
| 1 | One end event per outcome, no more | A model with an end event per branch stops showing what the outcomes actually are |
| 2 | Every data association has a `BPMNEdge` | A declared association with no edge leaves the data object floating; the reader cannot tell what produces it |
| 3 | Every exclusive gateway has a `default` path | Without one, an input nobody predicted leaves the token with nowhere to go |
| 4 | No crossing arrows | Crossings are where readers lose the thread |
| 5 | A declared type used by a task is bound to that task | Otherwise the type exists in the model and nothing on the diagram says where |
| 6 | Decisions carry a `textAnnotation` | The reason for a branch belongs next to the branch, not in a ticket |
| 7 | An input example lives in a comment | So the first thing a newcomer does is run it, not guess the shape |
| 8 | No task without a name | An unnamed box teaches nothing |
| 9 | No element the engine will not execute | See below |
| 10 | `isCollection` agrees with the `[]` in the name | A lie here is invisible until runtime |
| 11 | No data object that repeats a type already on the boundary | The start and end events already declare it, and a gateway does not change it |

**Rule 9 deserves its own paragraph.** Among *tasks*, the engine executes only
`task` and `serviceTask`. `scriptTask`, `businessRuleTask`, `userTask`,
`manualTask`, `sendTask` and `receiveTask` compile without a single warning and
are then **silently skipped** — the token moves on carrying the previous node's
result. A model built from semantically expressive task types therefore returns
whatever the last executable node produced, and looks like it passed. This was
established on a live stand by running the same model with each task type in
turn. `callActivity` is not a task and does execute.

### check_examples.py — five rules about request and response examples

1. Every end event carries at least one example.
2. Request and response examples are paired by the same name.
3. Documentation links back to the source repository.
4. Documentation is in English.
5. No duplicated request examples.

### The rest

| Script | What it catches |
|--------|-----------------|
| `check_edges.py` | An edge whose end does not reach the shape it connects. A line stopping in empty space reads as a broken model |
| `check_graph.py` | The diagram and the process disagreeing — a flow with no edge, a node with no shape |
| `check_labels.py` | Labels sitting on a line, on each other, or a data object's caption drifting away from its own shape onto a neighbour's |
| `check_inline.py` | A code insert larger than the inline editor window. Long bodies belong in a Code Action |
| `check_layout.py` | Shapes overlapping within one plane (a boundary event on its task's border is not an overlap) |
| `rule_redundant_dor.py` | Rule 11 as an importable module, so a generator can enforce it too |

## layout/

Transformation passes. Each takes a model path and rewrites it in place, so run
them on a copy or under version control.

| Script | What it does |
|--------|--------------|
| `relayout.py` | Lays the process out top to bottom, branches starting beside their source |
| `straighten.py` | Makes routes orthogonal and puts a condition label next to its gateway, along the branch it belongs to |
| `snap_associations.py` | Pulls both ends of an association onto the middle of the nearest side, so no line ends in a corner |
| `place_labels.py` | Moves labels off lines and off each other |
| `place_data_labels.py` | Puts a data element's caption under its own shape and nowhere else |
| `place_notes.py` | Positions comments near what they explain |
| `fit_notes.py` | Wraps comment text and fits the frame to it, so no line is cut off |
| `split_shared_data.py` | Gives each end event its own data element instead of one shared between them |
| `add_boundary_event.py` | The message boundary event a step raises from code, and the throw event it leads to |
| `add_stores.py` | Data stores from the `stores` block, each bound to the step that uses it — the engine ignores an unbound one |
| `add_types.py` | Types, external types and libraries a step uses beyond its own input and output |
| `add_examples.py` | Process documentation with the link back to source, and the response example on each end event |
| `add_notes.py` | The comments declared in the specification, and the input example beside the start event |
| `drop_redundant_dor.py` | Removes a data object that only repeats a type already declared on the boundary (rule 11) |
| `bind_type_reference.py` | Fills `dataObjectRefName` so the Types panel shows which data element carries each type |
| `fix_binding.py` | Rewrites Code Action arguments to the form that passes a value rather than the literal text of the expression |

**On `fix_binding.py`.** A Code Action argument written as `Input.message`
arrives in the generated method as the string `"Input.message"`. Only `#Input.x`
and `{Input.x}` substitute the value. For a string parameter this yields
nonsense; for any other type the node dies silently and the flow ends on the
previous step with no error at all.

## platform/

### fetch_generated.py — read what the model actually became

```bash
export MEFDEV_BASIC=<login>:<password>     # or MEFDEV_APIKEY=<token>
python tools/platform/fetch_generated.py --stand http://localhost:5000 2113 1
python tools/platform/fetch_generated.py --stand http://localhost:5000 2113 1 --grep Boundary
```

Between a `<task>` in the diagram and the line that threw stands a code
generator. Until you have read its output, every explanation of a failure is a
guess. This pulls the generated C# for a published model, so you can see which
calls the node became, under which key a boundary event was registered, and
which arguments a Code Action really received.

Make it the first step after any engine error, not the last.
