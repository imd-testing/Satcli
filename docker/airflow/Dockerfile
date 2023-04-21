FROM apache/airflow:2.5.3-python3.10

RUN python -m pip install -U pika

COPY ./docker/airflow/webui.sh /webui.sh
COPY ./docker/airflow/scheduler.sh /scheduler.sh
COPY ./docker/airflow/worker.sh /worker.sh
COPY ./docker/airflow/flower.sh /flower.sh
COPY ./docker/airflow/initialize.sh /initialize.sh

COPY ./docker/airflow/lib.sh /lib.sh
COPY ./docker/airflow/rabbitmq.py /rabbitmq.py

ENV SQLALCHEMY_SILENCE_UBER_WARNING=1
