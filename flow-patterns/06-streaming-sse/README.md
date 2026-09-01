# 06 · Reading a response as a stream

Some answers arrive over time. Reading them line by line, and passing each line
on as it lands, keeps memory flat and lets the caller see progress.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| A built-in function as a step | `T_Call`, `actionType: Function`, `action: RestApi` |
| Every declared argument, `Timeout` included | the `actionParam` of `T_Call` |
| Credentials taken from the configuration | `Login` and `Password`, read from `Parameters.config` |
| `#Previous.Reader` — the open response body | `T_Stream`, the `while` loop |
| Passing each chunk out through an event | `Action.BoundaryEvents["Event_Chunk"].Raise(line)` |
| A non-interrupting boundary event | `Event_Chunk`, `cancelActivity="false"` |

## The model

```
start → Get Config → Parse Config → open the stream → read line by line → end
                                                             │
                                                     (chunk, non-interrupting)
                                                             ↓
                                                    send the chunk on → end
```

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `StreamRequest` | inner, JSON Schema | the process boundary; `Input.topic` selects what to ask for |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure |
| `ExternalConfig` | external | supplies `ratesUrl`, `login` and `password` |

`HttpResponse` is not declared by you: it is the result type of the `RestApi`
function, and `.Reader` is its open body. Nothing in the model holds the whole
answer at once.

## What you should get back

**On a stand that can reach the public internet**, the reading step raises one
event per non-empty line and the process ends without a body of its own — the
chunks are the output. The run log shows one `chunk out: …` line per chunk.

**On a stand without outbound access** — including the one these examples were
verified on — the call fails and the error branch answers:

```
{ "topic": "USD" }   →   HTTP 200
{"levelMessage":"11","statusCode":500,
 "message":"Error while try to call action 'T_Call/open the stream'","state":"1"}
```

That is the example working correctly: an unreachable endpoint is a failure, and
the failure has a path. Add `debug=true` to the start call and the reply also
carries `parametersContainer`, where you can see the configuration that was
resolved:

```json
"config": { "ratesUrl": "https://api.frankfurter.dev/v1",
            "listUrl": "https://jsonplaceholder.typicode.com/posts",
            "login": "", "password": "", "pageSize": 10 }
```

Use that when a Flow behaves as if it had no settings: it tells you whether the
configuration arrived or the call itself is at fault.

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
- **Expecting a body from the process.** The result is the sequence of chunks. If
  you also need a summary, join the branches before the end event.
- **Blank lines.** Streamed protocols use them as separators; the loop skips them
  rather than raising empty events.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `flow-patterns-config`. Then
import this file and compile it. It compiles anywhere; whether it *runs* depends
on your stand reaching `api.frankfurter.dev`.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
