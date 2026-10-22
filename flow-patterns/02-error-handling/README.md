# 02 · Errors as a branch of the diagram

An error is not an interruption here. It is a path on the diagram, with its own
handler and its own typed answer — in the caller's language.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| Boundary error event on a task | `Ev_Err_CA_Config`, `Ev_Err_T_ParseConfig`, `Ev_Err_T_Validate` |
| One handler serving several tasks | three sequence flows arriving at `handle Exception` |
| `#PreviousData` — the only carrier of the exception | the handler's `actionParam` |
| A Code Action (`HandleException`) | declared in `CodeActions`, called by the handler |
| HTTP 500 on the failure branch | `WorkflowEnvironment.Variables["StatusCode"]` in the handler |
| The error text in the caller's language | `Messages` (inner type) and `Accept-Language` |

## The model

```
start → Get Config → Parse Config → validate the order → end
            ↓             ↓                 ↓
            └─────────────┴─────────────────┴──→ handle Exception → end (error)
```

`Get Config` calls the configuration Flow [`03-config-as-flow/service-config.bpmn`](../03-config-as-flow/service-config.bpmn), imported into the tenant library under the name `bpmn-examples-config`.

All three risky steps lead into the **same** handler. That is normal: several incoming
sequence flows into one node is how BPMN says "these failures are handled alike".

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `OrderRequest` | inner, JSON Schema | the process boundary; `Input.orderId` is its only field |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure: `levelMessage`, `statusCode`, `message`, `state`. The handler fills it and it becomes the process result |
| `Messages` | inner, native C# | the texts of the errors this Flow raises, one per language |
| `ExternalConfig` | external | the configuration type, owned by `service-config`; its `language` is the stand's language |
| `PassingResult` | reserved | not declared by you — it is the type of `#PreviousData`, the wrapper that carries `Exception` |

The pairing to remember is `ErrorResponse` + `PassingResult`. One is what you
give the caller, the other is what the engine gives you.

## What you should get back

A valid order goes down the happy path:

```
{ "orderId": "ORD-1001" }   →   HTTP 200   {"orderId":"ORD-1001"}
```

An empty one takes the error branch, and the text follows `Accept-Language`:

| `Accept-Language` | HTTP | `message` |
|---|---|---|
| `uk-UA,uk;q=0.9,en;q=0.8` | 500 | `Потрібно вказати orderId` |
| `ja,fr;q=0.7` | 500 | `orderId est obligatoire` |
| `de-DE` | 500 | `orderId ist erforderlich` |
| `ar` | 500 | `الحقل orderId مطلوب` |
| `ja` | 500 | `orderId is required` — no Japanese text, so the stand's language (`en` in `service-config`) |
| none | 500 | `orderId is required` |

```
HTTP 500
{"levelMessage":"11","statusCode":500,"message":"Потрібно вказати orderId","state":"1"}
```

## Why it is built this way

**The handler takes `#PreviousData`, never `#Previous`.** This is the single
detail that costs newcomers the most time. `#Previous` is the previous node's
*result* — on a failure there is no result. `#PreviousData` is the wrapper around
it, and the only place carrying the `Exception`. Feed the handler `#Previous` and
the compiler answers `Cannot implicitly convert 'System.Exception' to
'WorkflowPassingNodeResult'`, which does not obviously mean "wrong placeholder".

**The handler sets the HTTP status itself.** `WorkflowEnvironment.Variables["StatusCode"] = 500`
is what the platform answers with when the Flow is started through the API; a
published plugin gets the status on its HTTP response as well. The platform's
API contract answers a business-rule error with 500 and the reason in
`message`; a text in `Messages` can carry its own status when the request
itself has to change (400) or the caller has to wait (409, 503) — see
[10 · Idempotency](../10-idempotency/).

**The language comes from the request.** The order is:

1. `Accept-Language` of the request, highest `q` first, by its primary subtag
   (`uk-UA` → `uk`);
2. the stand's language — `language` in the configuration Flow;
3. English.

The languages are the ones `Messages` has a text for: adding a language is
adding a text, not changing code. The platform's domain APIs name `en` and
`uk`; the example carries more texts, and the order stays the same. A
published plugin also answers with `Content-Language`.

**The text to translate is the one the step threw.** The engine wraps the
exception of a step (`Error while try to call action …`); the handler looks up
the innermost exception's message. An exception without a text in `Messages` —
a technical failure — keeps the engine's message as it is.

## Where newcomers stumble

- **Catching inside the code instead of on the diagram.** A `try/catch` in a task
  body hides the failure from the diagram: the process continues down the happy
  path with a half-built result. Let it throw and draw the branch.
- **One handler per task.** Tempting, and it doubles the diagram. Attach several
  boundary events to one handler until the responses genuinely differ.
- **Translating in the step.** The step throws one stable text; the handler
  chooses the language. A translated `throw` would make every language a
  different error.

## Run it

Import `service-config.bpmn` from [03 · Configuration](../03-config-as-flow/)
into a **tenant** library first, under the name `bpmn-examples-config`. Then
import this file, compile it, and start it with and without an `orderId`, and
with different `Accept-Language` headers.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
