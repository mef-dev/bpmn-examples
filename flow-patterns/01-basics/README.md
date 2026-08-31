# 01 · Basics: the data pipeline

The smallest working Flows. They show how data enters a process, passes through the elements, and leaves — with no queues, files, or parallelism.

## When to use

Your first Flow. Or when you need to recall where `#Previous` comes from and how `Global` differs from `Parameters`.

## Files

| File | What it shows |
|---|---|
| `echo-agent.bpmn` | a minimal pipeline: start → task → end; input and output typed with the same type |
| `global-and-jsonpath.bpmn` | `JsonPath` extracts a value from the response, `SaveVariable` puts it into `Global`, and the following steps read it |

## Platform functions used

`JsonPath` · `SaveVariable` · `RestApi`

## Reserved words

`Input` · `#Previous` · `Parameters` · `Global` · `Logger`

## What to watch out for

- `SaveVariable` writes **to `Global`**, not to `Parameters`. To read it later,
  use `Global.<name>`; it stays available until the process run ends.
- `Global` is dynamic: the compiler will not see a mistake in a name, it will
  surface at run time. Name your variables once and name them consistently.
- In `echo-agent` the input and the output are the same type. That is fine for
  an echo, but in a real process each step usually has its own (see
  TYPE-DESIGN §3.1).

---
For the data types in these examples, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
