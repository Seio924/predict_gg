import requests
import json
import time

class LoadData():
    def __init__(self, api_key):
        self.api_key = api_key
        self.summonerId = []

    def get_matchid(self, puuid):
        matchid_url = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=20&api_key=" + self.api_key
        r3 = requests.get(matchid_url)
        return r3.json()

    def get_puuid(self, name):
        puuid_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + '?api_key=' + self.api_key
        r3 = requests.get(puuid_url)
        return r3.json()['puuid']

    def get_match_data(self, matchid):
        match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid + '?api_key=' + self.api_key
        r4 = requests.get(match_url)
        with open('backend/api_match_info.json', 'w', encoding='utf-8') as json_file:
            json.dump(r4.json(), json_file, ensure_ascii=False, indent=4)

    def get_timeline_data(self, matchid):
        match_timeline_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchid + "/timeline" + '?api_key=' + self.api_key
        r5 = requests.get(match_timeline_url)
        with open('backend/api_timeline_info.json', 'w', encoding='utf-8') as json_file:
            json.dump(r5.json(), json_file, ensure_ascii=False, indent=4)

    def get_challenger_info(self):
        challenger_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + self.api_key
        r6 = requests.get(challenger_url)
        entries = r6.json()['entries']
        self.summonerId = [i['summonerName'] for i in entries if 'summonerName' in i]

        with open('backend/api_challenger_info.json', 'w', encoding='utf-8') as json_file:
            json.dump(r6.json(), json_file, ensure_ascii=False, indent=4)

    def process_challenger_data(self, num_matches):
        self.get_challenger_info()

        num = 0
        for summoner_name in self.summonerId:
            puuid = self.get_puuid(summoner_name)
            match_ids = self.get_matchid(puuid)
    
            for match_id in match_ids:
                if num == num_matches:
                    break
                else:
                    self.get_match_data(match_id)
                    self.get_timeline_data(match_id)
                    num += 1
                    time.sleep(5)
            print("업데이트 완료")
            break  