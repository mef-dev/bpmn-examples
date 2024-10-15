# Product Catalog

The catalog management API allows the management of the entire lifecycle of the catalog elements (product offerings, product offering prices, product specifications), the consultation of catalog elements during several processes such as ordering process, campaign management, sales management. The Product Catalog model allows a specification to be described by characteristics, described below.

## 	Characteristics
A characteristic is a name-value pair defining an aspect of the instantiated entity. The corresponding characteristic specification includes metadata such as:
• The name of the characteristic
• The value (data) type of the characteristic (could be simple or complex)
• Whether or not the value can be set at instantiation
• Whether or not the value must be supplied at instantiation, and the cardinality (how many values are allowed)
• List or range of allowed values

For example, a SMS Feature for mobile offers can be enabled or paused, thus it could be implemented as a characteristic describing the SMS access feature – for instance below:
• The name of the characteristic could be M2M SMS Access 
• The value type would be string
• The value is optional to be supplied – the default is Enable 
• It is a configurable characteristic –  two values are presented
• The valid values could be Enable or Pause
The Open API Product Catalog models is based on Characteristic-based approach instead of Schema-based. With Characteristic-based approach, the characteristics of the entity are specified dynamically, using the CharacteristicSpecification to define the behavior of the characteristic.

##	Multiple Catalogs
The Product Catalog Management API model supports multiple catalogs on base Network standards set. This allows service providers to expose multiple catalogs, for example for different sub-markets. Each catalog can have a different sub-category tree (namely Labels), so that the service provider can arrange the catalog elements by categories within the root categories (namely Prepaid and Postpaid subsriptions) in a way that meets the business needs of the specific catalog.
The underlying Product Offering catalog elements (namely Product Offering Market Segment, Product Offering Category) exist independently of the catalog(s) through which they are exposed. Thus, a direct search on any of these entities, without specifying a catalog, will retrieve the entities irrespective of the catalog(s)

##	Product Lifecycle Management
The Product Lifecycle Management, there is a requirement to distinguish between entities existing with different life cycle period (version) and accessible via different Sales Channels. For example, the same Product Offerings may exist in a Catalog but with different set of Tariffs. It is possible on base Historical Reprice of Tariffs of particular Product Offering, but in real life the most convenient way is based in Planned Reprise of Offering, namely from expiring to new one, namely with updated Tariffs. The precious one should be close for future activation from the Sales channels afterwords.

##	Product catalog view
The product catalog configuration used to illustrate Base and Extended scenarios is based on a bundle composed by the following product offerings, labeled with a Roles. The full Role’s list is presented below.
Base Products Specification marketed in Product Offering:
- `Mobile number` (or any kind of Network identifier) 
- `One Provisioning Unlimited Volume’s package` (role is ‘Base’), another one Recurring Subscription package with Dynamic Volume Tariffs conditions (role is ‘Override‘) and/or Set of Onetime Addon Packages with Fixed Volume Tariffs conditions (role is ‘Addon‘). This package’s set allows refreshing a balance of subscribed services (e.g set of voice minutes, GB of data or SMS) both ways in the beginning of new billing cycle and within the current billing cycle.
- `SIM Card` (linked to Mobile number)
Extended Products Specification marketed in Product Offering:
- `User Equipment` - smartphone, tablet, modem. This one is linked to Mobile number from the Base Products Specification.
- `One-Time Addon Package` with Fixed Free-of-charge Volume (role is ‘Grace-Activation‘). This is an optional package provided to the customer only ones after the Creation of Services. This package is usually valid only for one predefined period, namely till running out of volume.
These offers are linked with product specifications which will drive the product order execution. The characteristic values of the product specifications will depend on the offers selected by the customer and the information gathered during the order capture process.

##	Product Offering Sub Categories (Label Roles)
There are several Product Offering Roles within the BSS Template, namely:
- `Base`
The foundational Tariff Package designed to manage various consumption volumes efficiently. It forms the basis for handling all types of usage.
- `Override`
Allows the redefinition of the included amount of consumption volumes set by the Tariff Package (Base role). This role enables customization and flexibility in managing Post-Paid subscription-based consumption.
- `Addon`
An additional package providing a fixed volume of specific services. This extends the included amount of consumption volumes in the recurring subscription, allowing users to tailor their plans with extra services.
- `Grace-activation`
This package offers fixed free-of-charge volumes. Once these volumes are exhausted, the package will be automatically disabled by the service's start date. It provides a grace period for users to manage their usage effectively.
- `Individual`
Tailored for individual or non-public tariff conditions, this role allows personalized settings to meet specific user requirements.
-	Discount:
Functions as a marker for discount conditions. This Tariff Package serves as an indicator for applying discounts to the overall billing, providing a clear way to track and manage cost savings.
- `No_check`
Marker packages with a purpose defined by the LABEL value configured by the Configuration Team. This role allows for versatile use cases, adapting to specific needs as determined by the team configuring the system.
- `Loyalty`
Specifically designed for loyalty programs, this package offers non-monetary conditions to reward and incentivize users for their continued commitment. Ideal for fostering customer loyalty through special perks and benefits.

## Product Catalog Functionality

From a technical perspective, the Product catalog Management functionality supports the *productOffering* methods based on [BPMN Workflows](https://github.com/mef-dev/bpmn-examples/tree/dev/tmforum-apis/TMF620_Product_Catalog_Management) and allows users to query the catalog, market segments, and category of the resources