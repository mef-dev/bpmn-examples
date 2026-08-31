# Catalog of examples

A list of the models in this repository, what each one is for, and what exactly it shows. The data is collected from the files themselves, not from descriptions: task modes, elements used, reserved words and declared types are read from the models.

## Capability coverage

The denominator is what the compiler accepts and what the properties panel offers. An empty row means the capability is not covered by any example.

| Capability | Models | Where to look |
|---|---|---|
| **Nodes** | | |
| Task | 48 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+46) |
| External component (Call Activity) | 5 | `flow-patterns/02-error-handling/event-error-routing.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+3) |
| Sub Process | 4 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+2) |
| Exclusive gateway | 32 | `api-call/api-call.bpmn`, `flow-patterns/01-basics/global-and-jsonpath.bpmn` (+30) |
| Parallel gateway | 15 | `flow-patterns/05-events-and-signals/boundary-event-fanout.bpmn`, `flow-patterns/05-events-and-signals/zip-chunks.bpmn` (+13) |
| Event-based gateway | 1 | `flow-patterns/05-events-and-signals/zip-chunks.bpmn` |
| Start event | 48 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+46) |
| End event | 48 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+46) |
| Boundary event | 39 | `flow-patterns/01-basics/global-and-jsonpath.bpmn`, `flow-patterns/02-error-handling/event-error-routing.bpmn` (+37) |
| Intermediate catch event | 2 | `api-call/api-call.bpmn`, `flow-patterns/05-events-and-signals/zip-chunks.bpmn` |
| Intermediate throw event | 7 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+5) |
| **Event kinds** | | |
| error | 35 | `flow-patterns/01-basics/global-and-jsonpath.bpmn`, `flow-patterns/02-error-handling/event-error-routing.bpmn` (+33) |
| timer | 1 | `api-call/api-call.bpmn` |
| signal | 3 | `flow-patterns/02-error-handling/event-error-routing.bpmn`, `flow-patterns/05-events-and-signals/zip-chunks.bpmn` (+1) |
| message | 7 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+5) |
| **Loops** | | |
| Multi Instance execution | 4 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+2) |
| **Data** | | |
| Data Object | 48 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+46) |
| Data Store | 3 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+1) |
| **Task modes** | | |
| Action | 39 | `api-call/api-call.bpmn`, `api-gateway/api-gateway.bpmn` (+37) |
| Function | 13 | `api-call/api-call.bpmn`, `api-gateway/api-gateway.bpmn` (+11) |
| ExternalAction | 0 | — **none** |
| Inline | 17 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+15) |
| **Types** | | |
| Native (C# class) | 40 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+38) |
| Inner (JSON Schema) | 44 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+42) |
| External (reference) | 9 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+7) |
| **Other** | | |
| Linked libraries | 12 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+10) |
| Flow parameters | 44 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+42) |
| Reference to another Flow | 7 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+5) |

## Models

### Kafka_getConfig

End-to-end example from the guide: from JSON on input to a typed configuration.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `Kafka.bpmn` | Native type; External type | Inline | `Input`, `Logger`, `Parameters`, `WorkflowEnvironment` |

### api-call

End-to-end example from the guide: calling an external API with a retry.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `api-call.bpmn` | exclusive gateway; timer; functions: FormReport, RestApi/GET | Action, Function | `#Previous`, `Input`, `Logger`, `Parameters`, `ServiceProvider` |

### api-gateway

End-to-end example from the guide: a proxy gateway that corrects the request.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `api-gateway.bpmn` | functions: CorrectModels, FormResponse, RestApi | Action, Function | `#Previous`, `Input`, `Parameters`, `ServiceProvider` |

### flow-patterns

Teaching examples grouped by the problem they solve.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `01-basics/echo-agent.bpmn` | Native type; External type | Inline | `#Previous`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment` |
| `01-basics/global-and-jsonpath.bpmn` | boundary event; exclusive gateway; functions: JsonPath, RestApi, SaveVariable | Action, Function | `#Previous`, `Global`, `Input`, `Logger`, `Parameters` |
| `02-error-handling/event-error-routing.bpmn` | boundary event; exclusive gateway; call to another Flow; signal; Native type; functions: HandleException, correctInput, p_ucp_act_Customers_Sync | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `03-config-as-flow/get-config.bpmn` | Native type | Inline | `#Previous`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment` |
| `03-config-as-flow/send-links-before.bpmn` | boundary event; exclusive gateway; Sub Process; message; Data Store; Multi Instance; Native type; functions: GetLinks, GetPageInfos, RestApi/Download | Action, Inline, Function | `#Previous`, `DataAssociations`, `Input`, `Logger`, `Parameters` |
| `03-config-as-flow/send-links.bpmn` | boundary event; exclusive gateway; Sub Process; call to another Flow; message; Data Store; Multi Instance; Native type; External type; functions: GetLinks, GetPageInfos, RestApi/Download | Action, Inline, Function | `#Previous`, `DataAssociations`, `Input`, `Logger`, `Parameters` |
| `04-pagination/sync-folder-paged.bpmn` | boundary event; exclusive gateway; Sub Process; call to another Flow; Multi Instance; functions: HandleException, JsonPath, RestApi | Action, Function | `#Previous`, `Global`, `Input`, `Logger`, `Parameters` |
| `05-events-and-signals/boundary-event-fanout.bpmn` | boundary event; parallel gateway; exclusive gateway; message; External type; functions: RestApi/GET | Inline, Function | `#Previous`, `Action.BoundaryEvents`, `Input`, `Logger`, `Parameters` |
| `05-events-and-signals/zip-chunks.bpmn` | parallel gateway; event-based gateway; Sub Process; signal; message; Data Store; Multi Instance; Native type; functions: GetPage, GetPageInfos, SaveVariable | Action, Inline, Function | `#Previous`, `#event`, `DataAssociations`, `Input`, `Logger` |
| `06-streaming-sse/llm-stream.bpmn` | boundary event; exclusive gateway; message; Native type; External type; functions: RestApi | Inline, Function | `#Previous`, `Action.BoundaryEvents`, `Input`, `Logger`, `Parameters` |
| `06-streaming-sse/sse-roundtrip.bpmn` | boundary event; parallel gateway; exclusive gateway; signal; message; External type; functions: 1, DataResult, RestApi | Action, Inline, Function | `#Previous`, `Action.BoundaryEvents`, `Input`, `Logger`, `Parameters` |
| `07-triggers/http-route-start.bpmn` | call to another Flow; Native type; External type | Inline | `#Previous`, `Input`, `Parameters` |
| `08-ai-agents/ai-completions.bpmn` | call to another Flow; Native type; External type; functions: AI/Completions | Inline, Function | `Input`, `Logger`, `Parameters`, `WorkflowEnvironment` |
| `08-ai-agents/compile-structured-prompt.bpmn` | Native type | Inline | `Input`, `Logger`, `Parameters`, `Root`, `WorkflowEnvironment` |

