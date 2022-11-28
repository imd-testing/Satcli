#!/usr/bin/env python3

import pika
import ssl

connection = pika.BlockingConnection(
	pika.ConnectionParameters(
		'rabbitmq', 
		socket_timeout=1, 
		stack_timeout=1
	)
)

connection.close()
