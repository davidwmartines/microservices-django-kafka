#!/usr/bin/env bash

username=root
password=P@ssw0rd1

set -v

# create a customer:
customer_id=$(curl -s -u $username:$password -H 'Accept: application/json; indent=4'\
    -H 'Content-Type: application/json' \
    -d '{"first_name": "Bart", "last_name": "Simpson", "date_established": "1980-02-23T00:00:00Z"}' \
    http://localhost:8001/api/customers/ | jq -r ".id")

echo ${customer_id}

# create an order:
curl -s -u $username:$password -H 'Accept: application/json; indent=4'\
    -H 'Content-Type: application/json' \
    -d '{"customer_id": "'$customer_id'",  "item_count": 3340000}' \
    http://localhost:8002/api/orders/

# wait for eventual consistency...
sleep 2

# get points awarded
curl -H 'Accept: application/json; indent=4' -u $username:$password \
    http://localhost:8003/api/award/$customer_id/