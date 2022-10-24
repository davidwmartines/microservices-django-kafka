#rebuild images
build:
    sudo docker-compose build

#start
start:
    sudo docker-compose up

# shell into a person service
person-service-shell:
    sudo docker-compose run --rm -w /code person-service-web bash

# psql into the postgres service container
psql:
    sudo docker container exec -it microservices-django-kafka_postgres_1 psql -U postgres