# rebuild images
build:
    docker compose build

# start up
start:
    docker compose up

# shut down and terminate the stack
terminate:
    docker compose down

# initialize the Django services.  Performs database migrations and creates a superuser account in each.
init-services:
    ./initialize_services.sh

# creates the streams and connectors in ksqldb.
init-ksqldb:
    ./ksqldb/migrate.sh

# shell into a person service container
shell-person:
    docker compose run --rm person-service-web bash

# shell into a person service container
shell-planning:
    docker compose run --rm planning-service-web bash

# shell into an accounting service container
shell-accounting:
    docker compose run --rm accounting-service-web bash

# psql into the postgres service container
psql:
    docker container exec -it postgres psql -U postgres

# ksql shell
ksql:
    docker container exec -it ksqldb ksql

# schema-registry shell
shell-schema-registry:
    docker container exec -it schema-registry bash

# take ownership of all the files, such as those created by docker
own:
    chown -R $USER .

# start a console consumer on a topic
consume topic:
    docker run -it --network microservices-django-kafka_default edenhill/kcat:1.7.0 -b kafka:9092 -C -t {{topic}} -f 'Topic %t [%p] at offset %o: key %k: headers %h: %s\n'


# run black and flake8
lint:
    black --preview . && flake8 .
