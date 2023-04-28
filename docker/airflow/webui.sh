#!/bin/bash

set -eEu

source /lib.sh

# On s'assure que le lock sur PID soit effacé.
if [ -f /opt/airflow/airflow-webserver.pid ]
then
	rm /opt/airflow/airflow-webserver.pid
fi

echo "WAITING FOR Postgres"
waitPg

echo "WAITING FOR Rabbitmq"
waitRabbit

airflow webserver --port 80
