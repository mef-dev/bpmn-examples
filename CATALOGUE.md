# Каталог прикладів

Перелік моделей репозиторію з призначенням кожної та переліком того, що саме вона показує. Дані зібрано з самих файлів, а не з описів: режими задач, задіяні елементи, зарезервовані слова та оголошені типи прочитано з моделей.

## Покриття можливостей

Знаменник — те, що приймає компілятор і що пропонує панель властивостей. Порожній рядок означає, що можливість не покрита жодним прикладом.

| Можливість | Моделей | Де подивитись |
|---|---|---|
| **Вузли** | | |
| Задача | 48 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+46) |
| Зовнішній компонент (Call Activity) | 5 | `flow-patterns/02-error-handling/event-error-routing.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+3) |
| Підпроцес | 4 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+2) |
| Ексклюзивний шлюз | 32 | `api-call/api-call.bpmn`, `flow-patterns/01-basics/global-and-jsonpath.bpmn` (+30) |
| Паралельний шлюз | 15 | `flow-patterns/05-events-and-signals/boundary-event-fanout.bpmn`, `flow-patterns/05-events-and-signals/zip-chunks.bpmn` (+13) |
| Подієвий шлюз | 1 | `flow-patterns/05-events-and-signals/zip-chunks.bpmn` |
| Початкова подія | 48 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+46) |
| Кінцева подія | 48 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+46) |
| Гранична подія | 39 | `flow-patterns/01-basics/global-and-jsonpath.bpmn`, `flow-patterns/02-error-handling/event-error-routing.bpmn` (+37) |
| Проміжна подія-перехоплювач | 2 | `api-call/api-call.bpmn`, `flow-patterns/05-events-and-signals/zip-chunks.bpmn` |
| Проміжна подія-кидок | 7 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+5) |
| **Види подій** | | |
| помилка | 35 | `flow-patterns/01-basics/global-and-jsonpath.bpmn`, `flow-patterns/02-error-handling/event-error-routing.bpmn` (+33) |
| таймер | 1 | `api-call/api-call.bpmn` |
| сигнал | 3 | `flow-patterns/02-error-handling/event-error-routing.bpmn`, `flow-patterns/05-events-and-signals/zip-chunks.bpmn` (+1) |
| повідомлення | 7 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+5) |
| **Цикли** | | |
| виконання у кількох екземплярах | 4 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+2) |
| **Дані** | | |
| Data Object | 48 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+46) |
| Data Store | 3 | `flow-patterns/03-config-as-flow/send-links-before.bpmn`, `flow-patterns/03-config-as-flow/send-links.bpmn` (+1) |
| **Режими задачі** | | |
| Action | 39 | `api-call/api-call.bpmn`, `api-gateway/api-gateway.bpmn` (+37) |
| Function | 13 | `api-call/api-call.bpmn`, `api-gateway/api-gateway.bpmn` (+11) |
| ExternalAction | 0 | — **немає** |
| Inline | 17 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+15) |
| **Типи** | | |
| Native (клас C#) | 40 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+38) |
| Inner (JSON Schema) | 44 | `Kafka_getConfig/Kafka.bpmn`, `api-call/api-call.bpmn` (+42) |
| External (посилання) | 9 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+7) |
| **Інше** | | |
| Підключені бібліотеки | 12 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+10) |
| Параметри Flow | 44 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+42) |
| Посилання на інший Flow | 7 | `Kafka_getConfig/Kafka.bpmn`, `flow-patterns/01-basics/echo-agent.bpmn` (+5) |

## Моделі

### Kafka_getConfig

Наскрізний приклад із ґайду: з JSON на вході до типізованої конфігурації.

| Модель | Що показує | Режими | Задіяні слова |
|---|---|---|---|
| `Kafka.bpmn` | тип Native; тип External | Inline | `Input`, `Logger`, `Parameters`, `WorkflowEnvironment` |

### api-call

Наскрізний приклад із ґайду: виклик зовнішнього API з повтором.

| Модель | Що показує | Режими | Задіяні слова |
|---|---|---|---|
| `api-call.bpmn` | ексклюзивний шлюз; таймер; функції: FormReport, RestApi/GET | Action, Function | `#Previous`, `Input`, `Logger`, `Parameters`, `ServiceProvider` |

### api-gateway

Наскрізний приклад із ґайду: проксі-шлюз із коригуванням запиту.

