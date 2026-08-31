# 07 · What starts a process

The same Flow can be started by an HTTP request, by a message from a queue, or by hand. This is a property of the start event, not a separate kind of process.

## When to use

Designing the entry point: route, queue, schedule.

## Files

| File | What it shows |
|---|---|
| `http-route-start.bpmn` | start event with an HTTP route: the method and the path are set directly on it |

## Platform functions used

`AI/Completions` (through a Call Activity)

## Reserved words

`Input` · `#Previous`

## What to watch for

- The HTTP route is set on the start event (`StartSignalRoute`): method +
  route. The diagram does not change because of it — what changes is the way it is called.
- Starting from a queue is a signal start event with a description of the source (topic,
  filter, mode `run` / `debug` / `async`); there is an example in `02-error-handling`.
- `DebugParamas` is the data for the Debug button; `ExecuteParamas` is for Execute. These
  are different sets, and both stay in the file, so they must hold no real data.

---
For the data types in these examples, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
