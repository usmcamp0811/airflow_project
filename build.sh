#!/bin/bash

docker build -t puckel-airflow-with-docker-inside:latest --build-arg DOCKER_ID=$(getent group docker | awk -F ":" '{ print $3 }') .
