#!/bin/python3

import os

import requests
import pandas as pd
import json
import elasticsearch

from satcli import Mariadb
from satcli import SteamApi


base_dir = os.path.exists(os.path.dirname(os.path.realpath(__file__)))

try:
    maria = Mariadb()
    steam_api = SteamApi()
    
    todo = maria.read_todo_list()
    if len(todo) == 0:
        maria.ingest_todo_list(steam_api.request_todo_list())
    
    read_cursor = maria.cursor()

    read_cursor.execute('SELECT * FROM steampowered.applications')
    print ( read_cursor.fetchall() )

finally:
    maria.close()
