# Usage Consumption Management

The Usage Consumption Management, inclusive of the QueryUsageConsumption method, encompasses the assessment of consumption levels associated with products, services, or resources pertaining to one or more parties. This method facilitates the retrieval of information concerning remaining, global, or utilized bucket values, including instances of exceptional consumption commonly referred to as out-of-bucket consumption.

The Usage Consumption Application Programming REST Interface (API) provides the following operations:
- A listing of existing usage consumption queries based on filter criteria.
- Retrieval of an existing usage consumption query by its identifier.
- Creation of a new query for usage consumption
 
Despite the existence of diverse Usage Consumption API resources within the Telecom Forum (TMF) design, the implementation within the WideCoup Business Support System (BSS) excludes certain activities due to the Online mode of operations execution. These excluded activities encompass:
- Deletion of an existing query for usage consumption.
- Notification of events, specifically QueryUsageConsumption creation or removal events.

## Service Activation and Configuration Management Functionality

From a technical standpoint, the Service Activation and Configuration Management functionality supports the *QueryUsageConsumption* methods based on [BPMN Workflows](https://github.com/mef-dev/bpmn-examples/tree/dev/tmforum-apis/TMF677_Usage_Consumption_Management), encompassing all requests within the query lifecycle includind server paging, filtering and sorting of existing usage consumption.