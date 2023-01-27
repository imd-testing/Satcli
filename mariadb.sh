#!/bin/bash

set -eEu

source .env

mysql -u steampowered -h localhost --password="${MARIADB_PASSWORD}" -P ${MARIADB_PORT:-3306} --protocol=TCP steampowered