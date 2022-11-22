import mysql.connector as Connector
import getpass
import os

class Mariadb():
    def __init__(self):
        self.con = None
        self.cursor = None

        try:
            self.open()
        except Connector.errors.ProgrammingError:
            self.create_database()
            self.open()
    
    def open(self):
        self.con = Connector.connect(
            host = 'localhost',
            user = getpass.getuser(),
            database = 'steampowered',
            unix_socket = '/run/mysqld/mysqld.sock'
        )
        
    def create_database(self):
        self.con = Connector.connect(
            host = 'localhost',
            user = getpass.getuser(),
            database = 'mysql',
            unix_socket = '/run/mysqld/mysqld.sock'
        )
        
        cursor = self.con.cursor()
        
        base_dir = os.path.dirname(os.path.realpath(__file__))
        
        with open(os.path.join(base_dir, 'schema.sql')) as file:
            for query in file.read().split(";"):
                cursor.execute(query)
                
    def close(self):
        self.con.close()
