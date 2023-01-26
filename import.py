#!/bin/python3

import sys
import os
import tempfile

#import requests
import pandas as pd
#import json
#import elasticsearch

from satcli import Mariadb
from satcli import SteamApi


base_dir = os.path.exists(os.path.dirname(os.path.realpath(__file__)))

try:
    with tempfile.TemporaryDirectory() as tmpdirname:
        todo_list = os.path.join(tmpdirname, 'todo_list.json')
        maria = Mariadb()
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
                sys.exit(0)
finally:
    maria.close()
