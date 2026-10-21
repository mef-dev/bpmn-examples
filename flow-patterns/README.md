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
| [09 · Files](09-files-and-archives/) | a file lives in a store, and what you hand back is a link | `archive-and-link.bpmn` |
| [10 · Idempotency](10-idempotency/) | a repeated request gets the stored answer from the distributed cache | `idempotent-request.bpmn` |

**Before your first Flow**, read [TYPE-DESIGN.md](TYPE-DESIGN.md). Most errors
that look like a platform failure are a skipped type-design step.

## Import the configuration Flow first

Every example takes its settings from a separate Flow through a Call Activity.
That indirection is the habit the whole group is built around: it is what lets
the same model run in any environment without an edit.

The consequence is a prerequisite. Before compiling anything else:

1. Import `03-config-as-flow/service-config.bpmn` into a **tenant** library.
2. Name it `bpmn-examples-config`.
3. Compile it.

Every other model then resolves
`activities://bpmn-mnemo/tenant/<your library>/bpmn-examples-config/#latest`. If
your tenant library is named something other than `bpmn_examples`, change that
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

## What was actually verified

Every model was compiled against the platform and then **started**, and the
replies below are what came back — not what the code was expected to produce.

| Model | Input | Result |
|---|---|---|
| `first-flow` | `{"name":"Ada","language":"en"}` | `{"name":"Ada","language":"en"}` |
| `error-as-branch` | `{"orderId":"ORD-1001"}` | `{"orderId":"ORD-1001"}` |
| `error-as-branch` | `{"orderId":""}`, `Accept-Language: uk` | HTTP 500, `ErrorResponse` with `"message":"Потрібно вказати orderId"` |
| `service-config` | `{}` | the settings object |
| `use-config` | `{"key":"EUR"}` | `{"key":"https://api.frankfurter.dev/v1/latest?base=EUR"}` |
| `paged-fetch` | `{"total":25}` | three `PageInfo` entries, the last one short — one Sub Process instance each, two at a time |
| `http-start` | `{"event":"order.created",…}` | the request echoed back |
| `structured-prompt` | `{"question":…,"tone":"plain"}` | two typed chat messages |
| `raise-event` | `{"jobId":"JOB-7"}` | `{"jobId":"JOB-7"}`, with a progress event per part |
| `stream-response` | `{"topic":"USD"}` | `{"topic":"USD"}`, every line passed on through `Event_Chunk` |
| `archive-and-link` | `{"note":"quarterly summary"}` | the folder and a link to the archive |
| `idempotent-request` | `{"orderId":"ORD-1001","amount":25.5}`, `x-ms-client-request-id` | first call: `cacheStatus` `Added`; the same id again: the same `confirmation`, `cacheStatus` `IsCompleted` |

Two limits still shape what these models can show, and both are outside the
diagrams:

- **An outbound call needs a stand with a route to the internet.** Without one
  the call fails and the error branch answers, which is the correct behaviour.
- **The `AI/Completions` built-in runs only a model installed on the stand.**
  It compiles and it is callable from a model, but it answers only from a
  model installed on the stand itself, not from the remote provider that
  `POST /api/v0/ai/chat/completions` uses.
  On a stand without a local chat model every call ends on the error branch.
  [08 · Agents](08-ai-agents/) stops at building the request for that reason,
  and the call itself is parked under `parked/ai-completion.spec.json` — it
  builds, passes every check, and waits for a stand that has the model.

## How to read a group

Each group's README says the same four things:

- **what capabilities the example demonstrates**, and where in the file to look;
- **which types it declares** and how each one is used;
- **what you should get back** — the actual reply, taken from a real run;
- **why it is built that way**, and where newcomers usually trip.

## The file beside each model

Next to every `<name>.bpmn` lies `<name>.spec.json`: the intent the model is
built from — the input and its example, each step with the comment that
explains it, the stores, the outcomes and their examples. The model is what a
generator makes of it, layout included, so the two cannot drift apart: a change
starts in the specification, and the model is regenerated, never edited by
hand. Read the specification when you want the decisions without the diagram
around them.

---

Every model here compiles against the platform. The models are generated from
the platform's own function catalogue, so their declarations cannot drift from
the engine that runs them.
