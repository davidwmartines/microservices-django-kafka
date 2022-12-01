FROM python:3.9.15-slim-buster

RUN apt-get update && apt-get -y install gcc && apt-get -y install curl

RUN pip install -U pip

RUN python3 -m venv /venv

# note: This docker-compose build uses the parent directory build context
# hence the need to use /person-service/ in these paths.
# This is done in order to include the events-lib directory as pip installable.
# Normally we would just use "." to use the directory containing the Dockerfile
# as the build context.

COPY ./person-service/requirements.txt ./code/requirements.txt
COPY ./events/ ./events
RUN . /venv/bin/activate; pip install -r /code/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code
ENV PATH /venv/bin:/bin:/usr/bin:/usr/local/bin

COPY ./person-service/ /code/

WORKDIR /code

CMD ["gunicorn", "service.wsgi"]
