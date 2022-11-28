#!/bin/bash

set -eE
set -u

source /lib.sh

echo "WAITING FOR UI"
waitUI

cd /opt/airflow/dags

airflow celery worker
