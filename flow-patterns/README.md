# Flow patterns

Teaching examples for the MEF.DEV platform, one problem per group. Each model
is small, commented on the diagram, and has been compiled and started on the
platform. The concepts behind them are described in the
[BPMN Low-Code overview](https://platform.mef.dev/bpmn_lowcode/bpmn_lowcode_overview.md).

## The groups

Ten groups, eleven models: group 03 has two.

| Group | The one thing it teaches | Model |
|---|---|---|
| [01 · Basics](01-basics/) | `Input` is the caller's payload, `#Previous` is the last step's result | `first-flow.bpmn` |
| [02 · Errors](02-error-handling/) | a failure is a branch: HTTP 500 and the text in the caller's language (`Accept-Language`, then the installation's language) | `error-as-branch.bpmn` |
| [03 · Configuration](03-config-as-flow/) | settings live in their own Flow, so a model never learns its environment | `bpmn-examples-config.bpmn` (required by every group), `use-config.bpmn` |
| [04 · Pagination](04-pagination/) | plan the pages first, then walk them with Multi Instance; on an API, `offset`/`limit` and `Content-Range` | `paged-fetch.bpmn` |
| [05 · Events](05-events-and-signals/) | a step can raise an event and keep working | `raise-event.bpmn` |
| [06 · Streaming](06-streaming-sse/) | read a response as it arrives, pass each chunk on | `stream-response.bpmn` |
| [07 · Triggers](07-triggers/) | the start event decides how a Flow is reached | `http-start.bpmn` |
| [08 · Agents](08-ai-agents/) | build a prompt as typed data, not as a string | `structured-prompt.bpmn` |
| [09 · Files](09-files-and-archives/) | a file lives in a store, and what you hand back is a link | `archive-and-link.bpmn` |
| [10 · Idempotency](10-idempotency/) | a repeated `x-ms-client-request-id` gets the stored answer from the distributed cache; HTTP 201, 400, 409, 503 | `idempotent-request.bpmn` |

**Before your first Flow**, read [TYPE-DESIGN.md](TYPE-DESIGN.md). Most errors
that look like a platform failure are a skipped type-design step.

## Before you start

You need an account on a MEF.DEV installation with permission to create tenant
libraries.

Every model is imported under its file name: `first-flow.bpmn` becomes the
Flow `first-flow`.

1. Create a **tenant** library named `bpmn_examples`.
2. Import [`03-config-as-flow/bpmn-examples-config.bpmn`](03-config-as-flow/bpmn-examples-config.bpmn)
   into it and compile it.
3. Import the model you want into the same library and compile it.
4. Start it from the designer, or through the API:

   ```
   POST https://<host>/api/v0/bpmn/flowdefinitions/tenant/bpmn_examples/<flow>/Start.json?run=auto
   Content-Type: application/json

   <the example input from the group's README>
   ```

## Which model depends on which

```mermaid
flowchart LR
  subgraph lib["tenant library bpmn_examples"]
    direction LR
    cfg["<b>bpmn-examples-config</b><br/>03-config-as-flow/bpmn-examples-config.bpmn"]
    m01["first-flow<br/>01-basics"]
    m02["error-as-branch<br/>02-error-handling"]
    m03["use-config<br/>03-config-as-flow"]
    m04["paged-fetch<br/>04-pagination"]
    m05["raise-event<br/>05-events-and-signals"]
    m06["stream-response<br/>06-streaming-sse"]
    m07["http-start<br/>07-triggers"]
    m08["structured-prompt<br/>08-ai-agents"]
    m09["archive-and-link<br/>09-files-and-archives"]
    m10["idempotent-request<br/>10-idempotency"]
  end
  subgraph platform["built into the platform"]
    ai["library libs://common/ai"]
    rest["function RestApi/GET"]
    file["function IO/Local/File,<br/>Folder and File stores"]
    sse["Server-side events"]
    cache["distributed cache<br/>IDistributedCache"]
  end
  m01 & m02 & m03 & m04 & m05 --> cfg
  m06 & m07 & m08 & m09 & m10 --> cfg
  m08 -.-> ai
  m06 -.-> rest
  m06 -.-> sse
  m05 -.-> sse
  m09 -.-> file
  m10 -.-> cache
```

A solid arrow: the model calls `bpmn-examples-config` in its step `Get Config`
and takes the type `Config` from it, so `bpmn-examples-config` must be imported
and compiled first. No other model depends on another one: import any of them
alone after `bpmn-examples-config`. A dotted arrow: what the model uses from the
platform itself; nothing to import.

Why `bpmn-examples-config` comes first: every model begins with the step **`Get Config`**, a
Call Activity that calls the Flow `bpmn-examples-config`. Each model holds the
reference
`activities://bpmn-mnemo/tenant/bpmn_examples/bpmn-examples-config/#latest`; a
model compiles only when that Flow exists under exactly that library and name.

