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
| `cacheStatus`: `Added` or `IsCompleted` | the answer, and the response header in a published plugin |
| A setting from the configuration Flow | `cacheSeconds` — how long the answer is kept |
| The error text in the caller's language | `Messages`, as in [02 · Errors](../02-error-handling/) |

## The model

```
start → Get Config → Parse Config → read the request id → look for the stored answer → answered before?
                                                                                           │ no         │ yes
                                                                                           ↓            ↓
                                                                              accept the payment   answer as before → end (from the cache)
                                                                                           ↓
                                                                                 store the answer → end
```

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `PaymentRequest` | inner, JSON Schema | the process boundary: `orderId`, `amount` |
| `PaymentAnswer` | inner, native C# | the answer: `orderId`, `amount`, `confirmation`, `acceptedAt`, `cacheStatus` |
| `Messages` | inner, native C# | the error text for a request without an id, one per language |
| `ExternalConfig` | external | the configuration type; `cacheSeconds` sets how long the answer is kept |

`Parameters.cacheKey` (a global parameter) carries the key from the step that
reads the header to the step that stores the answer.

## What you should get back

| Call | `x-ms-client-request-id` | HTTP | Answer |
|---|---|---|---|
| first | `r-1` | 200 | a new `confirmation`, `"cacheStatus":"Added"` |
| again | `r-1` | 200 | the **same** `confirmation` and `acceptedAt`, `"cacheStatus":"IsCompleted"` |
| another | `r-2` | 200 | a new `confirmation`, `"cacheStatus":"Added"` |
| no header, `Accept-Language: uk` | — | 500 | `"message":"Потрібен заголовок x-ms-client-request-id"` |

```
{"orderId":"ORD-1001","amount":25.5,"confirmation":"f5fd623e-ebe0-4f40-80f1-f64cfd590f10",
 "acceptedAt":"2026-10-21T14:47:11.9897513Z","cacheStatus":"IsCompleted"}
```

## Why it is built this way

**The id belongs to the request, not to the body.** The client generates it once
per operation and repeats it on every retry. Two different operations with the
same body are two requests; one operation retried is one.

**The cache is the platform's, not the Flow's.** `ServiceProvider.GetService<IDistributedCache>()`
returns the cache shared by every instance on the stand, so a retry finds the
answer whichever instance served the first call. A `Parameters` field would live
only as long as one instance.

**Store after the work, not before.** The answer is stored once it exists. A
failure before that leaves nothing in the cache, and the retry does the work.

**How long is a setting.** `cacheSeconds` comes from the configuration Flow:
after that time the same id is a new request.

**The header is read where the request is.** Started through the API, the
platform records the request headers (`HttpRequestService`); a published plugin
has the HTTP request itself (`WorkflowEnvironment.Variables["HttpRequest"]`).
The step reads whichever is there.

## Where newcomers stumble

- **Keying the cache by the body.** Two orders for the same amount are not one
  order. Key by the request id.
- **Storing the answer before the work.** A failed call then answers its retry
  with an answer that was never true.
- **Answering a retry with a new id.** `confirmation` is issued once; the retry
  shows the same one. That is how a client sees that nothing was done twice.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `bpmn-examples-config`. Then
import this file, compile it, and start it twice with the same
`x-ms-client-request-id` header, then once without it.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
