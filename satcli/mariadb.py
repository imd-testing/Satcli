import mysql.connector as Connector
import getpass
import os

class Mariadb():
    def __init__(self):
        self.con = None
        self.cursor = None
        
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.env = self.read_env()
        self.open()

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

    def open(self):
        port = self.env.get('MARIADB_PORT')
        if port is None:
            port = 3306
            
        password = self.env.get('MARIADB_PASSWORD')
        if password is None:
            raise 'You need to define a MARIADB_PASSWORD in a .env file at your project root.'
        
        self.con = Connector.connect(
            host = 'localhost',
            user = 'steampowered',
            password = password,
            port = port,
            database = 'steampowered'
        )

    def close(self):
        self.con.close()
