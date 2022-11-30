#!/usr/bin/env bash

docker container exec -it \
    ksqldb bash -c \
    "ksql-migrations --config-file /project/ksql-migrations.properties initialize-metadata; exit 0"

docker container exec -it \
    ksqldb bash -c \
    "ksql-migrations --config-file /project/ksql-migrations.properties apply --all; exit 0"