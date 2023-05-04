#!/bin/bash

set -eEu
set -o pipefail

BASE_DIR=$( realpath $( dirname "${BASH_SOURCE[0]}" )/.. )
PROJECT_NAME=$( basename "$BASE_DIR")
VOLUME_NAME="${PROJECT_NAME}_pgdata"
COMPOSE="docker-compose -f $BASE_DIR/docker-compose.initialize.yml --project-directory $BASE_DIR"

if docker volume ls -q | grep -q "$VOLUME_NAME"
then
	echo "VOLUME $VOLUME_NAME, deleting."
	$COMPOSE down
	docker volume rm $VOLUME_NAME
fi

$COMPOSE up --build --abort-on-container-exit