| Модель | Що показує | Режими | Задіяні слова |
|---|---|---|---|
| `api-gateway.bpmn` | функції: CorrectModels, FormResponse, RestApi | Action, Function | `#Previous`, `Input`, `Parameters`, `ServiceProvider` |

### flow-patterns

Навчальні приклади, згруповані за задачею, яку вони розвʼязують.

| Модель | Що показує | Режими | Задіяні слова |
|---|---|---|---|
| `01-basics/echo-agent.bpmn` | тип Native; тип External | Inline | `#Previous`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment` |
| `01-basics/global-and-jsonpath.bpmn` | гранична подія; ексклюзивний шлюз; функції: JsonPath, RestApi, SaveVariable | Action, Function | `#Previous`, `Global`, `Input`, `Logger`, `Parameters` |
| `02-error-handling/event-error-routing.bpmn` | гранична подія; ексклюзивний шлюз; виклик іншого Flow; сигнал; тип Native; функції: HandleException, correctInput, p_ucp_act_Customers_Sync | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `03-config-as-flow/get-config.bpmn` | тип Native | Inline | `#Previous`, `Input`, `Logger`, `Parameters`, `WorkflowEnvironment` |
| `03-config-as-flow/send-links-before.bpmn` | гранична подія; ексклюзивний шлюз; підпроцес; повідомлення; Data Store; кілька екземплярів; тип Native; функції: GetLinks, GetPageInfos, RestApi/Download | Action, Inline, Function | `#Previous`, `DataAssociations`, `Input`, `Logger`, `Parameters` |
| `03-config-as-flow/send-links.bpmn` | гранична подія; ексклюзивний шлюз; підпроцес; виклик іншого Flow; повідомлення; Data Store; кілька екземплярів; тип Native; тип External; функції: GetLinks, GetPageInfos, RestApi/Download | Action, Inline, Function | `#Previous`, `DataAssociations`, `Input`, `Logger`, `Parameters` |
| `04-pagination/sync-folder-paged.bpmn` | гранична подія; ексклюзивний шлюз; підпроцес; виклик іншого Flow; кілька екземплярів; функції: HandleException, JsonPath, RestApi | Action, Function | `#Previous`, `Global`, `Input`, `Logger`, `Parameters` |
| `05-events-and-signals/boundary-event-fanout.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; повідомлення; тип External; функції: RestApi/GET | Inline, Function | `#Previous`, `Action.BoundaryEvents`, `Input`, `Logger`, `Parameters` |
| `05-events-and-signals/zip-chunks.bpmn` | паралельний шлюз; подієвий шлюз; підпроцес; сигнал; повідомлення; Data Store; кілька екземплярів; тип Native; функції: GetPage, GetPageInfos, SaveVariable | Action, Inline, Function | `#Previous`, `#event`, `DataAssociations`, `Input`, `Logger` |
| `06-streaming-sse/llm-stream.bpmn` | гранична подія; ексклюзивний шлюз; повідомлення; тип Native; тип External; функції: RestApi | Inline, Function | `#Previous`, `Action.BoundaryEvents`, `Input`, `Logger`, `Parameters` |
| `06-streaming-sse/sse-roundtrip.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; сигнал; повідомлення; тип External; функції: 1, DataResult, RestApi | Action, Inline, Function | `#Previous`, `Action.BoundaryEvents`, `Input`, `Logger`, `Parameters` |
| `07-triggers/http-route-start.bpmn` | виклик іншого Flow; тип Native; тип External | Inline | `#Previous`, `Input`, `Parameters` |
| `08-ai-agents/ai-completions.bpmn` | виклик іншого Flow; тип Native; тип External; функції: AI/Completions | Inline, Function | `Input`, `Logger`, `Parameters`, `WorkflowEnvironment` |
| `08-ai-agents/compile-structured-prompt.bpmn` | тип Native | Inline | `Input`, `Logger`, `Parameters`, `Root`, `WorkflowEnvironment` |

### http-stream

Наскрізний приклад із ґайду: потокова відповідь і розсилання подій.

| Модель | Що показує | Режими | Задіяні слова |
|---|---|---|---|
| `http_stream.bpmn` | гранична подія; ексклюзивний шлюз; повідомлення; тип Native; тип External; функції: RestApi | Inline, Function | `#Previous`, `Action.BoundaryEvents`, `Input`, `Logger`, `Parameters` |

