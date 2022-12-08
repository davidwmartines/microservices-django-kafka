#!/usr/bin/env bash

username=root
password=P@ssw0rd1

set -v

# create a person:
person_id=$(curl -s -u $username:$password -H 'Accept: application/json; indent=4'\
    -H 'Content-Type: application/json' \
    -d '{"first_name": "Bart", "last_name": "Simpson", "date_of_birth": "1981-01-01T00:00:00Z"}' \
    http://localhost:8001/api/persons/ | jq -r ".id")

echo ${person_id}

# create a balance sheet:
curl -s -u $username:$password -H 'Accept: application/json; indent=4'\
    -H 'Content-Type: application/json' \
    -d '{"person_id": "'$person_id'",  "assets": 3340000, "liabilities": "537300"}' \
    http://localhost:8002/api/balance-sheets/





# echo "list persons..."
# curl -H 'Accept: application/json; indent=4' -u $username:$password \
#     http://localhost:8001/api/persons/