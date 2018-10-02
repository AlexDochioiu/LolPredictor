# -*- coding: utf-8 -*-

def get_single_match_stats(api_token: str, server: str, match_id: str):
    '''
    For a given match id on a given server, we pull the following details:
        top1_user_id, top1_champ_id, jgl1_user_id, jgl1_champ_id, mid1_user_id, 
        mid1_champ_id, adc1_user_id, adc1_champ_id, sup1_user_id, sup1_champ_id,
        top2_user_id, top2_champ_id, jgl2_user_id, jgl2_champ_id, mid2_user_id, 
        mid2_champ_id, adc2_user_id, adc2_champ_id, sup2_user_id, sup2_champ_id,
        red_team_won (boolean)
        
    P.S. red team is team1 ; blue team is team2
    '''
    
    import urllib.request
    import json
    
    contents = urllib.request.urlopen(urllib.request.Request(
            'https://{0}.api.riotgames.com/lol/match/v3/matches/{1}'.format(server, match_id),
            headers={"X-Riot-Token": api_token, "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",}
            )).read().decode("utf-8")
    
    parsed_contents = json.loads(contents)
    
    returned_game_type: str = parsed_contents['gameMode'] # CLASSIC MEANS NORMAL PVP (both 5v5 and 3v3)
    returned_map_id: int = parsed_contents['mapId'] # mapId 11 is summoner's rift (so 5v5)
    if returned_game_type != 'CLASSIC' and returned_map_id != 11:
        # THIS IS NOT a draft or ranked game
        return []
    
    return_value = [0]*11
    
    def get_players_data():
        players_data = []
        for index in range(10):
            players_data.append([]) # each row will contain: player_id, player_position, champ_id
            player_rito_index: int = parsed_contents['participantIdentities'][index]['participantId']
            if player_rito_index != index + 1:
                print("WARNING: POSITION INDEX DOES NOT MATCH WITH RIOT PLAYER INDEX for game {0} on server {1}".format(match_id, server))
                
            players_data[index].append( parsed_contents['participantIdentities'][index]['player']['accountId'] )
            players_data[index].append( parsed_contents['participants'][index]['timeline']['lane'] ) 
            players_data[index].append( parsed_contents['participants'][index]['championId'] ) 
            
        return players_data
        
    
    red_team_won: bool = parsed_contents['teams'][0]['win'] == 'Win'
    return_value[10] = red_team_won
    return_value[0] = get_players_data()
    
    return return_value

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

print(get_single_match_stats(api_key, "euw1", "3782523216"))

# KOREA MATCH ID 3359817093