# Service Usage Management

The Service Usage Management REST API incorporates the ServiceUsage method, offering a standardized mechanism for the management of service usage. This includes the retrieval and export of a collection of service usages. The creation option for service usage is reserved for future utilization, given the diverse Extract, Transform, Load (ETL) scenarios provided within the Widecoup Business Support System (BSS) solution.

A service usage, in this context, denotes an instance of usage on a Service derived from various Resource usages. These usages can be further employed by Omni-channels or other systems to disseminate Product usage values. Each service usage is characterized by attributes, representing its inherent properties. The ServiceUsage API facilitates the following operations on the ServiceUsage resource:
- Retrieval of a ServiceUsage or a collection of ServiceUsage, contingent on filter criteria.

Furthermore, the ServiceUsageSpecification entity within the BSS Template establishes a standardized mechanism for the management of service usage specifications. This encompasses the handling of custom sets of service usage characteristics. The Service Usage Specification offers a detailed description of a service usage event, capturing attributes of interest to the business. Similar to ServiceUsage, it is comprised of characteristics that define all attributes known for a specific type of usage.

Despite the existence of different Service Usage API resources within the TeleManagement Forum (TMF) design, the implementation within the WideCoup BSS excludes certain activities due to the Online mode of operations execution.  Specifically, the excluded activities are as follows:
- Creation of a ServiceUsage
- Partial update of a ServiceUsage or a collection of ServiceUsage
- Creation of a ServiceUsageSpecification
- Partial update of a ServiceUsageSpecification or a collection of ServiceUsageSpecification

## Service Usage Management Functionality

From a technical standpoint, the Service Usage Management functionality supports the *ServiceUsage* methods based on [BPMN Workflows](https://github.com/mef-dev/bpmn-examples/tree/dev/tmforum-apis/TMF727_Service_Usage_Management), enabling the retrieval of a ServiceUsage or a collection of ServiceUsage, contingent on filter criteria.