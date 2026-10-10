# Catalog of examples

A list of the models in this repository, what each one is for, and what it shows. The data is collected from the files themselves, not from descriptions: task modes, elements used, reserved words and declared types are read from the models.

## Capability coverage

The denominator is what the compiler accepts and what the properties panel offers. An empty row means the capability is not covered by any example.

| Capability | Models | Where to look |
|---|---|---|
| **Nodes** | | |
| Task | 40 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+38) |
| External component (Call Activity) | 9 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+7) |
| Sub Process | 1 | `flow-patterns/04-pagination/paged-fetch.bpmn` |
| Exclusive gateway | 22 | `tmforum-apis/TMF620_Product_Catalog_Management/TMF620_Get_ProductOffering.bpmn`, `tmforum-apis/TMF622_Monitor/TMF622_Get_Monitor.bpmn` (+20) |
| Parallel gateway | 12 | `tmforum-apis/TMF620_Product_Catalog_Management/TMF620_Get_ProductOffering.bpmn`, `tmforum-apis/TMF640_Service_Activation_and_Configuration/TMF640_Get_Service.bpmn` (+10) |
| Event-based gateway | 0 | — **none** |
| Start event | 40 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+38) |
| End event | 40 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+38) |
| Boundary event | 40 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+38) |
| Intermediate catch event | 0 | — **none** |
| Intermediate throw event | 2 | `flow-patterns/05-events-and-signals/raise-event.bpmn`, `flow-patterns/06-streaming-sse/stream-response.bpmn` |
| **Event kinds** | | |
| error | 40 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+38) |
| timer | 0 | — **none** |
| signal | 0 | — **none** |
| message | 2 | `flow-patterns/05-events-and-signals/raise-event.bpmn`, `flow-patterns/06-streaming-sse/stream-response.bpmn` |
| **Loops and data** | | |
| Multi Instance execution | 1 | `flow-patterns/04-pagination/paged-fetch.bpmn` |
| Data Object | 40 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+38) |
| Data Store | 1 | `flow-patterns/09-files-and-archives/archive-and-link.bpmn` |
| **Task modes** | | |
| Action | 40 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+38) |
| Function | 3 | `flow-patterns/06-streaming-sse/stream-response.bpmn`, `flow-patterns/09-files-and-archives/archive-and-link.bpmn` (+1) |
| ExternalAction | 0 | — **none** |
| Inline | 13 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+11) |
| **Types** | | |
| Native (C# class) | 31 | `flow-patterns/03-config-as-flow/service-config.bpmn`, `flow-patterns/04-pagination/paged-fetch.bpmn` (+29) |
| Inner (JSON Schema) | 37 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+35) |
| External (reference) | 9 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+7) |
| **Other** | | |
| Linked libraries | 1 | `flow-patterns/08-ai-agents/structured-prompt.bpmn` |
| Flow parameters | 38 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+36) |
| Reference to another Flow | 9 | `flow-patterns/01-basics/first-flow.bpmn`, `flow-patterns/02-error-handling/error-as-branch.bpmn` (+7) |

## Models

### flow-patterns

Teaching examples for the MEF.DEV platform, one per problem. Each was written to be read: small enough to hold in your head, commented in the code itself, and compiled against the real platform before it was published here.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `01-basics/first-flow.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `02-error-handling/error-as-branch.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `03-config-as-flow/service-config.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action, Inline | `#PreviousData`, `Logger`, `WorkflowEnvironment`, `PassingResult` |
| `03-config-as-flow/use-config.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `04-pagination/paged-fetch.bpmn` | External component (Call Activity); Sub Process; error; Multi Instance execution; Data Object; Native (C# class); Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `Root`, `WorkflowEnvironment`, `Transition`, `PassingResult` |
| `05-events-and-signals/raise-event.bpmn` | External component (Call Activity); error; message; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `Action.BoundaryEvents`, `PassingResult` |
| `06-streaming-sse/stream-response.bpmn` | External component (Call Activity); error; message; Data Object; Inner (JSON Schema); External (reference) | Action, Function, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `Action.BoundaryEvents`, `PassingResult` |
| `07-triggers/http-start.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `08-ai-agents/structured-prompt.bpmn` | External component (Call Activity); error; Data Object; Inner (JSON Schema); External (reference) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `09-files-and-archives/archive-and-link.bpmn` | External component (Call Activity); error; Data Object; Data Store; Native (C# class); Inner (JSON Schema); External (reference) | Action, Function, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |

### tmforum-apis

Implementations of TM Forum Open APIs: each Flow is one operation (method + resource) with response caching and error handling.

| Model | What it shows | Modes | Words used |
|---|---|---|---|
| `TMF620_Product_Catalog_Management/TMF620_Get_ProductOffering.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF622_CancelProductOrder/TMF622_Post_CancelProductOrder.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF622_Monitor/TMF622_Get_Monitor.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF622_Product_Ordering/TMF622_Get_ProductOrder.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF622_Product_Ordering/TMF622_Post_CancelProductOrder.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF622_Product_Ordering/TMF622_Post_ProductOrder.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF622_Product_Ordering/TMF622_Put_ProductOrder.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Get_Service.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Patch_Service.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Post_Service.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Put_Service.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF653_Service_Test_Management/TMF653_POST_ServiceTest.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF654_PrepayBalance_Management/GET_AccumulatedBalance.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF654_PrepayBalance_Management/TMF654_GET_AccumulatedBalance.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object | Action | `#Previous`, `#PreviousData`, `Input`, `Parameters` |
| `TMF666_Account_Management/TMF666_Get_BillingAccount.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF666_Account_Management/TMF666_Post_BillingAccount.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF666_Account_Management/TMF666_Put_BillingAccount.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF677_Usage_Consumption_Management/TMF677_Get_QueryUsageConsumption.bpmn` | Exclusive gateway; error; Data Object | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF677_Usage_Consumption_Management/TMF677_Post_QueryUsageConsumption.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF678_Customer_Bill_Management/TMF678_BillingCycle.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF678_Customer_Bill_Management/TMF678_Get_AppliedCustomerBillingRate.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF678_Customer_Bill_Management/TMF678_Get_BillingCycle.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Delete_Topic.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Get_Hub.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Get_Topic.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Get_Topic_Event.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Post_Topic.bpmn` | error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF688_Event_Management/TMF688_Put_Topic.bpmn` | Exclusive gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF724_Incident_Management/TMF724_POST_diagnoseIncident.bpmn` | Exclusive gateway; error; Data Object; Native (C# class) | Action, Function, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `PassingResult` |
| `TMF727_Service_Usage_Management/TMF727_Get_ServiceUsage.bpmn` | Exclusive gateway; Parallel gateway; error; Data Object; Native (C# class); Inner (JSON Schema) | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment`, `ServiceProvider`, `PassingResult` |

## What is missing for full coverage

Not covered by any example:

- Event-based gateway
- Intermediate catch event
- timer
- signal
- ExternalAction

Covered by one or two examples, which means it is effectively untested:

- Sub Process — 1
- Intermediate throw event — 2
- message — 2
- Multi Instance execution — 1
- Data Store — 1
- Linked libraries — 1
