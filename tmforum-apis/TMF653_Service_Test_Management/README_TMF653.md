## TMF653 Service Test Management API

The TMF653 Service Test Management API provides a standardized mechanism for telecom operators to perform **on-demand validation of active services** using predefined Test Specifications within the MEF.DEV ecosystem.
It ensures consistent verification of deployed service instances and their related charging or configuration data by executing automated test workflows in default synchronous mode.

A Service Test, in this context, represents a technical validation process that evaluates the operational state and quality of a specific service instance or a group of service components.
Such validation may include connectivity, rating, or charging verification across mobile, M2M, or fixed-line domains.
Each Service Test retrieves and evaluates operational characteristics such as session identifiers, Charging IDs, Access Point Names (APNs), RAT types, and roaming contexts to confirm service correctness and compliance with expected network behavior.

### Native Implementation within the WideCoup BSS

Over recent years, the [NRF Rating API](https://app.swaggerhub.com/apis/MEF.DEV/nrf-rating/1.1.5) has evolved into a robust implementation of Class B operations on the 3GPP Re interface, providing real-time interaction between service control and charging functions. The native implementation of TMF653 Service Test Management builds upon this foundation, supporting dynamic credit limit updates and multiple charging levels (session-level and service-level) across both prepaid and postpaid service delivery models.

This approach allows operators to validate not only service configuration but also end-to-end charging logic during active service sessions — ensuring billing accuracy, quality assurance, and customer experience consistency.

###  Service Test Management Functionality

From a technical standpoint, the Service Test Management functionality supports the *ServiceTest* methods defined through [BPMN Workflows](https://github.com/mef-dev/bpmn-examples/tree/dev/tmforum-apis/TMF653_ServiceTest_Management), enabling the creation, execution, and state tracking of Service Tests throughout their lifecycle.

Each Service Test entity maintains a state attribute that reflects the execution progress and result status, which depend on the underlying workflow and service event responses.
Typical lifecycle values for a Service Test include:
- `Completed` – The test finished successfully, and all required results were collected.
- `Failed` – The test execution encountered operational or validation errors.

Depending on the implementation, the lifecycle can be extended with additional states, such as:
- `Acknowledged` – The test request has been received and accepted.
- `InProgress` – The test execution is currently in progress.
- `Canceled` – The test was terminated before completion.

Each Service Test may include multiple characteristics (test items) such as M2M_SMS, M2M_DTE, or M2M_VCE, each representing a domain-specific validation (for example, message delivery, data session establishment, or voice call verification). These characteristics encapsulate detailed diagnostic parameters — including ChargingID, ChargingCause, sgsnMccMnc, and Roaming status — enabling precise correlation between service configuration, mediation data, and real-time network events.

