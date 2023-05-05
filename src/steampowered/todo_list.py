import os
from sqlalchemy import create_engine, text

def add_to_todolist():
	engine = create_engine(os.getenv('STEAMPOWERED__DATABASE__SQL_ALCHEMY_CONN'))
	
	with engine.connect() as conn:
		conn.execute(text("INSERT INTO public.todo_list ( todo, parameters ) VALUES ( 'refresh_app_list', '' )"))


