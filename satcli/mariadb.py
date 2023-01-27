import mysql.connector as Connector
import pandas as pd
import os
import datetime

from sqlalchemy import create_engine

def read_env():
    config = {}
    base_dir = os.path.dirname(os.path.realpath(__file__))

    dotenv = os.path.join(base_dir, '../.env')
    if os.path.exists(dotenv):
        with open(dotenv) as file:
            content = file.read().split("\n")

            for line in content:
                parsed = line.split('=')
                if len(parsed) == 2:
                    config[parsed[0].strip()] = parsed[1].strip()

    return config

def getEngine():
    env = read_env()
    
    port = env.get('MARIADB_PORT')
    if port is None:
        port = 3306

    password = env.get('MARIADB_PASSWORD')
    if password is None:
        raise 'You need to define a MARIADB_PASSWORD in a .env file at your project root.'

    return create_engine(f"mysql+mysqlconnector://steampowered:{password}@localhost:{port}/steampowered" )



class Relation():
    def __init__(self, connection, table):
        self.connection = connection
        self.table = table
        self.df = None
        
        self.refresh()
        
    def refresh(self, con = None):
        self.df = pd.read_sql(f"SELECT id, label FROM steampowered.{self.table}", self.connection, index_col = 'id' )
        
    def getByLabel(self, label):
        if label is None:
            return

        if label not in self.df['label'].values :
            self.connection.execute(f"INSERT INTO steampowered.{self.table} SET label = %s ", (label, ))
            self.refresh()
            
        index = self.df[self.df['label'] == label].index

        return int(index[0])
        
    def existsOrCreate(self, index, label):
        if index is None:
            return None

        if int(index) not in self.df.index:
            self.connection.execute(f"INSERT INTO steampowered.{self.table} SET id = %s, label = %s ", (index, label, ))
            self.refresh()

        return int(index)
        
    def __str__(self):
        return f"RELATION {self.table}\n" + str(self.df)
        
class N_2_n():
    def __init__(self, connection, table_types, table_relations, key_relation):
        self.connection = connection
        self.relation = Relation(connection, table_types)
        self.table_relations = table_relations
        self.key_relation = key_relation
        
    def bindIndex(self, to, index, label):
        id = self.relation.existsOrCreate(index, label)
        
        self.connection.execute(f"INSERT INTO steampowered.{self.table_relations} SET id_app = %s, {self.key_relation} = %s",
            (to, id, )
        )
        
    def bind(self, to, label):
        id = self.relation.getByLabel(label)
        
        self.connection.execute(f"INSERT INTO steampowered.{self.table_relations} SET id_app = %s, {self.key_relation} = %s",
            (to, id, )
        )
        

class Mariadb():
    def __init__(self, connection, truncate = False):
        self.categories = None
        self.connection = connection

        if truncate is True:
            self.truncate()

        with self.connection.begin():
            self.types = Relation(self.connection, 'types')
            self.controllers = Relation(self.connection, 'controller_support')
            self.categories = N_2_n(self.connection, 'categories', 'app_2_categories', 'id_categories')
            self.genres = N_2_n(self.connection, 'genres', 'app_2_genres', 'id_genres')

            self.developpers = N_2_n(self.connection, 'developers', 'app_2_developers', 'id_developers')
            self.publishers = N_2_n(self.connection, 'publishers', 'app_2_publishers', 'id_publishers')

    def read_todo_list(self, limit = None):
        sql = 'SELECT id, app_name, last_import_details FROM steampowered.todo_list WHERE last_import_details IS NULL'
        
        if limit is not None:
            sql = sql + f" LIMIT {limit}"
        
        df = pd.read_sql(sql, self.connection, index_col = 'id' )

        return df
        
    def ingest_todo_list(self, df):
        with self.connection.begin():
            self.connection.execute("SET NAMES utf8mb4;")
            df.to_sql('todo_list', con = self.connection, if_exists = 'append')

    def mark_todo_failed_on_details(self, app_id):
        with self.connection.begin():
            self.connection.execute(
                'UPDATE steampowered.todo_list SET last_import_details = NOW(), failed_on_details = 1 WHERE id = %s',
                ( app_id, )
            )

    def get_attributs(self, datas, *key_list):
        current = datas
        next = None
        for key in key_list:
            next = current.get(key)
            if next is None:
                return None
            current = next
            
        return current

    def insert_details_app(self, con, id, datas):
        input_date = self.get_attributs(datas, 'release_date', 'date')
        if len(input_date) > 0:
            try:
                release_date = datetime.datetime.strptime(input_date, '%d %b, %Y')
            except ValueError:
                release_date = datetime.datetime.strptime(input_date, '%d %b %Y')
                
            release_date = release_date.strftime('%Y-%m-%d')
        else:
            release_date = None

        meta_score = self.get_attributs(datas, 'metacritic', 'score')
        recomm = self.get_attributs(datas, 'recommendations', 'total')
        win = self.get_attributs(datas, 'platforms', 'windows')
        mac = self.get_attributs(datas, 'platforms', 'mac')
        linux = self.get_attributs(datas, 'platforms', 'linux')
        
        controller = self.controllers.getByLabel(datas.get('controller_support'))
        type = self.types.getByLabel(datas.get('type'))

        sql = (
            "INSERT INTO steampowered.applications SET id = %s,"
            "id_type = %s,"
            "id_controller_support = %s,"
            "app_name = %s,"
            "required_age = %s,"
            "metacritic_score = %s,"
            "recommendations_count = %s,"
            "release_date = %s,"
            "is_available_on_windows = %s,"
            "is_available_on_mac = %s,"
            "is_available_on_linux = %s,"
            "is_free = %s"
        )
        
        params = (
            id,
            type,
            controller,
            datas.get('name'),
            datas.get('required_age'),
            meta_score,
            recomm,
            release_date,
            win,
            mac,
            linux,
            datas.get('is_free'),
        )

        con.execute( sql, params )

    def insert_details(self, id, datas):
        with self.connection.begin(): 
            name = datas.get('name')
            print ( f"TRANSACTION FOR {name} [{id}]" )

            self.insert_details_app(self.connection, id, datas)

            categories = datas.get('categories')
            genres = datas.get('genres')
            developers = datas.get('developers')
            publishers = datas.get('publishers')
            
            if categories is not None:
                for category in categories:
                    self.categories.bindIndex(
                        id,
                        category.get('id'),
                        category.get('description'),
                    )
            
            
            if genres is not None:
                for genre in datas.get('genres'):
                    self.genres.bindIndex(
                        id,
                        genre.get('id'),
                        genre.get('description'),
                    )

            if developers is not None:
                for label in developers:
                    self.developpers.bind( id, label )
            
            if publishers is not None:
                for label in publishers:
                    self.publishers.bind( id, label )
                
            self.connection.execute( 'UPDATE steampowered.todo_list SET last_import_details = NOW(), failed_on_details = 0 WHERE id = %s', ( id, ) )

    def truncate(self):
        with self.connection.begin():
            self.connection.execute('DELETE FROM steampowered.app_2_categories');
            self.connection.execute('DELETE FROM steampowered.app_2_genres');
            self.connection.execute('DELETE FROM steampowered.app_2_developers');
            self.connection.execute('DELETE FROM steampowered.app_2_publishers');
            self.connection.execute('DELETE FROM steampowered.categories');
            self.connection.execute('DELETE FROM steampowered.genres');
            self.connection.execute('DELETE FROM steampowered.developers');
            self.connection.execute('DELETE FROM steampowered.publishers');
            self.connection.execute('DELETE FROM steampowered.applications');
            self.connection.execute('DELETE FROM steampowered.todo_list');
