# 01 · Basics: how data moves through a Flow

The smallest Flow that still does something real: it takes typed input, passes it
through one step, and returns typed output.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| A typed process boundary | the start and end events, each tied to a data element |
| `Input` — what the caller sent | `T_Compose`, first line |
| `#Previous` — the previous step's result | `Parse Config` (`T_ParseConfig`), which casts it |
| Settings taken from a separate Flow | `Get Config` (`CA_Config`): a Call Activity that runs the configuration Flow `bpmn-examples-config` ([03 · Configuration](../03-config-as-flow/)) |
| An error path drawn on the diagram | the boundary error events on `Get Config` and `Parse Config`, both leading to `handle Exception` |
| Writing to the run log | `Logger.LogInformation` in `compose the greeting` |

## The model

```
start → Get Config → Parse Config → compose the greeting → end
            ↓             ↓ (on error)
            └─────────────┴──→ handle Exception → end
```

`Get Config` calls the Flow `bpmn-examples-config`: the file
[`03-config-as-flow/bpmn-examples-config.bpmn`](../03-config-as-flow/bpmn-examples-config.bpmn),
imported into the tenant library `bpmn_examples`.
`Parse Config` casts its answer into `Parameters.config`. Every model in this
repository starts with these two steps; your own work begins after them.

`handle Exception` (id `T_HandleException`) calls the Code Action
`HandleException`, which builds the `ErrorResponse`; [02 · Errors](../02-error-handling/)
explains it.

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `GreetingRequest` | inner, JSON Schema | the process boundary: the start event accepts it, the end event returns it. `Input.name` and `Input.language` are its fields |
| `ErrorResponse` | inner, JSON Schema | what `HandleException` returns, so a failure has a shape too |
| `ExternalConfig` | external → `types://external/ConfigActivity/Config` | the configuration type, declared **once** in `bpmn-examples-config` and only referenced here |

`ExternalConfig` is the one worth pausing on. This file never repeats the fields
of the configuration; it points at the Flow that owns them. Change the shape
there and every consumer sees the change, instead of each keeping a stale copy.

## What you should get back

Build → Execute, **Parameters**:

```
{ "name": "Ada", "language": "en" }
```

The answer:

```
{"name":"Ada","language":"en"}
```

With an empty `name` the reply is `{"name":"world","language":null}` — the step
substitutes the default. The run log shows one line: `greeting Ada`.

## Why it is built this way

**The settings come from another Flow, not from this file.** The first two steps
call `bpmn-examples-config` and cast its answer into `Parameters.config`. It looks like
ceremony in an example this small, and it is the single most important habit in
the group — see [03 · Configuration](../03-config-as-flow/) for what it buys you.

**The input is a declared type, not a loose bag.** The compiler can then tell you
that `Input.nmae` does not exist, instead of the process returning null at run
time and leaving you to guess.

**The error path exists even in the smallest Flow.** The configuration Flow can
be missing or fail, and its answer can fail to cast. Boundary error events on
both steps lead to a handler and its own end event. Without them a failure ends
the process without an answer.

## Where newcomers stumble

- **`#Previous` is the previous node's result, not the process input.** After the
  configuration steps, `#Previous` holds the configuration — not what the caller
  sent. Reach for `Input` when you mean the caller's payload.
- **A step must return something.** The body of a task is compiled into a method
  with a return type. A branch that falls off the end without `return` fails the
  whole model with `CS0161`, and the message points at generated code you cannot
  open.
- **Input and output share a type here.** That is fine for an echo. In a real
  process each step usually deserves its own type; a shared one hides the moment
  the shape actually changes.

## Run it

Follow [Before you start](../README.md#before-you-start): the tenant library
`bpmn_examples` with `bpmn-examples-config` in it. Then import this file into
the same library, compile it and start it with the input above.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
