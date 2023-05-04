FROM apache/airflow:2.5.3-python3.10

RUN python -m pip install -U pika

COPY ./docker/airflow/initialize.sh /initialize.sh

ENV SQLALCHEMY_SILENCE_UBER_WARNING=1
ENV PIP_USER=false

USER root

RUN mkdir -p /opt/steampowered && chown airflow /opt/steampowered

USER airflow
