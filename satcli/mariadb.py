import mysql.connector as Connector
import pandas as pd
import os

from sqlalchemy import create_engine

class Mariadb():
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.env = self.read_env()
        
        port = self.env.get('MARIADB_PORT')
        if port is None:
            port = 3306

        password = self.env.get('MARIADB_PASSWORD')
        if password is None:
            raise 'You need to define a MARIADB_PASSWORD in a .env file at your project root.'


        self.engine = create_engine(f"mysql+mysqlconnector://steampowered:{password}@localhost:{port}/steampowered" )
        
    def close(self):
        self.engine.dispose()

    def read_env(self):
        config = {}

        dotenv = os.path.join(self.base_dir, '../.env')
        if os.path.exists(dotenv):
            with open(dotenv) as file:
                content = file.read().split("\n")

                for line in content:
                    parsed = line.split('=')
                    if len(parsed) == 2:
                        config[parsed[0].strip()] = parsed[1].strip()

        return config

    def read_todo_list(self):
        df = pd.read_sql('SELECT id, app_name, last_import_details FROM steampowered.todo_list', self.engine,
            index_col = 'id'
        )

        return df
        
    def ingest_todo_list(self, df):
        with self.engine.begin() as con:
            con.execute("TRUNCATE TABLE steampowered.todo_list;")

            con.execute("SET NAMES utf8mb4;")

            df.to_sql('todo_list', con = con, if_exists = 'append')

    def mark_todo_failed_on_details(self, app_id):
        with self.engine.begin() as con:
            con.execute(
                'UPDATE steampowered.todo_list SET last_import_details = NOW(), failed_on_details = 1 WHERE id = %s',
                ( app_id, )
            )

