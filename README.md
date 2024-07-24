# reference_data_api

A learning and development/python/fast-api/reference-data api that currently returns details of countries.

## To seed data

python database_seeder.py

## To run tests

pytest

## To run the server

uvicorn reference_data_app.main:app --reload

## Docker

### To build docker image

docker build -t myimage .

### To run the docker container

docker run -d --name mycontainer -p 8000:8000 myimage
