#!/usr/bin/env bash

docker-compose run --rm \
    accounting-service-web bash -c "./manage.py migrate --no-input"

docker-compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@$$w0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    accounting-service-web bash -c "./manage.py createsuperuser --no-input"

docker-compose run --rm \
    person-service-web bash -c "./manage.py migrate --no-input"

docker-compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@$$w0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    person-service-web bash -c "./manage.py createsuperuser --no-input"

docker-compose run --rm \
    planning-service-web bash -c "./manage.py migrate --no-input"

docker-compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@$$w0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    planning-service-web bash -c "./manage.py createsuperuser --no-input"
