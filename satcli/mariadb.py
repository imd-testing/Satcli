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


        self.engine = create_engine(f"mysql+mysqlconnector://steampowered:{password}@localhost:{port}/steampowered")

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
        df = pd.read_sql('SELECT id, app_name FROM steampowered.todo_list', self.engine,
            index_col = 'id'
        )

        return df
        
    def ingest_todo_list(self, df):
        with self.engine.connect() as con:
            con.execution_options(autocommit = True).execute("TRUNCATE TABLE steampowered.todo_list;")

            con.execution_options(autocommit = False).execute("SET NAMES utf8mb4;")

            df.to_sql('todo_list', con = con, if_exists = 'append')
