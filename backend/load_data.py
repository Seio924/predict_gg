import requests
import json
import time
from analysis import AnalysisData

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
        self.summonerId = [entry['summonerName'] for entry in r6.json()['entries'] if entry['summonerName'] != '']
        self.summonerId.sort()
        with open('backend/api_challenger_info.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.summonerId, json_file, ensure_ascii=False, indent=4)

    def get_diamond1_info(self):
        diamond1_url = "https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1&api_key=" + self.api_key
        r7 = requests.get(diamond1_url)
        self.summonerId = [entry['summonerName'] for entry in r7.json() if entry.get('summonerName', '') != '']        
        self.summonerId.sort()

        with open('backend/api_diamond1_info.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.summonerId, json_file, ensure_ascii=False, indent=4)

    def process_challenger_data(self, num_matches):
        self.get_challenger_info()
        analysis_data = AnalysisData()

        num = 0
        for summoner_name in self.summonerId:
            puuid = self.get_puuid(summoner_name)
            match_ids = self.get_matchid(puuid)
    
            for match_id in match_ids:
                self.get_match_data(match_id)
                self.get_timeline_data(match_id)
                num += 1
                analysis_data.analyze_data()
                
                print("분석 완료 : " + str(num))
                time.sleep(4)

                if num == num_matches:
                    break
                
            
            if num == num_matches:
                break
        analysis_data.plot_results()
        print("끝")

    def process_diamond1_data(self, num_matches):
        self.get_diamond1_info()
        analysis_data = AnalysisData()

        num = 0
        for summoner_name in self.summonerId:
            puuid = self.get_puuid(summoner_name)
            match_ids = self.get_matchid(puuid)
    
            for match_id in match_ids:
                
                self.get_match_data(match_id)
                self.get_timeline_data(match_id)
                num += 1
                analysis_data.analyze_data()
                
                print("분석 완료 : " + str(num))

                time.sleep(4)

                if num == num_matches:
                    break
                
            
            if num == num_matches:
                break
        analysis_data.plot_results()
        print("끝")