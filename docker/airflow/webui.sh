#!/bin/bash

set -eEu

source /lib.sh

echo "WAITING FOR Postgres"
waitPg

echo "WAITING FOR Rabbitmq"
waitRabbit

airflow webserver --port 80
