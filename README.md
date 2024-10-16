# BPMN-based flow examples for execution within the MEF.DEV Enterprise Integration platform

### Table of Contents
1. [Account Management TMF666](#Account-Management-TMF666)
2. [Product Ordering TMF622](#Product-Ordering-TMF622)
3. [Service Activation and Configuration TMF640](#Service-Activation-and-Configuration-TMF640)
4. [Service Usage Management TMF727](#Service-Usage-Management-TMF727)
5. [Usage Consumption Management TMF677](#Usage-Consumption-Management-TMF677)
6. [Customer Bill Management TMF678](#Customer-Bill-Management-TMF678)
7. [Product Catalog Management TMF620](#Product-Catalog-Management-TMF620)
8. [Prepay Balance Management TMF654](#Prepay-Balance-Management-TMF654)
9. [Event Management TMF688](#Event-Management-TMF688)
10. [Incident Management TMF724](#Incident-Management-TMF724)
11. [Resources and Useful Links](#Resources-and-Useful-Links)

## Account Management TMF666
The "Account Management TMF666" API establishes a standardized mechanism for billing and settlement accounts administration. This ensures a seamless process within both B2C and B2B contexts. The API facilitates the creation, modification, and retrieval of account information, operating within the scope of diverse account entities such as FinancialAccount, PartyAccount, BillingAccount, and SettlementAccount.

The minimal implementation exclusively encompasses the BillingAccount entity. This strategic focus streamlines access to all accounts using either the Account internal identifier or the Customer ID. Notably, in creating a BillingAccount from inception, the utilization of Customer entity creation is anticipated, accompanied by external identifiers for future synchronization purposes.

## Product Ordering TMF622
The "Product Ordering TMF622" API emerges as a cornerstone in the telecom evolution, providing a standardized mechanism for initiating and tracking product orders. MEF.DEV's implementation within WideCoup BSS ensures flexibility and efficiency, allowing the creation, modification, and retrieval of product order information. This standardized approach simplifies transactions between customers, service providers, and partners, highlighting the transformative power of open APIs.

In the intricate tapestry of telecom operations, Product Ordering API represents a specific type of order that enables transactions between a customer and a service provider or between a service provider and a partner. The API permits the creation, modification, and retrieval of Product Order information, where Product Orders are intricately associated with Customer parties.

Despite the existence of different Product Order resources in the TM Forum design, the minimal implementation exclusively incorporates the Product Order due to the Online mode of order execution. This strategic alignment underscores the practicality and efficiency gained through the focus on specific functionalities, contributing to a streamlined and agile telecom ecosystem.

## Service Activation and Configuration TMF640
The "Service Activation and Configuration TMF640" API embodies the essence of service lifecycle management. MEF.DEV's implementation empowers communication service providers to create, modify, and retrieve product order information seamlessly. Despite the diverse activities supported by this API, the focus remains on the business/customer layer, exemplifying how standardized open APIs drive efficiency in delivering ordered services.

This comprehensive API covers a spectrum of activities necessary to support the business/customer layer in delivering ordered services. From creating new services to modifying inflight service creation and overall lifecycle management, the API ensures a holistic approach to service activation and configuration.

Activities such as monitoring long-running service creation processes, creating inactive services, modifying inflight service creation, and canceling inflight service creation are not required for minimal implementation This strategic decision aligns with the need for a seamless and rapid execution model, contributing to the efficiency of the service activation and configuration processes.

## Service Usage Management TMF727
Precision in managing service usage is paramount, and the "Service Usage Management TMF727" API encapsulates this need. It incorporates the ServiceUsage method, offering a standardized mechanism for the management of service usage. This includes the retrieval and export of a collection of service usages. The creation option for service usage is successfully complemented by ETL features, given the diverse Extract, Transform, and Load scenarios.

In this context, a service usage denotes an instance of usage on a Service derived from various Resource usages. These usages can be further employed by Omni-channels or other systems to disseminate Product usage values. Each service usage is characterized by attributes, representing its inherent properties. The ServiceUsage API facilitates the retrieval of a ServiceUsage or a collection of ServiceUsage, contingent on filter criteria.

Furthermore, the ServiceUsageSpecification entity within the BSS Template establishes a standardized mechanism for the management of service usage specifications. This encompasses the handling of custom sets of service usage characteristics. The ServiceUsageSpecification offers a detailed description of a service usage event, capturing attributes of interest to the business.

Similar to ServiceUsage, it is comprised of characteristics that define all attributes known for a specific type of usage. Specifically, the optional for implementation activities are the creation of a ServiceUsage, partial update of a ServiceUsage or a collection of ServiceUsage, creation of a ServiceUsageSpecification, and partial update of a ServiceUsageSpecification or a collection of ServiceUsageSpecification.

This optionality aligns with the online execution model, focusing on the retrieval and export functionalities while reserving specific activities for future scenarios. By navigating this delicate balance, MEF.DEV ensures that the Service Usage Management API remains a robust and efficient tool for managing service usage within the ever-evolving telecom landscape.

## Usage Consumption Management TMF677
The "Usage Consumption Management TMF677" API encompasses the assessment of consumption levels associated with products, services, or resources pertaining to one or more parties. This method facilitates the retrieval of information concerning remaining, global, or utilized bucket values, including instances of exceptional consumption commonly referred to as out-of-bucket consumption. The Usage Consumption API provides the following operations: a listing of existing usage consumption queries based on filter criteria, retrieval of an existing usage consumption query by its identifier, and creation of a new query for usage consumption.

Despite the existence of diverse Usage Consumption API resources within the TM Forum design, the minimal implementation doesn’t require certain activities due to the Online mode of operations execution. These optional activities encompass the deletion of an existing query for usage consumption and notification of events, specifically QueryUsageConsumption creation or removal events.

This strategic approach ensures that the Usage Consumption Management API within WideCoup BSS aligns with the online execution model, focusing on efficient retrieval and creation functionalities while maintaining flexibility for future utilization. As the telecom industry continues to evolve, the ability to assess and manage consumption levels with precision becomes a critical factor in delivering exceptional services to end-users.

## Customer Bill Management TMF678
In the realm of billing and invoicing, the "Customer Bill Management TMF678" API emerges as a game-changer. MEF.DEV's implementation facilitates the identification and retrieval of customer bills, providing a comprehensive view of applied customer billing rates. This standardized approach streamlines the billing process, demonstrating how open APIs can revolutionize rating and billing processes in telecom.

The Customer Bill Management API encompasses business entities integral to Rating and Billing processes, providing operations for the identification and retrieval of details regarding applied customer billing rates for products subscribed by a customer. Typically, these products are rated at varying prices determined by product offering prices, pricing rules, and additional terms and conditions specified by the customer.

The Customer Bill Management REST API facilitates the retrieval of information from one or multiple customer bills (also referred to as invoices) generated for a customer. A customer bill serves as an electronic or paper document produced after the billing process, consolidating and displaying various items (applied customer billing rates generated during the rating and billing processes) to be charged to a customer. It represents the total amount due for all products during the billing period, encompassing critical information such as dates and bill references.

This API model accommodates the requirements for three fundamental billing types: postpaid and prepaid periodical bills, as well as bill operation by request, and bills with scheduled installment payment guidelines. Furthermore, this API allows for the identification and retrieval of details related to bill cycles. By offering standardized operations for the identification and retrieval of customer billing rates, the API ensures that communication service providers can deliver accurate and timely bills to their customers. The flexibility to accommodate different billing types further enhances the adaptability of the solution to diverse business models within the telecom industry.

|![TMF Open APIs](https://github.com/mef-dev/bpmn-examples/blob/dev/tmforum-apis/tmforum-apis.png)|
| :--: |

## Product Catalog Management TMF620
The Product Catalog Management API supports the lifecycle of catalog elements, such as product offerings, prices, and specifications, essential for processes like ordering and campaign management. It uses a characteristic-based model, where entity attributes are dynamically specified.

This approach provides flexibility, enabling service providers to expose multiple catalogs for different markets, with independent product offerings that can be searched across catalogs. The API supports product lifecycle management, including versioning and tariff updates. It also offers various product roles (Base, Override, Addon) to manage product offerings, ensuring tailored and efficient service delivery.

## Prepay Balance Management TMF654
The Prepay Balance Management API tracks and manages balances for prepay users, ensuring they have sufficient funds to use services. It handles both monetary balances and non-monetary "buckets" (e.g., SMS or data). Users can transfer credit between accounts, and operators offer multiple recharge channels.

When a customer acquires a product, balances and buckets are created to track voice, data, and SMS usage. Each balance and bucket is uniquely identified for tracking and top-ups. The API also supports accumulated balance methods, retrieving credit, reserved amounts, loyalty bonuses, and other account details.

## Event Management TMF688
The "Event Management TMF688" API enhances event handling and communication in telecom networks, allowing providers to deliver superior services. It supports large-scale distributed publishing and subscription for events from various Event Producers, facilitating diverse event-based architectures and seamless network communication.

The API integrates efficiently within the WideCoup Business Support System, leveraging established entities like multi-threaded tasks for smooth operation. It offers functionalities for managing Topic and Event resources, enabling users to subscribe to events, receive notifications via callback APIs, and access event details, such as alarms categorized by predefined standards. Understanding the lifecycle of events—transitioning through states like raised, updated, and cleared—is vital for effective management and responsiveness in telecom operations.

## Incident Management TMF724
Incident Management enhances NOC engineers' efficiency by using advanced AI, LLMs, and real-time data to manage and resolve incidents. The process starts with engineers prompting the Co-Pilot, which orchestrates tasks by selecting agents from its repository. The Network Incident Agent refines the prompt, accessing a Vectorized Knowledge Base and real-time network data. AI models like GPT-4 and LLaMa3 help provide sophisticated responses.

The MEF.DEV platform performs Root Cause Analysis, generating a resolution using the TMF724 API model. The Co-Pilot can integrate vendor-specific workflows for category-based incident diagnosis, such as device-based incidents, network-based incidents, etc.

## Resources and Useful Links
For a technical preview of the MEF.DEV platform and additional information, feel free to use the following links.
- [Join the technical preview](https://preview.mef.dev/rflnk/wsvfcV0ECUiTog2b%2Fv2PmCJMkMdhSXKjoyJe5Ziwl6L2%2FsEhxbNHs0%2FK9YZqm%2Bxt).
- [The MEF.DEV platform documentation](https://platform.mef.dev/plugin_basics/introduction.md).
- [How to create the First Angular plugin](https://platform.mef.dev/dev_guides/first_ui_plugin.md).
- [How to create the First Backend plugin](https://platform.mef.dev/dev_guides/first_backend_plugin.md).
- [How to create Complex Angular & Backend plugin](https://platform.mef.dev/dev_guides/portal_plugin.md).
- [UI Kit Demo and documentation](https://platform.mef.dev/ui_kit_demo/app/home).
- [Docker compose repository](https://github.com/mef-dev/docker) to run the MEF.DEV platform in-house using Docker.
- [Kubernetes cluster repository](https://github.com/mef-dev/k8s) to run the MEF.DEV platform in-house using Kubernetes.
- For [QA & Online support](https://t.me/mef_dev_support) please feel free to join our Telegram channel. Our team operates 24/7 and would be glad to provide all the needed assistance and support.

The MEF.DEV team also has a dedicated community on LinkedIn. We would be delighted to see you among dozens of IT Engineers and Software Developers.
[Join us](https://www.linkedin.com/groups/9050042/) and let's reshape the Digital Transformation world together.
