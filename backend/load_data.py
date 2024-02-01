import requests
import json

api_key = 'RGAPI-e787e1b0-49da-42b6-b3ed-7e79fcf06283'

def get_matchid(puuid, api_key):
    # matchid 정보
    matchid_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"+ puuid +"/ids?start=0&count=20&api_key=" + api_key
    r3 = requests.get(matchid_url)
    print(r3.json())

def get_puuid(name, api_key):
    # puuid 정보
    puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + '?api_key=' + api_key
    r3 = requests.get(puuid_url)

    return r3.json()['puuid']

def get_match_data(matchid, api_key):
    # 매치 정보
    match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid + '?api_key=' + api_key
    r4 = requests.get(match_url)
    
    with open('api_match_info.json', 'w', encoding='utf-8') as json_file:
        json.dump(r4.json(), json_file, ensure_ascii=False, indent=4)


def get_timeline_data(matchid, api_key):
    # 타임라인 매치 정보 (1분 단위)
    match_timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid + "/timeline" + '?api_key=' + api_key
    r5 = requests.get(match_timeline_url)
    
    with open('api_timeline_info.json', 'w', encoding='utf-8') as json_file:
        json.dump(r5.json(), json_file, ensure_ascii=False, indent=4)


puuid = get_puuid('Hide on bush', api_key)
print(puuid)

get_matchid(puuid, api_key)
