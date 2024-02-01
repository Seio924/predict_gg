import requests
import json
import time

api_key = 'RGAPI-379e15d8-520c-4465-83f8-330f104a073a'

def get_matchid(puuid, api_key):
    # matchid 정보
    matchid_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/"+ puuid +"/ids?start=0&count=20&api_key=" + api_key
    r3 = requests.get(matchid_url)
    #print(r3.json())
    return r3.json()

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

def get_challenger_info(api_key):
    # 챌린저 유저 정보 가져오기 (닉네임)
    challenger_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    r6 = requests.get(challenger_url)

    summonerId = []
    entries = r6.json()['entries']
    num = 0
    for i in entries:
        summonerId.append(i['summonerName'])
        num += 1
    summonerId = list(filter(None, summonerId))

    with open('api_challenger_info.json', 'w', encoding='utf-8') as json_file:
        json.dump(r6.json(), json_file, ensure_ascii=False, indent=4)
    return summonerId

summonerId = get_challenger_info(api_key)
#print(summonerId)

num = 0
# 모든 챌린저 유저 match_id 가져오기
for i in summonerId:
    puuid = get_puuid(i, api_key)
    #print(puuid)
    matchid = get_matchid(puuid, api_key)
    
    for j in matchid:
        if num == 30:
            break
        else:
            get_match_data(j, api_key)
            get_timeline_data(j, api_key)
            num += 1
            time.sleep(5)
        print("업데이트 완료")
    break
