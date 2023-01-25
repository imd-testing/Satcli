import requests
import pandas as pd
class SteamApi():
    def request_todo_list(self):
        response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        jsonRet = response.json().get('applist').get('apps')

        # L'API steam peut renvoyer plusieurs fois la même entrée pour des raisons que j'ignore.
        df = pd.DataFrame.from_dict(jsonRet).drop_duplicates()

        return df
