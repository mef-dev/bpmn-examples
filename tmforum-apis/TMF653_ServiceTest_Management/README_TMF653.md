## TMF653 Service Test Management API

The **Service Test Management API TMF653** is a specialized endpoint designed to enable telecom operators to perform **on-demand testing of active services** using predefined test specifications.
MEF.DEV's implementation facilitates the validation and monitoring of live services in a flexible, standards-aligned manner.

This API serves a vital role in automated service assurance processes, helping telcos ensure the quality and accuracy of their services, especially in billing, rating, and network-specific operations.

### Key Features
* **On-Demand Test Execution**. Enables immediate testing of a specific service instance using a selected test specification (e.g., rating info validation)
* **Dynamic Evaluation**. Each test execution returns state, validity period, and custom characteristics gathered during the process
* **Multi-Network Compatibility**. Supports services across different network slices (e.g., 3G, 4G, 5G)
* **Integrated with Rating Function**. Can be used to retrieve real-time diagnostics characteristics like RAT-Type and Technology, charging ID, roaming status, etc

**You can try the TMF665 plugin as part of the platform's technical preview by following the link below.**
You can use this Postman collection to run the test locally or on the MEF.DEV platform. Make sure to configure your `{{API}}` environment variable to the correct base URL before executing.