### http-stream

End-to-end example from the guide: a streaming response and event delivery.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `http_stream.bpmn` | boundary event; exclusive gateway; message; Native type; External type; functions: RestApi | Inline, Function | `#Previous`, `Action.BoundaryEvents`, `Input`, `Logger`, `Parameters` |

### tmforum-apis

Implementations of TM Forum Open APIs: each Flow is one operation (method + resource) with response caching and error handling.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `TMF620_Product_Catalog_Management/TMF620_Get_ProductOffering.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_CancelProductOrder/TMF622_Post_CancelProductOrder.bpmn` | boundary event; Native type; functions: HandleException, get_Note, p_ucp_del_ProductOrder | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Monitor/TMF622_Get_Monitor.bpmn` | boundary event; exclusive gateway; Native type; functions: HandleException, correct_EmptyResult, correct_Request | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Product_Ordering/TMF622_Get_ProductOrder.bpmn` | boundary event; exclusive gateway; Native type; functions: HandleException, correct_EmptyResult, correct_Request | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Product_Ordering/TMF622_Post_CancelProductOrder.bpmn` | boundary event; Native type; functions: HandleException, get_Note, p_ucp_del_ProductOrder | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Product_Ordering/TMF622_Post_ProductOrder.bpmn` | boundary event; Native type; functions: HandleException, POST_p_ucp_set_ProductOrder, add | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Product_Ordering/TMF622_Put_ProductOrder.bpmn` | boundary event; exclusive gateway; Native type; functions: HandleException, PUT_p_ucp_set_ProductOrder, change | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Get_Service.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Patch_Service.bpmn` | boundary event; exclusive gateway; Native type; functions: HandleException, formResponse, form_CacheId | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Post_Service.bpmn` | boundary event; Native type; functions: HandleException, p_ucp_set_ServiceOrder, proceedConfig | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Put_Service.bpmn` | boundary event; Native type; functions: HandleException, p_ucp_set_ServiceOrder, proceedConfig | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF653_Service_Test_Management/TMF653_POST_ServiceTest.bpmn` | boundary event; exclusive gateway; Native type; functions: HandleException, p_ucp_get_ServiceTest, proceedSessionParameters | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF654_PrepayBalance_Management/GET_AccumulatedBalance.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF654_PrepayBalance_Management/TMF654_GET_AccumulatedBalance.bpmn` | boundary event; parallel gateway; exclusive gateway; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF666_Account_Management/TMF666_Get_BillingAccount.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF666_Account_Management/TMF666_Post_BillingAccount.bpmn` | boundary event; Native type; functions: HandleException, p_ucp_set_BillingAccount_Dbss, proceedSessionParameters | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF666_Account_Management/TMF666_Put_BillingAccount.bpmn` | boundary event; exclusive gateway; Native type; functions: HandleException, formValidationError, p_ucp_set_BillingAccount_Dbss | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF677_Usage_Consumption_Management/TMF677_Get_QueryUsageConsumption.bpmn` | boundary event; exclusive gateway; functions: HandleException, add_Cache, correct_Result | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF677_Usage_Consumption_Management/TMF677_Post_QueryUsageConsumption.bpmn` | boundary event; exclusive gateway; Native type; functions: HandleException, add_Cache_Status, correct_Empty_Result | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF678_Customer_Bill_Management/TMF678_BillingCycle.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF678_Customer_Bill_Management/TMF678_Get_AppliedCustomerBillingRate.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF678_Customer_Bill_Management/TMF678_Get_BillingCycle.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Delete_Topic.bpmn` | boundary event; Native type; functions: HandleException, p_ucp_del_EventTopic, proceedConfig | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Get_Hub.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Get_Topic.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Get_Topic_Event.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Post_Topic.bpmn` | boundary event; Native type; functions: HandleException, p_ucp_set_EventTopic, proceedSessionParameters | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Put_Topic.bpmn` | boundary event; exclusive gateway; Native type; functions: HandleException, format_Validation_Error, p_ucp_set_EventTopic | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF724_Incident_Management/TMF724_POST_diagnoseIncident.bpmn` | boundary event; exclusive gateway; Native type; functions: RestApi, RestApi/GET, formatException | Action, Inline, Function | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF727_Service_Usage_Management/TMF727_Get_ServiceUsage.bpmn` | boundary event; parallel gateway; exclusive gateway; Native type; functions: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |

## What is missing for full coverage

Not covered by any example:

- the ExternalAction mode

Covered by one or two examples, which means it is effectively untested:

- Event-based gateway — 1
- Intermediate catch event — 2
- timer — 1
