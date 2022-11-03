# Django / Kafka  - Microservices

Demo of a microservice architecture utilizing Django and Kafka.


- Microservices written in Python, using the Django framework.
- Examples of two types of event production: 
    - Transactional-Outbox pattern
    - Change-Data-Capture on domain model table
- Debezium Connector, deployed to ksqldb-server.
- Avro serialization.
- Schema Registry.
- ksqldb streams for event transformation.


## Architecture

![Diagram](/doc/Django-Kafka-Microservices.jpg)



## Run

This project uses [just](https://github.com/casey/just) commands.

The example set of services are run together in a single docker compose stack.  To get the demo working, run the following commands:

### Start up the stack:

```sh
just up
```
Leave this console running.  In a separate console, run the two following initialization scripts.

### Initialize the services:

```sh
just init-services
```

### Initialize ksqldb:
```sh
just init-ksqldb
```

---
#### Linux Environment Notes

The sh scripts may require exec permissions:
```sh
chmod +x wait-for-it.sh 
```

You may need to run the just commands with `sudo`  in order to run docker commands, e.g.:
```sh
sudo just up
```

---

## Demo

1. Access the person service admin site at [http://localhost:8001/admin/](http://localhost:8001/admin/).
2. Log in with username `root`, password `P@ssw0rd1`.
3. Create some person entities.

4. Access the accounting service admin site at [http://localhost:8002/admin](http://localhost:8002/admin) (same root credentials to log in).
5. Create some balance sheet entities.  For `Person id`, use `ID`s of persons that were created in the person service.

6.  Observe that the Planning Service's local `person` and `balance_sheet` tables are kept eventually consistent with the data from the person and accounting services.