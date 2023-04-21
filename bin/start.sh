#!/bin/bash

set -eEu

export BASE_DIR=$( realpath $( dirname "${BASH_SOURCE[0]}" )/.. )

COMPOSE="docker-compose -f $BASE_DIR/docker-compose.yml --project-directory $BASE_DIR"

$COMPOSE up
