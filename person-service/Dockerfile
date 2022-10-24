FROM python:3.9.15-slim-buster

RUN apt-get update && apt-get -y install gcc

RUN pip install -U pip

RUN python3 -m venv /venv

COPY ./requirements.txt ./code/requirements.txt
RUN . /venv/bin/activate; pip install -r /code/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code
ENV PATH /venv/bin:/bin:/usr/bin:/usr/local/bin

COPY . /code/

WORKDIR /code

CMD ["gunicorn", "service.wsgi"]
