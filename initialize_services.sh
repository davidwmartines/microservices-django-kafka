#!/usr/bin/env bash

echo "Running Django Migrations for the Orders Service"
docker compose run --rm \
    orders-service-web bash -c "./manage.py migrate --no-input"

echo "Creating a superuser in the Orders Service"
docker compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@ssw0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    orders-service-web bash -c "./manage.py createsuperuser --no-input"

echo "Running Django Migrations for the Customer Service"
docker compose run --rm \
    customer-service-web bash -c "./manage.py migrate --no-input"

echo "Creating a superuser in the Customer Service"
docker compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@ssw0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    customer-service-web bash -c "./manage.py createsuperuser --no-input"

echo "Running Django Migrations for the Points Service"
docker compose run --rm \
    points-service-web bash -c "./manage.py migrate --no-input"

echo "Creating a superuser in the Points Service"
docker compose run --rm \
    -e DJANGO_SUPERUSER_PASSWORD=P@ssw0rd1 \
    -e DJANGO_SUPERUSER_USERNAME=root \
    -e DJANGO_SUPERUSER_EMAIL=root@root.com \
    points-service-web bash -c "./manage.py createsuperuser --no-input"
