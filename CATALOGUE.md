# Catalog of examples

A list of the models in this repository, what each one is for, and what it shows. The data is collected from the files themselves, not from descriptions: task modes, elements used, reserved words and declared types are read from the models.

## Capability coverage

The denominator is what the compiler accepts and what the properties panel offers. An empty row means the capability is not covered by any example.

| Capability | Models | Where to look |
|---|---|---|
| **Nodes** | | |
| Task | 43 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+41) |
| External component (Call Activity) | 8 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+6) |
| Sub Process | 1 | `flow-patterns/04-pagination/paged-fetch.bpmn` |
| Exclusive gateway | 24 | `api-call/api-call.bpmn`, `http-stream/http_stream.bpmn` (+22) |
| Parallel gateway | 12 | `tmforum-apis/TMF620_Product_Catalog_Management/TMF620_Get_ProductOffering.bpmn`, `tmforum-apis/TMF640_Service_Activation_and_Configuration/TMF640_Get_Service.bpmn` (+10) |
| Event-based gateway | 0 | — **none** |
| Start event | 43 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+41) |
| End event | 43 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+41) |
| Boundary event | 40 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+38) |
| Intermediate catch event | 1 | `api-call/api-call.bpmn` |
| Intermediate throw event | 1 | `http-stream/http_stream.bpmn` |
| **Event kinds** | | |
| error | 39 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+37) |
| timer | 1 | `api-call/api-call.bpmn` |
| signal | 0 | — **none** |
| message | 3 | `flow-patterns/05-events-and-signals/raise-event.bpmn`, `flow-patterns/06-streaming-sse/stream-response.bpmn` (+1) |
| **Loops and data** | | |
| Multi Instance execution | 1 | `flow-patterns/04-pagination/paged-fetch.bpmn` |
| Data Object | 43 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+41) |
| Data Store | 0 | — **none** |
| **Task modes** | | |
| Action | 41 | `api-call/api-call.bpmn`, `api-gateway/api-gateway.bpmn` (+39) |
| Function | 5 | `api-call/api-call.bpmn`, `api-gateway/api-gateway.bpmn` (+3) |
| ExternalAction | 0 | — **none** |
| Inline | 14 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/first-flow.bpmn` (+12) |
| **Types** | | |
| Native (C# class) | 34 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/03-config-as-flow/service-config.bpmn` (+32) |
| Inner (JSON Schema) | 43 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+41) |
| External (reference) | 10 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/first-flow.bpmn` (+8) |
| **Other** | | |
| Linked libraries | 3 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/08-ai-agents/structured-prompt.bpmn` (+1) |
| Flow parameters | 42 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+40) |
| Reference to another Flow | 9 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/first-flow.bpmn` (+7) |

## Models

### Kafka_getConfig

End-to-end example from the guide: from JSON on input to a typed configuration.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `Kafka.bpmn` | Data Object; Native (C# class); Inner (JSON Schema); External (reference) | Inline | `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |

### api-call

End-to-end example from the guide: calling an external API with a retry.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `api-call.bpmn` | Exclusive gateway; timer; Data Object; Inner (JSON Schema) | Action, Function | `#Previous`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `Transition`, `PassingResult` |

### api-gateway

End-to-end example from the guide: a proxy gateway that corrects the request.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `api-gateway.bpmn` | Data Object; Inner (JSON Schema) | Action, Function | `#Previous`, `Input`, `Parameters`, `ServiceProvider`, `PassingResult` |

### flow-patterns

Teaching examples, one per problem. Each is written for this folder, not lifted from a running system.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `01-basics/first-flow.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `02-error-handling/error-as-branch.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `03-config-as-flow/service-config.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `03-config-as-flow/use-config.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `04-pagination/paged-fetch.bpmn` | External component (Call Activity); Sub Process; error; Multi Instance execution; Data Object; Native (C# class); Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `Root`, `WorkflowEnvironment`, `Transition`, `PassingResult` |
| `05-events-and-signals/raise-event.bpmn` | External component (Call Activity); error; message; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `#event`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `Action.BoundaryEvents`, `PassingResult` |
| `06-streaming-sse/stream-response.bpmn` | External component (Call Activity); error; message; Data Object; Inner (JSON Schema); External (reference) | Action, Function, Inline | `#Previous`, `#PreviousData`, `#event`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `Action.BoundaryEvents`, `PassingResult` |
| `07-triggers/http-start.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `08-ai-agents/structured-prompt.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |

### http-stream

End-to-end example from the guide: a streaming response and event delivery.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `http_stream.bpmn` | Exclusive gateway; message; Data Object; Native (C# class); Inner (JSON Schema); External (reference) | Function, Inline | `#Previous`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `Action.BoundaryEvents`, `PassingResult` |

### tmforum-apis

Implementations of TM Forum Open APIs: each Flow is one operation (method + resource) with response caching and error handling.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `TMF620_Product_Catalog_Management/TMF620_Get_ProductOffering.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF622_CancelProductOrder/TMF622_Post_CancelProductOrder.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF622_Monitor/TMF622_Get_Monitor.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF622_Product_Ordering/TMF622_Get_ProductOrder.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF622_Product_Ordering/TMF622_Post_CancelProductOrder.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF622_Product_Ordering/TMF622_Post_ProductOrder.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF622_Product_Ordering/TMF622_Put_ProductOrder.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Get_Service.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Patch_Service.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Post_Service.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Put_Service.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF653_Service_Test_Management/TMF653_POST_ServiceTest.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF654_PrepayBalance_Management/GET_AccumulatedBalance.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF654_PrepayBalance_Management/TMF654_GET_AccumulatedBalance.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF666_Account_Management/TMF666_Get_BillingAccount.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF666_Account_Management/TMF666_Post_BillingAccount.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF666_Account_Management/TMF666_Put_BillingAccount.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF677_Usage_Consumption_Management/TMF677_Get_QueryUsageConsumption.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF677_Usage_Consumption_Management/TMF677_Post_QueryUsageConsumption.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF678_Customer_Bill_Management/TMF678_BillingCycle.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF678_Customer_Bill_Management/TMF678_Get_AppliedCustomerBillingRate.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF678_Customer_Bill_Management/TMF678_Get_BillingCycle.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Delete_Topic.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Get_Hub.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Get_Topic.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Get_Topic_Event.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Post_Topic.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Put_Topic.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF724_Incident_Management/TMF724_POST_diagnoseIncident.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action, Function, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `Root`, `WorkflowEnvironment`, `PassingResult` |
| `TMF727_Service_Usage_Management/TMF727_Get_ServiceUsage.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |

## What is missing for full coverage

Not covered by any example:

- Event-based gateway
- signal
- Data Store
- ExternalAction

Covered by one or two examples, which means it is effectively untested:

- Sub Process — 1
- Intermediate catch event — 1
- Intermediate throw event — 1
- timer — 1
- Multi Instance execution — 1
