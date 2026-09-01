# 02 · Errors as a branch of the diagram

An error is not an interruption here. It is a path on the diagram, with its own
handler and its own typed answer.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| Boundary error event on a task | `Ev_Err_T_Validate`, attached to the validating step |
| One handler serving several tasks | two sequence flows arriving at `handle Exception` |
| `#PreviousData` — the only carrier of the exception | the handler's `actionParam` |
| A Code Action (`HandleException`) | declared in `CodeActions`, called by the handler |
| `EndSignalRoute` on the failing end event | `Ev_Failed` |
| Telling the runtime apart | `WorkflowEnvironment.RuntimeName` inside the handler |

## The model

```
start → Get Config → Parse Config → validate the order → end
                          ↓                   ↓
                          └───────────→ handle Exception → end (error)
```

Both risky steps lead into the **same** handler. That is normal: several incoming
sequence flows into one node is how BPMN says "these failures are handled alike".

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `OrderRequest` | inner, JSON Schema | the process boundary; `Input.orderId` is its only field |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure: `levelMessage`, `statusCode`, `message`, `state`. The handler fills it and it becomes the process result |
| `ExternalConfig` | external | the configuration type, owned by `service-config` |
| `PassingResult` | reserved | not declared by you — it is the type of `#PreviousData`, the wrapper that carries `Exception` |

The pairing to remember is `ErrorResponse` + `PassingResult`. One is what you
give the caller, the other is what the engine gives you.

## What you should get back

A valid order goes down the happy path:

```
{ "orderId": "A-1001" }   →   HTTP 200   {"orderId":"A-1001"}
```

An empty one takes the error branch:

```
{ "orderId": "" }
```
```
HTTP 200
{"levelMessage":"11","statusCode":500,
 "message":"Error while try to call action 'T_Validate/validate the order'",
 "state":"1"}
```

Read that second reply carefully. **The transport status is 200 while the body
says 500.** `EndSignalRoute` and `WorkflowEnvironment.Variables["StatusCode"]`
set the code the platform reports when the Flow is published behind an HTTP
route; a direct `Start` call still answers 200 and puts your `ErrorResponse` in
the body. If a caller of yours branches on the HTTP code alone, it will read a
failure as success — branch on the body.

## Why it is built this way

**The handler takes `#PreviousData`, never `#Previous`.** This is the single
detail that costs newcomers the most time. `#Previous` is the previous node's
*result* — on a failure there is no result. `#PreviousData` is the wrapper around
it, and the only place carrying the `Exception`. Feed the handler `#Previous` and
the compiler answers `Cannot implicitly convert 'System.Exception' to
'WorkflowPassingNodeResult'`, which does not obviously mean "wrong placeholder".

**The handler sets `WorkflowEnvironment.Variables["StatusCode"]` as well.** The
same Flow can run inside the platform or inside a plugin, and the two report
status differently. `WorkflowEnvironment.RuntimeName` tells them apart.

## Where newcomers stumble

- **Catching inside the code instead of on the diagram.** A `try/catch` in a task
  body hides the failure from the diagram: the process continues down the happy
  path with a half-built result. Let it throw and draw the branch.
- **One handler per task.** Tempting, and it doubles the diagram. Attach several
  boundary events to one handler until the responses genuinely differ.
- **Returning the exception text to the caller.** Note what the reply above does
  *not* contain: the message from `throw`. The handler decides once what the
  outside world is allowed to see.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `flow-patterns-config`. Then
import this file, compile it, and start it twice — with and without an
`orderId`.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
