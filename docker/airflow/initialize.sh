#!/bin/bash

set -eEu

source /lib.sh

echo "WAITING FOR Postgres"
waitPg

echo "WAITING FOR Rabbitmq"
waitRabbit


if ! ( airflow db check 2>&1 | grep -q " does not exist" )
then
	echo "DATABASE already exists, reseting it."
	airflow db reset -y
fi

echo "RUNNING airflow db init"
if airflow db init >/tmp/airflow-db-init.log 2>&1
then
	rm /tmp/airflow-db-init.log
else
	cat /tmp/airflow-db-init.log
	exit 1
fi

echo "CREATING USER"
if airflow users create \
	--username "$AIRFLOW_USER_LOGIN" \
	--firstname John \
	--lastname Doe \
	--role Admin \
	--password "$AIRFLOW_USER_PASSWORD" \
	--email jdoe@example.com \
	>/tmp/airflow-db-init.log 2>&1
then
	rm /tmp/airflow-db-init.log
else
	cat /tmp/airflow-db-init.log
	exit 1
fi
