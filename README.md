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

![Diagram](/doc/architecture.jpg)


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

1. Create a customer in the Cuustomer service, via its REST API.
2. Create an order for the customer in the Orders service, via its REST API.
3. Call the `/award` API of the Points service, to get the number of points awarded to the customer.

### Example
```sh
$ ./demo.sh

# create a customer:
customer_id=$(curl -s -u $username:$password -H 'Accept: application/json; indent=4'\
    -H 'Content-Type: application/json' \
    -d '{"first_name": "Bart", "last_name": "Simpson", "date_established": "1980-02-23T00:00:00Z"}' \
    http://localhost:8001/api/customers/ | jq -r ".id")

echo ${customer_id}
31d71211-60b6-4e72-9b0c-e874583404c7

# create an order:
curl -s -u $username:$password -H 'Accept: application/json; indent=4'\
    -H 'Content-Type: application/json' \
    -d '{"customer_id": "'$customer_id'",  "item_count": 3340000}' \
    http://localhost:8002/api/orders/
{
    "id": "c341cd83-5297-4208-84bc-b09494d7774c",
    "customer_id": "31d71211-60b6-4e72-9b0c-e874583404c7",
    "date_placed": "2022-12-10T12:02:28.673825Z",
    "item_count": 3340000
}
# wait for eventual consistency...
sleep 2

# get points awarded
curl -H 'Accept: application/json; indent=4' -u $username:$password \
    http://localhost:8003/api/award/$customer_id/
{
    "points": 79523.80952380953
}
```
