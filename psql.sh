#!/bin/bash

set -eEu

BASE_DIR=$( realpath $( dirname "${BASH_SOURCE[0]}" ) )

source $BASE_DIR/.env

docker run -ti --rm --network "datascientest_satcli_steam-satcli" -e "PGPASSWORD=$POSTGRES_PASSWORD" postgres:15.1 psql -h postgres -U root
