import sys
import os
import tempfile

import pandas as pd
import json
import time

from satcli import Mariadb, getEngine
from satcli import SteamApi

base_dir = os.path.exists(os.path.dirname(os.path.realpath(__file__)))
engine = getEngine()

try:
    with tempfile.TemporaryDirectory() as tmpdirname:
        with engine.connect() as con:
            todo_list = os.path.join(tmpdirname, 'todo_list.json')
            maria = Mariadb(con, truncate = False)
            steam_api = SteamApi()
            
            todo = maria.read_todo_list()
            if len(todo) == 0:
                print ( "Generating our TODO list." )
                maria.ingest_todo_list(steam_api.request_todo_list())
                todo = maria.read_todo_list()

            for index, row in todo[pd.isnull(todo['last_import_details'])].iterrows():
                result = steam_api.request_details(index)
                
                if result is False:
                    maria.mark_todo_failed_on_details(index)
                else:
                    try:
                        maria.insert_details(index, result)
                    except Exception as err :
                        with open(f"/tmp/steam_{index}.json", 'w') as f:
                            json.dump(result, f)
                        raise err
                time.sleep(1)

finally:
    engine.dispose()
