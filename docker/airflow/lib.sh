#!/bin/bash

set -eEu

function waitRabbit {
	for i in $(seq 1 3000)
	do
		sleep 0.5
		if /rabbitmq.py 2>/dev/null >/dev/null
		then
			return 0
		fi
	done

	echo "rabbitmq never started"

	return 1
}

function waitPg {
	for i in $(seq 1 30)
	do
		sleep 0.1
		if pg_isready -h postgres -U airflow >/dev/null
		then
			return 0
		fi
	done

	echo "POSGRES didn't start, exiting"

	return 1
}

function waitUI {
	for i in $(seq 1 3000)
	do
		sleep 0.1
		if curl -s -i --connect-timeout 1 webui:80 >/dev/null
		then
			return 0
		fi
	done

	echo "webui never started"

	return 1
}
