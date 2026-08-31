# 02 · Errors as a separate path

Here an error does not stop the process silently — it becomes a branch of the diagram with its own result and its own HTTP code.

## When to use

Any Flow that calls an external system. That is, almost any Flow.

## Files

| File | What it shows |
|---|---|
| `event-error-routing.bpmn` | an error boundary event on two tasks → a shared handler → a separate end event with code 500 |

## Platform functions used

— (everything is done with Code Action and Expression)

## Reserved words

`#PreviousData` · `PassingResult` · `WorkflowEnvironment.RuntimeName` · `WorkflowEnvironment.Variables["StatusCode"]`

## What to watch out for

- The handler takes `#PreviousData`, not `#Previous`: it needs the wrapper with
  the `Exception` field, not the result.
- One handler for several tasks is normal practice: several incoming flows lead
  into it.
- `WorkflowEnvironment.RuntimeName` tells the mode apart (`UCP` / `Plugin`) —
  the response code is set differently in each.
- The end event has its own `EndSignalRoute` with a code; without it the client
  gets 200 for an error.

---
For the data types in these examples, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
