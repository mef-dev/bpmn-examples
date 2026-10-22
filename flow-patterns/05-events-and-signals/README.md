# 05 · Raising an event from code

A step that takes a while does not have to stay silent until it ends. It can
raise an event, and a second branch of the diagram reacts while the first keeps
working.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| **`Action.BoundaryEvents["…"].Raise(payload)`** | inside `do the work in parts` (`T_Work`) — the point of this group |
| A non-interrupting boundary event | `progress` (`Event_Progress`), with `cancelActivity="false"` |
| A message event definition on a boundary event | `messageEventDefinition` inside it |
| A second branch running alongside the main one | `progress` → `notify subscribers` (`Event_Notify`) |
| Sending the payload to subscribers | `notify subscribers`: an intermediate throw event to the platform's `Server-side events` channel |

## The model

```
start → Get Config → Parse Config → do the work in parts → end
            ↓             ↓                 │
            │             │       (progress, non-interrupting)
            │             │                 ↓
            │             │        notify subscribers
            └─────────────┴──→ handle Exception → end
```

`Get Config` calls the Flow `bpmn-examples-config`: the file
[`03-config-as-flow/bpmn-examples-config.bpmn`](../03-config-as-flow/bpmn-examples-config.bpmn),
imported into the tenant library `bpmn_examples`.

`progress` sits on the edge of the working step. Because it does **not** cancel
the step, the work continues while the lower branch runs. `notify subscribers`
passes each payload to `Server-side events`, the platform's server-sent events
channel: a client subscribed to it over HTTP receives the payloads as they are
raised.

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `JobRequest` | inner, JSON Schema | the process boundary; `Input.jobId` names the job |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure |
| `ExternalConfig` | external | the configuration type |

The event payload is a plain string here (`"part 2 of 3"`). It can be any
declared type; start with a string and give it a type once subscribers need
more than a line of text.

## What you get back

```
{ "jobId": "JOB-7" }   →   HTTP 200
{"jobId":"JOB-7"}
```

The step raises three progress events while it works, and the branch behind
the boundary event sends each one to `Server-side events`. Start the model with
`debug=true` to see them: the trace shows one transition out of
`Event_Progress` per part, while `T_Work` is still running. The run log has one
line per part: `part 1 done`, `part 2 done`, `part 3 done`.

## Why it is built this way

**`cancelActivity="false"` is what makes it a fan-out.** An interrupting boundary
event stops the task and takes over — right for errors, wrong for progress. Turn
it off and the two branches run side by side.

**The name in brackets is the id on the diagram**, not the label. Get it wrong
and the engine raises `BoundaryEventNotFound`; the built-in functions that raise
events catch exactly that and downgrade it to a warning, so a typo can pass
unnoticed.

**The event carries data.** `Raise(payload)` hands the branch something to work
with; without it the branch knows only that *something* happened.

## Where newcomers stumble

- **The answer comes from the main branch only.** The progress branch ends at
  `notify subscribers` and adds nothing to the reply; the caller gets the result
  of `do the work in parts`.
- **A signal is not a message.** A signal is heard by everyone subscribed; a
  message goes to one recipient. The boundary event here is a message.
- **`Parameters.Clone()` when branches write.** Two branches sharing one
  parameter object write over each other. Give a branch its own copy if it
  mutates state.

## Run it

Follow [Before you start](../README.md#before-you-start). Then import this file
into the same library and compile it. Watch the run log, not only the reply.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
