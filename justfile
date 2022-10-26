#rebuild images
build:
    sudo docker-compose build

# start up
up:
    sudo docker-compose up

# shut down
down:
    sudo docker-compose down

# shell into a person service container
shell-person:
    sudo docker-compose run --rm -w /code person-service-web bash

# psql into the postgres service container
psql:
    sudo docker container exec -it microservices-django-kafka_postgres_1 psql -U postgres

# ksql shell
ksql:
    sudo docker container exec -it microservices-django-kafka_ksqldb_1 ksql

# take ownership of all the files, such as those created by docker
own:
    sudo chown -R $USER .