### tmforum-apis

Реалізації відкритих API TM Forum: кожен Flow — одна операція (метод + ресурс) з кешуванням відповіді та обробкою помилок.

| Модель | Що показує | Режими | Задіяні слова |
|---|---|---|---|
| `TMF620_Product_Catalog_Management/TMF620_Get_ProductOffering.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_CancelProductOrder/TMF622_Post_CancelProductOrder.bpmn` | гранична подія; тип Native; функції: HandleException, get_Note, p_ucp_del_ProductOrder | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Monitor/TMF622_Get_Monitor.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: HandleException, correct_EmptyResult, correct_Request | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Product_Ordering/TMF622_Get_ProductOrder.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: HandleException, correct_EmptyResult, correct_Request | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Product_Ordering/TMF622_Post_CancelProductOrder.bpmn` | гранична подія; тип Native; функції: HandleException, get_Note, p_ucp_del_ProductOrder | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Product_Ordering/TMF622_Post_ProductOrder.bpmn` | гранична подія; тип Native; функції: HandleException, POST_p_ucp_set_ProductOrder, add | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF622_Product_Ordering/TMF622_Put_ProductOrder.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: HandleException, PUT_p_ucp_set_ProductOrder, change | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Get_Service.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Patch_Service.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: HandleException, formResponse, form_CacheId | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Post_Service.bpmn` | гранична подія; тип Native; функції: HandleException, p_ucp_set_ServiceOrder, proceedConfig | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF640_Service_Activation_and_Configuration/TMF640_Put_Service.bpmn` | гранична подія; тип Native; функції: HandleException, p_ucp_set_ServiceOrder, proceedConfig | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF653_Service_Test_Management/TMF653_POST_ServiceTest.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: HandleException, p_ucp_get_ServiceTest, proceedSessionParameters | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF654_PrepayBalance_Management/GET_AccumulatedBalance.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF654_PrepayBalance_Management/TMF654_GET_AccumulatedBalance.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF666_Account_Management/TMF666_Get_BillingAccount.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF666_Account_Management/TMF666_Post_BillingAccount.bpmn` | гранична подія; тип Native; функції: HandleException, p_ucp_set_BillingAccount_Dbss, proceedSessionParameters | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF666_Account_Management/TMF666_Put_BillingAccount.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: HandleException, formValidationError, p_ucp_set_BillingAccount_Dbss | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF677_Usage_Consumption_Management/TMF677_Get_QueryUsageConsumption.bpmn` | гранична подія; ексклюзивний шлюз; функції: HandleException, add_Cache, correct_Result | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF677_Usage_Consumption_Management/TMF677_Post_QueryUsageConsumption.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: HandleException, add_Cache_Status, correct_Empty_Result | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF678_Customer_Bill_Management/TMF678_BillingCycle.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF678_Customer_Bill_Management/TMF678_Get_AppliedCustomerBillingRate.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF678_Customer_Bill_Management/TMF678_Get_BillingCycle.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Delete_Topic.bpmn` | гранична подія; тип Native; функції: HandleException, p_ucp_del_EventTopic, proceedConfig | Action, Inline | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Get_Hub.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Get_Topic.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Get_Topic_Event.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Post_Topic.bpmn` | гранична подія; тип Native; функції: HandleException, p_ucp_set_EventTopic, proceedSessionParameters | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF688_Event_Management/TMF688_Put_Topic.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: HandleException, format_Validation_Error, p_ucp_set_EventTopic | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF724_Incident_Management/TMF724_POST_diagnoseIncident.bpmn` | гранична подія; ексклюзивний шлюз; тип Native; функції: RestApi, RestApi/GET, formatException | Action, Inline, Function | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |
| `TMF727_Service_Usage_Management/TMF727_Get_ServiceUsage.bpmn` | гранична подія; паралельний шлюз; ексклюзивний шлюз; тип Native; функції: HandleException, compose_ReadCacheResult, compose_WriteCacheResult | Action | `#Previous`, `#PreviousData`, `Input`, `Logger`, `Parameters` |

## Чого бракує для повного покриття

Не покрито жодним прикладом:

- режим ExternalAction

Покрито одним-двома прикладами, тобто фактично не перевіряється:

- Подієвий шлюз — 1
- Проміжна подія-перехоплювач — 2
- таймер — 1

