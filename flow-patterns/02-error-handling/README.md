# 02 · Errors as a branch of the diagram

An error is not an interruption here. It is a path on the diagram, with its own
handler and its own typed answer — in the caller's language.

## What this example demonstrates

| Capability | Where to look |
|---|---|
| Boundary error event on a step | on `Get Config`, `Parse Config` and `validate the order` (ids `Ev_Err_CA_Config`, `Ev_Err_T_ParseConfig`, `Ev_Err_T_Validate`) |
| One handler serving several steps | three arrows arriving at `handle Exception` |
| `#PreviousData` — the only carrier of the exception | the step `handle Exception`: its implementation calls `HandleException` with `"prevData": "#PreviousData"` |
| A Code Action (`HandleException`) | the model's `CodeActions` (designer: Code Actions; XML: global parameter `CodeActions`) |
| HTTP 500 on the failure branch | `WorkflowEnvironment.Variables["StatusCode"]` in `HandleException` |
| The error text in the caller's language | the type `Messages` and the request header `Accept-Language` |

## The model

```
start → Get Config → Parse Config → validate the order → end
            ↓             ↓                 ↓
            └─────────────┴─────────────────┴──→ handle Exception → end (error)
```

`Get Config` calls the Flow `bpmn-examples-config`: the file
[`03-config-as-flow/bpmn-examples-config.bpmn`](../03-config-as-flow/bpmn-examples-config.bpmn),
imported into the tenant library `bpmn_examples`.

All three steps that have a boundary error event lead into the **same** handler.
Several arrows into one step is how BPMN says "these failures are handled
alike".

## Types it declares

| Type | Kind | How it is used |
|---|---|---|
| `OrderRequest` | inner, JSON Schema | the process boundary; `Input.orderId` is its only field |
| `ErrorResponse` | inner, JSON Schema | the shape of a failure: `levelMessage`, `statusCode`, `message`, `state`. The handler fills it and it becomes the process result |
| `Messages` | inner, native C# | the texts of the errors this Flow raises, one per language |
| `ExternalConfig` | external | the configuration type, owned by `bpmn-examples-config`; its `language` is the installation's language |
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
| `ja,fr;q=0.7` | 500 | `orderId est obligatoire` — there is no Japanese text, so the next language, `fr` |
| `de-DE` | 500 | `orderId ist erforderlich` |
| `ar` | 500 | `الحقل orderId مطلوب` |
| `ja` | 500 | `orderId is required` — no Japanese text and no other language, so the installation's language (`en` in the configuration Flow) |
| none | 500 | `orderId is required` |

```
HTTP 500
{"levelMessage":"11","statusCode":500,"message":"Потрібно вказати orderId","state":"1"}
```

A caller reads `statusCode` and `message`. `levelMessage` and `state` are fields
of the platform's error format; this handler always sets them to `"11"` and `"1"`.

## Why it is built this way

**The handler takes `#PreviousData`, never `#Previous`.** This is the single
detail that costs newcomers the most time. `#Previous` is the previous node's
*result* — on a failure there is no result. `#PreviousData` is the wrapper around
it, and the only place carrying the `Exception`. Feed the handler `#Previous` and
the compiler answers `Cannot implicitly convert 'System.Exception' to
'WorkflowPassingNodeResult'`, which does not obviously mean "wrong placeholder".

**The handler sets the HTTP status itself.** `WorkflowEnvironment.Variables["StatusCode"] = 500`
is the HTTP status of the answer; a Flow published as a plugin endpoint gets it
on its HTTP response as well. A business-rule error answers 500 with the reason in `message`; a text in
`Messages` can carry its own status when the request
itself has to change (400) or the caller has to wait (409, 503) — see
[10 · Idempotency](../10-idempotency/).

**The language comes from the request.** The order is:

1. `Accept-Language` of the request, highest `q` first, by its primary subtag
   (`uk-UA` → `uk`);
2. the installation's language — `language` in the configuration Flow;
3. English.

The languages are the ones `Messages` has a text for: adding a language is
adding a text, not changing code. This example has texts in `en`, `uk`, `fr`,
`pt`, `es`, `de` and `ar`. A Flow published as a plugin endpoint also answers
with `Content-Language`.

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

Follow [Before you start](../README.md#before-you-start). Then import this file
into the same library, compile it, and start it with and without an `orderId`,
and with different `Accept-Language` headers.

---
For how the types in this example are designed, see [TYPE-DESIGN.md](../TYPE-DESIGN.md).
