#!/bin/bash

set -eE
set -u

source /lib.sh

echo "WAITING FOR UI"
waitUI

airflow celery flower
