# Planning Service

Example of a financial planning microservice.

The service's function is to create financial plans for people.  The finanacial plans are based on using information about the person, including their demographic and finanacial information.

The service consumes Person events from Kafka to maintain a private store of person demographic information.

The service comsumes BalanceSheet events from Kafka to maintain a private store of balance-sheet data for each person.

