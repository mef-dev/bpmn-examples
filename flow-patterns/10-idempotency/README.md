# 10 · Idempotency with the distributed cache

A client that lost a response sends the request again. The second call must not
do the work twice: it gets the stored answer. The request id in the header
`x-ms-client-request-id` is the key, and the platform's distributed cache keeps
the answer.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| Reading a request header in a Flow | `read the request id` |
| The platform's distributed cache (`IDistributedCache`) | `look for the stored answer`, `store the answer` |
| An early answer through a decision | `answered before?` → `answer as before` → `answered from the cache` |
| `cacheStatus`: `Added` or `IsCompleted` | the response header in a published plugin, repeated in the answer |
| HTTP 201, and an error status per message (400, 409, 503) | `answer 201`, `Messages` |
| A setting from the configuration Flow | `cacheSeconds` — how long the answer is kept |
| The error text in the caller's language | `Messages`, as in [02 · Errors](../02-error-handling/) |

## The model

```
start → Get Config → Parse Config → read the request id → look for the stored answer → answered before?
                                                                                    │ no            │ yes
                                                                                    ↓               ↓
                                                                       accept the payment     answer as before → end: answered from the cache
                                                                                    ↓
                                                                          store the answer → answer 201 → end: answered and stored

Get Config, Parse Config, read the request id, look for the stored answer
  ──(on error)──→ handle Exception → end: request refused
```

`Get Config` calls the Flow `bpmn-examples-config`: the file
[`03-config-as-flow/bpmn-examples-config.bpmn`](../03-config-as-flow/bpmn-examples-config.bpmn),
imported into the tenant library `bpmn_examples`.

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `PaymentRequest` | inner, JSON Schema | the process boundary: `orderId`, `amount` |
| `PaymentAnswer` | inner, native C# | the answer: `orderId`, `amount`, `confirmation`, `acceptedAt`, `cacheStatus` |
| `ErrorResponse` | inner, JSON Schema | the refusal: `levelMessage`, `statusCode`, `message`, `state` |
| `Messages` | inner, native C# | the refusal texts, one per language, and their HTTP status |
| `ExternalConfig` | external | the configuration type; `cacheSeconds` (300 in `bpmn-examples-config`) sets how long the answer is kept |

`Parameters.cacheKey` (a global parameter) carries the key from the step that
reads the header to the step that stores the answer.

## What you should get back

| Call | `x-ms-client-request-id` | HTTP | Answer |
|---|---|---|---|
| first | `r-1` | 201 | a new `confirmation`, `"cacheStatus":"Added"` |
| again | `r-1` | 201 | the **same** `confirmation` and `acceptedAt`, `"cacheStatus":"IsCompleted"` |
| another | `r-2` | 201 | a new `confirmation`, `"cacheStatus":"Added"` |
| again while `r-1` still runs | `r-1` | 409 | `The same request is still in progress; repeat it later` |
| no header, `Accept-Language: uk` | — | 400 | `"message":"Потрібен заголовок x-ms-client-request-id"` |
| the cache is not available | `r-3` | 503 | `The service is not available now; repeat the request later` |

409 appears only when a retry arrives within 60 seconds of a first call that
has not finished; 503 only when the installation's distributed cache is
unreachable.

```
{"orderId":"ORD-1001","amount":25.5,"confirmation":"f5fd623e-ebe0-4f40-80f1-f64cfd590f10",
 "acceptedAt":"2026-10-21T14:47:11.9897513Z","cacheStatus":"IsCompleted"}
```

## Why it is built this way

**The id belongs to the request, not to the body.** The client generates it once
per operation and repeats it on every retry. A repeated id gets the first
answer: the body of the retry is not compared.

**The key starts with the Flow's name.** Every Flow on the installation shares the
cache, so the key is `idempotent-request:` + the request id. A Flow that serves
several clients adds whatever separates them.

**The cache is the platform's, not the Flow's.** `ServiceProvider.GetService<IDistributedCache>()`
returns the cache shared by every server of the installation, so a retry finds the
answer wherever the first call ran. A `Parameters` field lives only as long as
one run of the Flow.

**The request is marked while the work runs.** Before the work the key holds
`pending` for 60 seconds; a retry that arrives meanwhile gets 409 and repeats
later. The cache has no "add if absent": two calls at the same moment can both
pass the check, so the mark narrows the window, it does not close it.

**Store after the work, not before.** The answer is stored once it exists. A
failure before that leaves only the `pending` mark: retries get 409 until it
expires, then do the work. A failure to store after the work is logged and the
answer still goes back; a retry then does the work again.

**The retention time is a setting.** `cacheSeconds` comes from the configuration
Flow: after that time the same id is a new request.

**The header is read where the request is.** A Flow started on the platform
finds the request headers in `HttpRequestService`; a Flow published as a plugin
endpoint has the HTTP request itself (`WorkflowEnvironment.Variables["HttpRequest"]`).
The step reads whichever is there.

## Where newcomers stumble

- **Keying the cache by the body.** Two orders for the same amount are not one
  order. Key by the request id.
- **Storing the answer before the work.** A failed call then answers its retry
  with an answer that was never true.
- **Issuing a new `confirmation` on a retry.** `confirmation` is issued once;
  the retry shows the same one. That is how a client sees that nothing was done
  twice.

## Run it

Follow [Before you start](../README.md#before-you-start). Then import this file
into the same library and compile it. Build → Execute sends no
`x-ms-client-request-id`, so the answer there is the refusal: HTTP 400,
`x-ms-client-request-id is required`. The stored answer appears when the Flow,
published as a plugin endpoint (designer: **Publish**), is called twice with the
same header.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
