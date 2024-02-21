import requests
import json
import time
from analysis import AnalysisData
from utils import PreprocessData


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

    def get_summoner_Id(self):
        challenger_url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + self.api_key
        grandmaster_url = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + self.api_key
        master_url = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + self.api_key
        diamond_urls = [f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/{tier}?page=1&api_key={self.api_key}" for tier in ['I', 'II', 'III', 'IV']]
        emerald_urls = [f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/EMERALD/{tier}?page=1&api_key={self.api_key}" for tier in ['I', 'II', 'III', 'IV']]
        platinum_urls = [f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/PLATINUM/{tier}?page=1&api_key={self.api_key}" for tier in ['I', 'II', 'III', 'IV']]
        gold_urls = [f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/GOLD/{tier}?page=1&api_key={self.api_key}" for tier in ['I', 'II', 'III', 'IV']]
        silver_urls = [f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/SILVER/{tier}?page=1&api_key={self.api_key}" for tier in ['I', 'II', 'III', 'IV']]
        bronze_urls = [f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/BRONZE/{tier}?page=1&api_key={self.api_key}" for tier in ['I', 'II', 'III', 'IV']]
        iron_urls = [f"https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/IRON/{tier}?page=1&api_key={self.api_key}" for tier in ['I', 'II', 'III', 'IV']]

        url_list = [challenger_url, grandmaster_url, master_url] + diamond_urls + emerald_urls + platinum_urls + gold_urls + silver_urls + bronze_urls + iron_urls

        for idx, url in enumerate(url_list):
            r = requests.get(url)
            if idx < 3:
                self.summonerId += [entry['summonerName'] for entry in r.json()['entries'] if entry['summonerName'] != ''][:250]
            elif idx == 6 or idx == 10 or idx == 14 or idx == 18 or idx == 22 or idx == 26 or idx == 30:   
                self.summonerId += [entry['summonerName'] for entry in r.json() if entry.get('summonerName', '') != ''][:61]
            else:
                self.summonerId += [entry['summonerName'] for entry in r.json() if entry.get('summonerName', '') != ''][:63]

        self.summonerId = list(set(self.summonerId))
        with open('backend/api_summoner_id.json', 'w', encoding='utf-8') as json_file:
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

    def process_summoner_data(self, num_matches):
        self.get_summoner_Id()
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

    def get_summoner_data_list(self, num_matches):
        self.get_summoner_Id()
        data_list = []
        win_lose_list = []

        num = 0
        for summoner_name in self.summonerId:
            puuid = self.get_puuid(summoner_name)
            match_ids = self.get_matchid(puuid)
    
            for match_id in match_ids:
                
                self.get_match_data(match_id)
                self.get_timeline_data(match_id)
                num += 1

                with open('backend/api_match_info.json', 'r', encoding="utf-8") as f:
                    match_info = json.load(f)

                with open('backend/api_timeline_info.json', 'r', encoding="utf-8") as f:
                    timeline_info = json.load(f)

                if "status" in match_info:
                    num -= 1
                    print("데이터 가져오기 실패: " + str(num))
                    continue

                elif "status" in timeline_info:
                    num -= 1
                    print("데이터 가져오기 실패: " + str(num))
                    continue
                
                test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

                

                interval_list = test.get_condition_timeline(10000)
                win_lose = test.get_match_data()[1]
                
                if not interval_list:
                    num -= 1
                    print("데이터 가져오기 실패: " + str(num))
                    pass
                else:
                    #win_lose = [[win_lose[0], win_lose[1]] for i in range(len(interval_list))]
                    
                    data_list.append(interval_list)
                    win_lose_list.append(win_lose)
                    print("데이터 가져오기 : " + str(num))

                time.sleep(3)

                if num == num_matches:
                    break
                
            
            if num == num_matches:
                break
            
        return (data_list, win_lose_list)