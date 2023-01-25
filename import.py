#!/bin/python3

import os
import tempfile

#import requests
import pandas as pd
#import json
#import elasticsearch

from satcli import Mariadb
from satcli import SteamApi


base_dir = os.path.exists(os.path.dirname(os.path.realpath(__file__)))


with tempfile.TemporaryDirectory() as tmpdirname:
    todo_list = os.path.join(tmpdirname, 'todo_list.json')
    maria = Mariadb()
    steam_api = SteamApi()
    
    todo = maria.read_todo_list()
    if len(todo) == 0:
        print ( "Generatin our TODO list." )
        maria.ingest_todo_list(steam_api.request_todo_list())
        todo = maria.read_todo_list()

    print ( todo ) 


