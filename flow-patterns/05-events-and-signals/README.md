# 05 · Events and signals

Two different things that are easy to confuse: a **signal** is heard by everyone subscribed to it; a **message** goes to a single recipient. And, separately, how to raise an event from code.

## When to use

Assembling a result from parts, coordinating parallel branches, "continue when it arrives".

## Files

| File | What it shows |
|---|---|
| `zip-chunks.bpmn` | parallel gateway fork/join, signal `AllPagesCompleted` versus message `PageNCompleted`, event-based gateway in a wait loop, ordering of the parts |
| `boundary-event-fanout.bpmn` | **`Action.BoundaryEvents["…"].Raise(payload)`** — raising a boundary event from code; non-interrupting boundary event |

## Platform functions used

`RestApi/GET`

## Reserved words

**`Action.BoundaryEvents[].Raise()`** · `#event.Data` · `#Previous["node-name"]` · `Parameters.Clone()` · `Transition`

## What to watch for

- **`Action.BoundaryEvents["Event_X"].Raise(x)`** — the main point of this group:
  this is how the code of a task raises the boundary event attached to it. The name
  in brackets is the `id` of the event in the diagram.
- A boundary event with `cancelActivity="false"` does **not** interrupt the task: the
  task keeps running and the event branch runs in parallel. That is exactly what a
  fan-out needs.
- After a parallel gateway, `#Previous` is a dictionary. Address it as
  `#Previous["node-name"]`, otherwise you get the dictionary instead of the object.
- `Parameters.Clone()` gives a branch its own copy of the state; without it, two
  branches write into the same one.

---
For the data types in these examples, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
