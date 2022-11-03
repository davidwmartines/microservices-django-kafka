#!/usr/bin/env bash

echo "Running Django Migrations for the Accounting Service"
docker-compose run --rm \
    accounting-service-web bash -c "./manage.py migrate --no-input"

echo "Creating a superuser in the Accounting Service"
docker-compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@ssw0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    accounting-service-web bash -c "./manage.py createsuperuser --no-input"

echo "Running Django Migrations for the Person Service"
docker-compose run --rm \
    person-service-web bash -c "./manage.py migrate --no-input"

echo "Creating a superuser in the Person Service"
docker-compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@ssw0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    person-service-web bash -c "./manage.py createsuperuser --no-input"

echo "Running Django Migrations for the Planning Service"
docker-compose run --rm \
    planning-service-web bash -c "./manage.py migrate --no-input"

echo "Creating a superuser in the Planning Service"
docker-compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@ssw0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    planning-service-web bash -c "./manage.py createsuperuser --no-input"
