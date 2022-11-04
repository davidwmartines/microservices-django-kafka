#!/usr/bin/env bash

docker container exec -it \
    microservices-django-kafka_ksqldb_1 bash -c \
    "ksql-migrations --config-file /project/ksql-migrations.properties initialize-metadata; exit 0"

docker container exec -it \
    microservices-django-kafka_ksqldb_1 bash -c \
    "ksql-migrations --config-file /project/ksql-migrations.properties apply --until 3; exit 0"