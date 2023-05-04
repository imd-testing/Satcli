import requests
import pandas as pd
import datetime

import psycopg2
import os

def add_to_todolist():
	response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
	jsonRet = response.json().get('applist').get('apps')

	# L'API steam peut renvoyer plusieurs fois la même entrée pour des raisons que j'ignore.
	df = pd.DataFrame.from_dict(jsonRet) \
		.drop_duplicates() \
		.rename(columns = {"appid" : "id", "name": "app_name"}) \
		.set_index('id')

	now = datetime.datetime.today()

	df['date_last_import'] = now

	df.to_sql(
		'todo_list', 
		con = os.getenv('STEAMPOWERED__DATABASE__SQL_ALCHEMY_CONN'), 
		if_exists = 'append'
	)
	
	
#	# Connect to your postgres DB
#	password = os.getenv('STEAMPOWERED_PG_PASSWORD')
#	
#	conn = psycopg2.connect(f"host=postgres dbname=steampowered user=steampowered password={password}")
#
#	# Open a cursor to perform database operations
#	cur = conn.cursor()
#
#	# Execute a query
#	cur.execute("SELECT * FROM information_schema.tables where table_catalog = 'steampowered';")
#
#	# Retrieve query results
#	records = cur.fetchall()
#
#	print ( records )

