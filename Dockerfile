FROM puckel/docker-airflow:1.10.2
ARG DOCKER_ID=999
USER root

# linux
RUN groupadd --gid $DOCKER_ID docker \
    && usermod -aG docker airflow

COPY ./config/airflow.cfg /usr/local/airflow/airflow.cfg
COPY pip.conf /usr/local/airflow/.pip/pip.conf

USER airflow
