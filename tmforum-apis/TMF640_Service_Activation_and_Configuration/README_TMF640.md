# Service Activation and Configuration Management

The Service Activation and Configuration Management REST Application Programming Interface (API) encompasses all activities necessary to support the business/customer layer in delivering ordered services. This includes the facilitation of any changes, both inflight and post activation, as well as the overall lifecycle management of services.

This API enables the creation, modification, and retrieval of Product Order information. Although Product Orders are linked to Customer parties, it is imperative to note that the administration of parties lies beyond the scope of this API. The range of activities supported by this API includes:
- Creating a new service (in cases where the "by request" configuration option is applicable)
- Modifying inflight service creation (within the activation process)
- Activating an inactive service
- Retrieving service details
- Modifying existing services
- Suspending or restoring services
- Removing services
- Assigning service-related resources (pertaining to Resource Facing Services)

Despite the existence of different Product Order resources in the Telecom Forum (TMF) design, the WideCoup Business Support System (BSS) implementation excludes certain activities due to the Online mode of operations execution. These excluded activities include:
- Monitoring long-running service creation processes
- Creating inactive services
- Modifying inflight service creation
- Canceling inflight service creation
- Checking the feasibility of a service

All services can be accessed using the Customer Facing Service identifier provided within the Product Ordering, as well as using features of the service if applicable. It is noteworthy that services configured with the "by default" option will be instantiated automatically within the ProductOrder execution, akin to creating an inactive service, and SIM entity creation is anticipated within the activation procedure.

## Native Implementation within the BSS

Over recent years, the WideCoup BSS API [BSS.Entities](https://github.com/mef-dev/bss-entities) has evolved into an open API platform with diverse implementations from various external system consumers. The native implementation of TMF Service Activation and Configuration Management is rooted in established Entities and Actions, specifically `ServiceSubscriptions`, `Subscribers/Activate`, `Subscribers/changeStatus`, and `Subscribers/Deactivate`.

## Service Activation and Configuration Management Functionality

From a technical standpoint, the Service Activation and Configuration Management functionality supports the *Service* methods based on [BPMN Workflows](https://github.com/mef-dev/bpmn-examples/tree/dev/tmforum-apis/TMF640_Service_Activation_and_Configuration), encompassing all activities within the service lifecycle and the assignment of service-related resources. The Service lifecycle is monitored through the **'state'** attribute, with typical lifecycle values including `Creating`, `Active`, `Temporarily closed`, or `Closed`.

The mapping of `Service status` values to the appropriate `Status code` is as follows:

| Service state | Status code |
| -- | -- |
| Active | Activ |
| Temporarily closed | temp |
| Closed | close |

It is important to acknowledge that certain implementations may introduce additional states:
- The `Creating` state is a technical state indicating erroneous records within the BSS.
  The initial `Active` state is executed by the Activation procedure and is irreversible.
- The `Temporarily closed` state results in the force setting of the special `Pause` status for all features of a particular service. The reverse operation, changing the service status to `Active`, also returns the paused features of the service to Enable status (the `AfterFinBlock` status code).
- The final `Close` state is executed by the Deactivation procedure and is irreversible.

Conversely, the feature of the service is monitored by the **'isEnabled'** attribute and can be `True` or `False`.
In turn, the feature of the service is a list of feature characteristics, with each separate feature characteristic having its own **'Status'**