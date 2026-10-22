# TM Forum Open APIs

Flows that implement TM Forum Open API operations: one Flow per operation
(method + resource), one folder per TMF specification.

## What a folder holds

| File | What it is |
|---|---|
| `TMFnnn_<Method>_<Resource>.bpmn` | the Flow of one operation |
| `README_TMFnnn.md` | the operations, their behaviour and lifecycle states |
| `*.oas.yaml`, `*.swagger.json` | the TM Forum OpenAPI specification the operations follow |
| `*.postman_collection.json` | requests to try the operations |
| `tmfnnn_*.json` | example payloads |

## How these Flows differ from flow-patterns

- **They need a BSS behind them.** The steps call actions of the BSS database
  (for example `p_ucp_get_productOffering` in TMF620). Without that database
  the Flows compile but do not answer.
- **They do not use `bpmn-examples-config`** or any other Flow of this
  repository.
- **Read operations cache their answers.** Every `Get` Flow keys its answer in
  the platform's distributed cache by `x-ms-client-request-id`; a repeated
  request gets the stored answer. `Post`, `Put` and `Delete` Flows do not use
  the cache. The same idea, in its smallest form, is
  [flow-patterns/10-idempotency](../flow-patterns/10-idempotency/).

## Folders with two variants of one operation

| Operation | Files |
|---|---|
| TMF622 Post CancelProductOrder | `TMF622_Product_Ordering/TMF622_Post_CancelProductOrder.bpmn` and `TMF622_CancelProductOrder/TMF622_Post_CancelProductOrder.bpmn` |
| TMF654 Get AccumulatedBalance | `TMF654_PrepayBalance_Management/TMF654_GET_AccumulatedBalance.bpmn` and `GET_AccumulatedBalance.bpmn` |

The two files of each pair are different models of the same operation.
