# FROM python:slim-bookworm
FROM python:3.11-slim


# Install PostgreSQL development libraries
RUN apt-get update && \
    apt-get install -y cmake libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

#install requirements
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt 

WORKDIR /app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./app /app/app
