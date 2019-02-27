FROM puckel/docker-airflow:1.10.2

USER root

# linux
RUN groupadd --gid 999 docker \
    && usermod -aG docker airflow

COPY ./config/airflow.cfg /usr/local/airflow/airflow.cfg
COPY pip.conf /usr/local/airflow/.pip/pip.conf

USER airflow
