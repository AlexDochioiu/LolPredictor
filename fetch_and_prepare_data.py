# -*- coding: utf-8 -*-


def get_hundred_matches_ids_from_index(api_token: str, server:str, account_id: str, season: int = 11, index: int = 0):
    '''
    For a user id, it returns 100 matches ids.
    
    from index 0 we get the most recent 100 games. games (0, 99]
    '''
    import urllib.request
    import json
    contents = urllib.request.urlopen(urllib.request.Request(
            'https://{0}.api.riotgames.com/lol/match/v3/matchlists/by-account/{1}?beginIndex={2}&season={3}'.format(server, account_id, index, season),
            headers={"X-Riot-Token": api_token, "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",}
            )).read().decode("utf-8")

    parsed_contents = json.loads(contents)
    
    match_ids = list(map(lambda match: match['gameId'], parsed_contents['matches']))

    return match_ids

def get_all_matches_ids_for_season(api_token: str, server:str, account_id: str, season: int = 11):
    print("Get all matches for acc {0} on server {1}".format(account_id, server))
    all_matches: list = []
    current_index: int = 0
    
    matches = get_hundred_matches_ids_from_index(api_token, server, account_id, season, current_index)
    all_matches.extend(matches)
    while len(matches) == 100:
        current_index += 100
        matches = get_hundred_matches_ids_from_index(api_token, server, account_id, season, current_index)
        all_matches.extend(matches)
        
    return all_matches
        


# match_ids = get_all_matches_ids_for_season("RGAPI-4a9863d3-fc93-4e0c-a98a-f726500517eb", "euw1", "30648034", 11)
# print(match_ids)
    
api_key: str = "RGAPI-685b780f-3e13-4dd8-bec4-604bc2378e1d"
    
import pandas as pd

dataset = pd.read_csv("players.csv")
dataset = dataset.drop(["Acc Name", "Team"], axis = 1)

match_ids = get_all_matches_ids_for_season(api_key, dataset.iloc[10][1], dataset.iloc[10][2], 11)
#match_ids = get_all_matches_ids_for_season(api_key, "euw1", "30648034", 11)
print(match_ids[:10])