| You see | It is |
|---|---|
| `Get Config` | the step in every model that calls the configuration Flow |
| `bpmn-examples-config` | the configuration Flow: file `03-config-as-flow/bpmn-examples-config.bpmn` |
| `bpmn_examples` | the tenant library all models live in |
| `ConfigActivity` | the alias under which each model refers to `bpmn-examples-config` (`UsedLibs`) |
| `ExternalConfig` | in each model, the configuration type `Config` declared in `bpmn-examples-config` |

To use another library name, edit the `ExternalDefinitionLink` parameter of
`Get Config` in each model you import.

**A tenant library, not a personal one.** A personal library is visible only to
the account that created it, so a `personal/…` reference works for its author
and for nobody else.

## Terms

| Term | Meaning |
|---|---|
| Flow | a BPMN model the platform compiles and runs |
| installation | one deployment of the MEF.DEV platform |
| tenant library | a library shared by every account of the tenant; Flows find each other there by name |
| Call Activity | a step that runs another Flow and returns its answer |
| `Input` | the request payload the Flow was started with |
| `#Previous` | the result of the step just before |
| `#PreviousData` | what the engine hands to an error handler: the failed step's exception |
| `Parameters` | variables that live for one run of the Flow and are visible to every step |
| boundary error event | the small circle on a step's edge; when the step fails, the run follows its arrow |
| Code Action | a C# function declared once in the model and called from its steps |
| Multi Instance | a Sub Process run once per element of a collection |
| published plugin | a Flow published as an HTTP endpoint of a plugin |
| `UsedLibs` | the model's list of other Flows and libraries it refers to, each under an alias |

## What the examples talk to

Two public sources, no key, no account, nothing to expire:

| Source | Used for |
|---|---|
| `api.frankfurter.dev` | exchange rates published by the European Central Bank |
| `jsonplaceholder.typicode.com` | a list endpoint that understands `_start` and `_limit` |

`login` and `password` in the configuration are empty, because neither source
needs them. A real deployment fills them in that one file.

Compiling never touches the network. Running the examples that make an outbound
call does: without a route to the internet those runs end on the error branch,
which is the correct behaviour and is shown in the group's README.

## Expected results

Each model started with its example input answers:

| Model | Input | Result |
|---|---|---|
| `first-flow` | `{"name":"Ada","language":"en"}` | `{"name":"Ada","language":"en"}` |
| `error-as-branch` | `{"orderId":"ORD-1001"}` | `{"orderId":"ORD-1001"}` |
| `error-as-branch` | `{"orderId":""}`, `Accept-Language: uk` | HTTP 500, `ErrorResponse` with `"message":"Потрібно вказати orderId"` |
| `bpmn-examples-config` | `{}` | the settings object (`Config`) |
| `use-config` | `{"key":"EUR"}` | `{"key":"https://api.frankfurter.dev/v1/latest?base=EUR"}` |
| `paged-fetch` | `{"total":25}` | three `PageInfo` entries, the third for rows 21–25 — one Sub Process instance each, two at a time |
| `http-start` | `{"event":"order.created",…}` | the request echoed back |
| `structured-prompt` | `{"question":…,"tone":"plain"}` | two typed chat messages |
| `raise-event` | `{"jobId":"JOB-7"}` | `{"jobId":"JOB-7"}`, with a progress event per part |
| `stream-response` | `{"topic":"USD"}` | `{"topic":"USD"}`, every line passed on through `Event_Chunk` |
| `archive-and-link` | `{"note":"quarterly summary"}` | the folder and a link to the archive |
| `idempotent-request` | `{"orderId":"ORD-1001","amount":25.5}`, `x-ms-client-request-id` | first call: HTTP 201, `cacheStatus` `Added`; the same id again: HTTP 201, the same `confirmation`, `cacheStatus` `IsCompleted`; no header: HTTP 400 |

Two conditions are outside the diagrams:

- **An outbound call needs a route to the internet.** Without one the call
  fails and the error branch answers.
- **`AI/Completions` needs a chat model installed on the installation itself.**
  Without one, the call ends on the error branch.
  [08 · Agents](08-ai-agents/) therefore stops at building the request.

## How to read a group

Each group's README says the same four things:

- **what capabilities the example demonstrates**, and where in the file to look;
- **which types it declares** and how each one is used;
- **what you should get back** for the example input;
- **why it is built that way**, and where newcomers usually trip.

## The file beside each model

Next to every `<name>.bpmn` lies `<name>.spec.json`: the model's intent — the
input and its example, each step with the comment that explains it, the stores,
the outcomes and their examples. The models were generated from these
specifications; `bpmn-examples-config.bpmn` is kept by hand (`"generate": false`). Read the specification
when you want the decisions without the diagram around them.
