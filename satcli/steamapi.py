import requests
import pandas as pd
class SteamApi():
    def request_todo_list(self):
        response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        jsonRet = response.json().get('applist').get('apps')

        # L'API steam peut renvoyer plusieurs fois la même entrée pour des raisons que j'ignore.
        df = pd.DataFrame.from_dict(jsonRet) \
            .drop_duplicates() \
            .rename(columns = {"appid" : "id", "name": "app_name"}) \
            .set_index('id')

        return df

    def request_details(self, app_id):
        response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}",
            headers={"Accept-Language":"en-US"}
        )
        if response.status_code == 200:
            result = response.json().get(str(app_id))
            
            status = result.get('success')
            
            if status is False:
                return False

            payload = result.get('data')

            return payload
        else:
            print( f"HTTP RETURN: {response.status_code}" )
            print(response.headers)

            raise "GET FAILED"
