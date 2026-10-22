# 06 · Reading a response as a stream

Some answers arrive over time. Reading them line by line, and passing each line
on as it lands, keeps memory flat and lets the caller see progress.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| A built-in function as a step | `open the stream` (`T_Call`): `actionType: Function`, `action: RestApi/GET` |
| Every declared argument, `Timeout` included | the `actionParam` of `open the stream` |
| Credentials taken from the configuration | `Login` and `Password`, read from `Parameters.config` |
| `#Previous.Reader` — the open response body | `read the stream line by line` (`T_Stream`), the `while` loop |
| Passing each chunk out through an event | `Action.BoundaryEvents["Event_Chunk"].Raise(line)` |
| A non-interrupting boundary event | `chunk` (`Event_Chunk`), `cancelActivity="false"` |

## The model

```
start → Get Config → Parse Config → open the stream → read the stream line by line → end
            ↓             ↓               ↓                    │
            │             │               │          (chunk, non-interrupting)
            │             │               │                    ↓
            │             │               │          send the chunk on
            └─────────────┴───────────────┴──→ handle Exception → end
```

`send the chunk on` (`Event_Send`) passes each line to `Server-side events`, the
platform's server-sent events channel: a client subscribed to it over HTTP
receives the lines as they are read.

`Get Config` calls the Flow `bpmn-examples-config`: the file
[`03-config-as-flow/bpmn-examples-config.bpmn`](../03-config-as-flow/bpmn-examples-config.bpmn),
imported into the tenant library `bpmn_examples`.

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `StreamRequest` | inner, JSON Schema | the process boundary; `Input.topic` selects what to ask for |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure |
| `ExternalConfig` | external | supplies `listUrl`, `login` and `password` |

`HttpResponse` is not declared by you: it is the result type of the `RestApi`
function, and `.Reader` is its open body. Nothing in the model holds the whole
answer at once.

## What you should get back

```
{ "topic": "USD" }   →   HTTP 200
{"topic":"USD"}
```

The reply is the request handed back: what matters happens on the way. Every
non-blank line of the answer leaves through `Event_Chunk` as it is read, and the
branch behind it passes the line to `Server-side events`, where a subscriber
receives it. Add `debug=true` to the start call and the trace shows one
transition out of `Event_Chunk` per line, while `T_Stream` is still running.

When the installation cannot reach the endpoint, the call fails and the error
branch answers — the example working correctly, because an unreachable endpoint
is a failure and the failure has a path:

```
{"levelMessage":"11","statusCode":500,
 "message":"Error while try to call action 'T_Call/open the stream'","state":"1"}
```

With `debug=true` the reply also carries `parametersContainer`, where the
resolved configuration is visible:

```json
"config": { "ratesUrl": "https://api.frankfurter.dev/v1",
            "listUrl": "https://jsonplaceholder.typicode.com/posts",
            "login": "", "password": "", "pageSize": 10,
            "language": "en", "cacheSeconds": 300 }
```

Use that when a Flow behaves as if it had no settings: it tells you whether the
configuration arrived or the call itself is at fault.

**Each `Raise` starts its own branch of execution.** That is fine for the lines
of an answer; for a long token stream, send in batches.

## Why it is built this way

**Every declared argument is passed, `Timeout` included.** The engine inlines the
function's body into your model, and that body names each declared parameter. Omit
`Timeout` and the name binds to the type `System.Threading.Timeout` instead, so
the compiler answers `'Timeout' is a type, which is not valid in the given
context` — pointing at code you never wrote.

**The credentials come from the configuration, and are empty.** A public source
needs none. When a real one does, exactly one file changes.

**Chunks leave through an event, not through the return value.** A returned
collection would mean waiting for the last line before anything moves.

## Where newcomers stumble

- **Reading the body twice.** `.Reader` is a stream: once consumed, it is gone.
  Keep what you need as you pass.
- **Expecting the lines in the reply.** The lines go to subscribers through
  `Event_Chunk`; the reply is only the request handed back. If the caller also
  needs a summary, build it in `read the stream line by line` and return it.
- **Blank lines.** Streamed protocols use them as separators; the loop skips them
  rather than raising empty events.

## How the platform delivers the chunks

`send the chunk on` is a message throw event to Server-Sent Events. The channel
and how events reach the engine through ServiceHost and the message broker are
described in the BPMN Low-Code guide, sections *Message events* and
*Event-based implementation: ServiceHost and the message broker* (part of
durable execution). See [BPMN Low-Code overview](https://platform.mef.dev/bpmn_lowcode/bpmn_lowcode_overview.md).

## Run it

Follow [Before you start](../README.md#before-you-start) for this file: IMPORT BPMN →
Save as into your Personal library → Compile → Publish into `bpmn_examples`.
Then Build → Execute → **Example** → Run with `{"topic":"USD"}`. It compiles
anywhere; whether it *runs* depends on your installation reaching
`jsonplaceholder.typicode.com`.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
