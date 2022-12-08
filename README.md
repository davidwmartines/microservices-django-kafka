# Django / Kafka  - Microservices

Demo of a microservice architecture utilizing Django and Kafka.

The primary goal of this example is to demonstrate achieving robust eventual-consistency of domain data between independent microservices, using an event-driven architecture.


- Microservices written in Python, using the Django framework.
- Services have no inter-dependencies. They are coupled only to canonical event schemas.
- Examples of two types of event production: 
    - Transactional-Outbox pattern
    - Change-Data-Capture on domain model table
- Uses the Debezium Connector, deployed to ksqldb-server.
- Events are serialized using Avro.
- Schemas are stored in the Schema Registry.


## Architecture

![Diagram](/doc/Django-Kafka-Microservices.jpg)


## Run

This project uses [just](https://github.com/casey/just) commands.

The example set of services are run together in a single docker compose stack.  To get the demo working, run the following commands:

### Start up the stack:

```sh
just start
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

Install docker-compose-plugin.

The sh scripts may require exec permissions:
```sh
chmod +x ./initialize_services.sh
chmod +x ./ksqldb/migrate.sh
chmod +x ./demo.sh
```

You may need to run the just commands with `sudo`  in order to run docker commands, e.g.:
```sh
sudo just start
```

---

## Demo

Run the `demo` script.

This will:

1. Create a person in the Person service, via its REST API.
2. Create a balance-sheet for the person in the Accounting service, via its REST API.
3. Call the `/ratios` API of the Planning service, to get financial planning ratio data for the person.

### Example
```sh
$ ./demo.sh

# create a person:
person_id=$(curl -s -u $username:$password -H 'Accept: application/json; indent=4'\
    -H 'Content-Type: application/json' \
    -d '{"first_name": "Bart", "last_name": "Simpson", "date_of_birth": "1980-02-23T00:00:00Z"}' \
    http://localhost:8001/api/persons/ | jq -r ".id")

echo ${person_id}
10cdc09d-757c-4e4f-96bc-367a7de72f70

# create a balance sheet:
curl -s -u $username:$password -H 'Accept: application/json; indent=4'\
    -H 'Content-Type: application/json' \
    -d '{"person_id": "'$person_id'",  "assets": 3340000, "liabilities": "537300"}' \
    http://localhost:8002/api/balance-sheets/
{
    "id": "8ab01372-1e2e-493a-88b6-da171b116ef2",
    "person_id": "10cdc09d-757c-4e4f-96bc-367a7de72f70",
    "date_calculated": "2022-12-08T04:41:29.568289Z",
    "assets": 3340000,
    "liabilities": 537300
}
# wait for eventual consistency...
sleep 1

# get financial planning data
curl -H 'Accept: application/json; indent=4' -u $username:$password \
    http://localhost:8003/api/ratios/$person_id/
[
    {
        "name": "Net Worth to Total Assets",
        "result": {
            "ratio": 0.8391317365269461,
            "benchmark": 0.5,
            "status": "Good"
        }
    }
```
