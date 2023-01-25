import requests
import pandas as pd
import json

class SteamApi():
    def request_todo_list(self):
        response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        jsonRet = response.json()
        dfReturnApi = pd.DataFrame.from_dict(jsonRet)
        dfList = pd.DataFrame(dfReturnApi['applist'])
        dfAppList = pd.DataFrame(dfList['applist']['apps'])
            
        json_filename = 'list_steam_game2.json'

        dfAppList.to_json(path_or_buf=json_filename,orient='index')

        if(self.jsonValidator(json_filename) == 1):
            self.csvListAdvice(json_filename)
        else:
            print('KO')