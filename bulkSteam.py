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
            self.csvListAdvice(json_filename)
        else:
            print('KO')
    
    def csvListAdvice(json_name = 'list_steam_game2.json'):
        dfOut = pd.DataFrame()

        dfGameList = pd.read_json(json_name,orient='index')
        dfGameList = dfGameList[dfGameList['name'] != ''] # for cleaning all test steam game
        
        for index, row in miniGameList.iterrows():
            dfAppDetail = self.getAppDetail(str(row['appid']))
            dfAppReview = self.getAppReview(str(row['appid']))
            

    def jsonValidator(path = 'list_steam_game2.json'):
        f = open(path, 'r')
        json.load(f)
        f.close()

        return 1

    def getAppReview(appId = 730):
            response = requests.get("https://store.steampowered.com/appreviews/"+str(appId)+"?json=1")
            jsonRet = response.json()
            if(jsonRet['success'] == 1): #if query is ok
                finalDf = pd.DataFrame(columns=['query_summary','reviews'])
                finalDf.loc[0] = [jsonRet['query_summary'],jsonRet['reviews']] 
                return finalDf

    def getAppDetail(appId = 730):
        responseGameReview = requests.get("https://store.steampowered.com/api/appdetails?appids="+str(appId))
        jsonRet = responseGameReview.json()
        dfRet = pd.DataFrame(columns=['categories','platforms','genres','metacritic','developers','publishers','name','is_free','recommendations','release_date','required_age'])
        if(jsonRet[str(appId)]['success'] == True):
            workPath = jsonRet[str(appId)]['data']
            dfRet.loc[0] = [workPath['categories'],workPath['platforms'],workPath['genres'],workPath['metacritic'],workPath['developers'],workPath['publishers'],workPath['name'],workPath['is_free'],workPath['recommendations'],workPath['release_date'],workPath['required_age']]
            return dfRet
        

steamApi.callGetGameListToCsv()
