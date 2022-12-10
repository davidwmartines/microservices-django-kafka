# Points Service

Example of a points-awarding microservice.

The service's function is to award points to customers based on their orders placed.

The service consumes Customer events from Kafka to maintain a private store of customer information.

The service comsumes Order events from Kafka to maintain a private store of order data for each customer.

