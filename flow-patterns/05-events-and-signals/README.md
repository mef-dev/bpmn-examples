# 05 · Raising an event from code

A step that takes a while does not have to stay silent until it ends. It can
raise an event, and a second branch of the diagram reacts while the first keeps
working.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| **`Action.BoundaryEvents["…"].Raise(payload)`** | inside `T_Work` — the point of this group |
| A non-interrupting boundary event | `Event_Progress`, with `cancelActivity="false"` |
| A message event definition on a boundary event | `messageEventDefinition` inside it |
| A second branch running alongside the main one | `T_Report` → `Ev_Reported` |
| `#event.Data` — the payload that was raised | the log line in `T_Report` |

## The model

```
start → Get Config → Parse Config → do the work in parts → end
                                            │
                                    (progress, non-interrupting)
                                            ↓
                                    report the progress → end
```

The bar under the working step is the boundary event. Because it does **not**
cancel the activity, the work continues while the lower branch runs.

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `JobRequest` | inner, JSON Schema | the process boundary; `Input.jobId` names the job |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure |
| `ExternalConfig` | external | the configuration type |

The event payload itself is a plain string here (`"part 2 of 3"`). It can be any
declared type — the reporting branch reads it as `#event.Data`. Start with a
string and give it a type once the branch does more than log.

## What you get back today

**This example does not run on the current platform build.** It compiles, the
diagram is correct, and the call fails:

```
{ "jobId": "job-7" }   →   HTTP 200, state "Error"
```
```
T_Work: System.NullReferenceException
  at Natec.Workflow.TransitionBoundaryEvent.Raise(Object payload)
     TransitionBoundaryEvent.cs:line 22
```

The cause is in the engine, not in the model. `Raise` reads the conveyor branch
it was constructed with:

```csharp
// TransitionBoundaryEvent.cs:22
var cct = _workflowConveyorBranch.ChainCancellationToken;
```

That branch comes from `BoundaryEventsList.ConveyorBranch`, an `AsyncLocal`
value — and the only two lines in the whole engine that would set it are
commented out:

```csharp
// WorkflowItemTaskCodeAction.cs:101-103
//BoundaryEvents.ConveyorBranch = workflowConveyorBranch;
result.Result = Action.Invoke(...);
//BoundaryEvents.ConveyorBranch = null;
```

So the value is always null, and any `Raise` from a task body throws. Nothing a
diagram can do works around it.

**When the engine sets that value again**, this model answers as designed: three
progress events, the reporting branch logging each one, and the process ending
on whichever branch finishes last. The run log is where the work shows —
`part 1 done` … `progress reported: part 1 of 3` and so on.

The example is kept because it is the correct way to write this, and because the
failure is worth being able to recognise: an unexplained
`NullReferenceException` inside `Raise` means the engine, not your code.

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

- **Two end events mean two answers.** As above: join the branches if the caller
  should get the main result.
- **A signal is not a message.** A signal is heard by everyone subscribed; a
  message goes to one recipient. The boundary event here is a message.
- **`Parameters.Clone()` when branches write.** Two branches sharing one
  parameter object write over each other. Give a branch its own copy if it
  mutates state.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `flow-patterns-config`. Then
import this file and compile it. Watch the run log, not only the reply.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
