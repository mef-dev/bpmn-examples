# Customer Bill Management

The Customer Bill Management API encompasses business entities integral to Rating and Billing processes, providing operations for the identification and retrieval of details regarding applied customer billing rates for products subscribed by a customer. Typically, these products are rated at varying prices determined by product offering prices, pricing rules, and additional terms and conditions specified by the customer. The rating process involves the application of rates to product usages, while the billing process further incorporates additional charges (recurring charges, one-time charges), discounts, and taxes to products. The aggregated applied rates culminate in bills sent to customers. The bill, the ultimate outcome of the billing process, can be generated through a cycle run (usually executed in batches) or as a result of events such as a customer request or account termination (handled in real-time).

The Customer Bill Management REST API facilitates the retrieval of information pertaining to one or multiple customer bills (also referred to as invoices) generated for a customer. A customer bill serves as an electronic or paper document produced at the conclusion of the billing process, consolidating and displaying various items (applied customer billing rates generated during the rating and billing processes) to be charged to a customer. It represents the total amount due for all products during the billing period, encompassing critical information such as dates and bill references. The Customer Bill Management REST API model accommodates the requirements for three fundamental billing types: postpaid periodical bill, postpaid real-time bill, and prepaid real-time bill.

Furthermore, this API allows for the identification and retrieval of details related to bill cycles.

## Native Implementation within the BSS

Over recent years, the WideCoup Billing (REST) API [BSS.Entities](https://github.com/mef-dev/bss-entities) has evolved into an open API platform with diverse implementations by various external system consumers. The native implementation of TMF Product Ordering management is grounded in established Entities and Actions, specifically `BillingTasks`, `Customers/CalcCharges`, and `Subscribers/Recharge`.

Despite the existence of different Customer Bill Management resources in the Telecom Forum (TMF) design, such as the real-time request for customer bill creation and its management, the implementation within the WideCoup Business Support System (BSS) exclusively incorporates appliedCustomerBillingRate and billCycle due to support for external BSS synchronization.

## Customer Bill Management Functionality

From a technical standpoint, the Customer Bill Management functionality supports the *appliedCustomerBillingRate* and *billCycle* methods based on [BPMN Workflows](https://github.com/mef-dev/bpmn-examples/tree/dev/tmforum-apis/TMF678_Customer_Bill_Management), enabling:
- The display of applied billing rates created before or during the billing process.
- The retrieval of a detailed description of a billing cycle and its various sub-steps.

Bills are typically generated within a regular bill cycle labeled `onCycle`. In cases where the bill is produced on request, such as a customer request, it is indicated as `offCycle`.

Typical lifecycle values for a billing cycle include:
- `new`: Bills are prepared for validation or sending.
- `validated`: Bills are examined through manual or automatic checks.
- `sent`: Bills are dispatched through the designated channel.
- `onHold`: Bills are temporarily withheld from further processing until issues associated with the bill are resolved.