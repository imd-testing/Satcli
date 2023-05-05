import requests
import pandas as pd
import os
import datetime

from sqlalchemy import create_engine, text

def refresh_app_list(conn, batch_time):
	response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
	jsonRet = response.json().get('applist').get('apps')
	
	df = pd.DataFrame.from_dict(jsonRet) \
		.drop_duplicates() \
		.rename(columns = {"appid" : "id", "name": "app_name"}) \
		.set_index('id')
	
	df['date_last_seen'] = batch_time

	params = []	
	
	# We are using another connexion to avoid pandas commiting on our main one.
	df.to_sql(
		'raw_app_list', 
		os.getenv('STEAMPOWERED__DATABASE__SQL_ALCHEMY_CONN'), 
		if_exists = 'replace'
	)
	
	conn.execute(text(
		"INSERT INTO app_list ( id, app_name, date_last_seen) "
		"SELECT id, app_name, date_last_seen FROM raw_app_list "
		"ON CONFLICT ( id ) DO NOTHING "
	))

	conn.execute(text(
		"UPDATE app_list AS a "
		"SET app_name = r.app_name, date_last_seen = r.date_last_seen "
		"FROM raw_app_list AS r "
		"WHERE r.id = a.id "
	))
	
def load_next_tasks(conn, batch_time):
	batch_size = os.getenv('STEAMPOWERED__BATCH_SIZE', 10)
	
	next_tasks = conn.execute(
		text("SELECT todo, parameters FROM todo_list WHERE ( date_last_batch IS NULL OR date_last_batch != :batch ) ORDER BY date_added ASC LIMIT :batch_size"),
		[{"batch": batch_time, "batch_size": batch_size}]
	).all()
	
	if len(next_tasks) > 0:
		conn.execute(
			text("UPDATE todo_list SET date_last_batch = :batch WHERE todo = :todo AND parameters = :param"),
			[{"batch": batch_time, "todo": t[0], "param": t[1]} for t in next_tasks]
		)
		conn.commit()

	return next_tasks
	
def remove_task(conn, task):
	conn.execute(
		text("DELETE FROM todo_list WHERE todo = :todo AND parameters = :param"),
		[{"todo": task[0], "param": task[1]}]
	)

def run_queue():
	engine = create_engine(
		os.getenv('STEAMPOWERED__DATABASE__SQL_ALCHEMY_CONN'), 
		future = True
	)
	batch_time = datetime.datetime.today()
	
	with engine.connect() as conn:
		tasks = load_next_tasks(conn, batch_time)
		
		for task in tasks:
			match task[0]:
				case 'refresh_app_list':
					refresh_app_list(conn, batch_time)
				case _ :
					print ( 'unknown action' )

			remove_task(conn, task)
			conn.commit()
