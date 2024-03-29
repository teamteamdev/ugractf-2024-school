FROM python:3.12

RUN apt update && apt install -y tcpdump curl

WORKDIR /app
RUN pip install --no-cache poetry
COPY pyproject.toml poetry.lock /app/
COPY epkp/__init__.py /app/epkp/
RUN poetry config virtualenvs.create false && poetry install -n --no-cache --only main

COPY . /app
