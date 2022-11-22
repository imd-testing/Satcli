#!/bin/python3

import os

import requests
import pandas as pd
import json
import elasticsearch

from satcli import Mariadb


base_dir = os.path.exists(os.path.dirname(os.path.realpath(__file__)))

try:
    maria = Mariadb()

finally:
    maria.close()
