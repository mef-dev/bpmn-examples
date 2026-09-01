# Flow patterns

Teaching examples for the MEF.DEV platform, one per problem. Each was written to
be read: small enough to hold in your head, commented in the code itself, and
compiled against the real platform before it was published here.

Every example is under the licence of this repository. None of them is a
production Flow with the names filed off — they were built for this folder.

## The groups

| Group | The one thing it teaches | Model |
|---|---|---|
| [01 · Basics](01-basics/) | `Input` is the caller's payload, `#Previous` is the last step's result | `first-flow.bpmn` |
| [02 · Errors](02-error-handling/) | a failure is a branch, and only `#PreviousData` carries the exception | `error-as-branch.bpmn` |
| [03 · Configuration](03-config-as-flow/) | settings live in their own Flow, so a model never learns its environment | `service-config.bpmn`, `use-config.bpmn` |
| [04 · Pagination](04-pagination/) | plan the pages first, then walk them with Multi Instance | `paged-fetch.bpmn` |
| [05 · Events](05-events-and-signals/) | a step can raise an event and keep working | `raise-event.bpmn` |
| [06 · Streaming](06-streaming-sse/) | read a response as it arrives, pass each chunk on | `stream-response.bpmn` |
| [07 · Triggers](07-triggers/) | the start event decides how a Flow is reached | `http-start.bpmn` |
| [08 · Agents](08-ai-agents/) | build a prompt as typed data, not as a string | `structured-prompt.bpmn` |

**Before your first Flow**, read [TYPE-DESIGN.md](TYPE-DESIGN.md). Most errors
that look like a platform failure are a skipped type-design step.

## Import the configuration Flow first

Every example takes its settings from a separate Flow through a Call Activity.
That indirection is the habit the whole group is built around: it is what lets
the same model run in any environment without an edit.

The consequence is a prerequisite. Before compiling anything else:

1. Import `03-config-as-flow/service-config.bpmn` into a **tenant** library.
2. Name it `flow-patterns-config`.
3. Compile it.

Every other model then resolves
`activities://bpmn-mnemo/tenant/<your library>/flow-patterns-config/#latest`. If
your tenant library is named something other than `tenant_shared`, change that
one segment in each model, or rename the library.

**A tenant library, not a personal one.** The platform resolves a personal
library only for the account that created it, so a `personal/…` reference works
for its author and for nobody else.

## What the examples talk to

Two public sources, no key, no account, nothing to expire:

| Source | Used for |
|---|---|
| `api.frankfurter.dev` | exchange rates published by the European Central Bank |
| `jsonplaceholder.typicode.com` | a list endpoint that understands `_start` and `_limit` |

`login` and `password` in the configuration are empty, because neither source
needs them. A real deployment fills them in that one file.

Compiling never touches the network. Running the examples that make an outbound
call does — if your stand has no route to the internet, those runs end on the
error branch, which is the correct behaviour and is shown in the group's README.

## How to read a group

Each group's README says the same four things:

- **what capabilities the example demonstrates**, and where in the file to look;
- **which types it declares** and how each one is used;
- **what you should get back** — the actual reply, taken from a real run;
- **why it is built that way**, and where newcomers usually trip.

---

Every model here compiles against the platform. The models are generated from
the platform's own function catalogue, so their declarations cannot drift from
the engine that runs them.
