# Prepay Balance Management

Prepay users pay up front before using services. Therefore, the users must have sufficient balance to use these services. The purpose of this the Prepay Balance Management API is to manage and track these balances, monetary at the first, namely core or additional account balances. 

For the non-monetary balances, namely buckets, the well-designed Usage Consumption management is available. A bucket represents an entity that keeps track of the balance available to use services. Every bucket will measure balance in different units, it can be monetary or non-monetary (for example a number of SMS that are available or the number of GB of data that are available).

In case of monetary balances, Users can pass credit between different account balance, therefore transferring balance from one account balances to another. Operators can provide multiple recharge channels to top up these balances to increase the balance to use for services.

When a customer acquires a product offered by a service provider, the fulfilment process creates a set of balances and bucket’s entities to track the balance for the services that comprise the product. As a  part of the instantiation of a mobile line product, the fulfilment process creates voice, data and SMS buckets that are associated to the product and provisioned to the network core. The process creates a prepaid account in the WideCoup Billing System and a related entry for the Customer Facing Services database.

Each account balance and bucket has its own unique id assigned to it during the fulfilment process. This id uniquely identifies the account balance when topping up the balance on the account or any other of the actions that can be perform on it. Each core account can have an association with more than one product. This enables consumers to share services, for example in data bundles or pool volumes. 


## Prepay Balance Management Functionality

From a technical perspective, the Prepay Balance Management functionality supports the *AccumulatedBalance* methods based on [BPMN Workflows](https://github.com/mef-dev/bpmn-examples/tree/dev/tmforum-apis/TMF654_PrepayBalance_Management) and allows a consumer to retrieve an aggregation of amounts for many account balances, namely described below (масив `accountBalance[balanceType]`)
- `credit` amount, if available
- `reserved` amount, calculated on reservations value awaiting accept
- `accepted` amount, calculated on reservations value awaiting charging after accept
- `loyalty` value in bonus unit, if available
- `billing` amount from the last billing cycle
- `receivable` amount, namely expected value to be change on the current date for prepaid