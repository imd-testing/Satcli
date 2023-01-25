import mysql.connector as Connector
import getpass
import os

class Cursor(Connector.cursor.MySQLCursor):
    def __init__(self, connection):
        self.is_closed = False
        super().__init__(connection)
        
    def close(self):
        if self.is_closed is False:
            self.is_closed = True
            super().close()

class Mariadb():
    def __init__(self):
        self.con = None

        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.env = self.read_env()
        self.open()
        self.cursor_list = []

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
        for c in self.cursor_list:
            c.close()

        self.con.close()
        
    def cursor(self):
        cur = self.con.cursor(cursor_class = Cursor)
        self.cursor_list.append(cur)
        
        return cur
        
    def read_todo_list(self):
        read_cursor = self.cursor()
        read_cursor.execute('SELECT * FROM steampowered.todo_list')
        result = read_cursor.fetchall()
        
        read_cursor.close()
        return result
        
    def ingest_todo_list(self, df):
        sql = ('INSERT INTO steampowered.todo_list ( id, app_name ) VALUES (%s, %s)')
        cur = self.cursor()
        cur.execute('SET NAMES utf8mb4;')
        
        for index, row in df.iterrows():
            cur.execute(sql, (
                row[0], 
                row[1]
        ))
            
        cur.close()
        self.con.commit()

