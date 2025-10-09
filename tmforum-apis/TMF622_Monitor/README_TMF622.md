# Monitor Management

The TMF API Monitor REST Application Programming Interface (API) provides a standardized mechanism for observing, tracking, and analyzing the **'operational state of asynchronous operations'** within the MEF.DEV ecosystem.
It ensures continuous visibility into execution results, response times, and diagnostic information of batch TMF-based interactions — such as Product Ordering, Service Configuration, and Resource Management.

This API enables the retrieval of Monitor entity information, where each Monitor is associated with a heterogeneous batch operation derived from TMF Order resources.

While the TM Forum (TMF) design specifies atomic PUT operations for Order resources — for example, PUT ProductOrder or PUT ServiceOrder — the WideCoup Business Support System (BSS) implementation instead adopts the **'PATCH'** operation model to handle offline and asynchronous batch order updates.
Each Monitor instance can be accessed using the Monitor identifier, which is returned in the `Location` response header of the corresponding PATCH request.

## Native Implementation within the WideCoup BSS

Over recent years, the WideCoup BSS API [BSS.Entities](https://github.com/mef-dev/bss-entities) has matured into an open API platform with numerous implementations from various external system consumers. The native implementation of TMF Monitor Management is built upon established BSS entities and actions — primarily `WorkEvents` and `Tasks` — which handle the orchestration, logging, and lifecycle management of monitored operations.

## Monitor Management Functionality

From a technical standpoint, the Monitor Management functionality supports the *Monitor* methods based on [BPMN Workflows](https://github.com/mef-dev/bpmn-examples/tree/dev/tmforum-apis/TMF622_Monitor). These workflows facilitate the retrieval of Monitor data and lifecycle tracking for batch processes initiated by asynchronous TMF operations.

Each Monitor entity maintains a state attribute that reflects its lifecycle stage, which in turn depends on the items.state attribute of individual batch items.
Typical lifecycle values for a Monitor include:
- `InProgress` – the monitored operation is currently being executed.
- `Completed` – the monitored operation has finished successfully.
- `InError` – one or more batch items have failed.

When a Product Order or related operation is submitted with a Priority greater than `1`, it triggers an offline execution mode, which may result in an InError state if issues occur during background processing.

The lifecycle values of individual Monitor Items generally align with their corresponding Order Item states. However, specific implementations may introduce additional custom states to accommodate extended or vendor-specific workflows.