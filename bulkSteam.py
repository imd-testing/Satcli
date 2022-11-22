import requests
import pandas as pd
import json

class steamApi:
    def callGetGameListToCsv():
        response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")
        jsonRet = response.json()
        dfReturnApi = pd.DataFrame.from_dict(jsonRet)
        dfList = pd.DataFrame(dfReturnApi['applist'])
        dfAppList = pd.DataFrame(dfList['applist']['apps'])
        
        json_filename = 'list_steam_game2.json'

        dfAppList.to_json(path_or_buf=json_filename,orient='index')

        if(self.jsonValidator(json_filename) == 1):
            print('OK')
        else:
            print('KO')
    
    def csvListAdvice(limit = 10):
        dfOut = pd.DataFrame()

        dfGameList = pd.read_json('list_steam_game2.json',orient='index')
        dfGameList = dfGameList[dfGameList['name'] != '']
        if(limit!=0):
            miniGameList = dfGameList[0:limit]
        else :
            miniGameList = dfGameList
            
        # print(miniGameList.columns.tolist())
        for index, row in miniGameList.iterrows():
            # print(row['appid'])
            # response = requests.get("https://store.steampowered.com/appreviews/1063730?json=1")
            response = requests.get("https://store.steampowered.com/appreviews/"+str(row['appid'])+"?json=1")
            jsonRet = response.json()
            # print(row['appid'])
            if(jsonRet['success'] == 1): #if query is ok
                dfListQs = pd.DataFrame(jsonRet['query_summary'],index=[0])
                print(dfListQs.columns.tolist())
                dfListR = pd.DataFrame(jsonRet['reviews'])
                # print(dfListR.columns.tolist())
                # dfListA = pd.DataFrame(dfListR['author'])
                # for indexR, rowR in dfListR.iterrows():
                    # dfListAR = pd.DataFrame(dfListA.iloc[indexA]['author'],index=[0])
                    # print(rowR)
                    # print(dfListR.columns.tolist())
                print(dfListR.columns.tolist())
            # dfOut[index] = 

    def jsonValidator(path = 'list_steam_game2.json'):
        f = open(path, 'r')
        json.load(f)
        f.close()

        return 1

steamApi.csvListAdvice(10,10)
# steamApi.callGetGameListToCsv()
# steamApi.jsonValidator()
