import requests
import json
import time
from analysis import AnalysisData
from utils import PreprocessData
import numpy as np

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
            if idx == 0 or idx == 2:
                print(len(self.summonerId))
                self.summonerId += [entry['summonerName'] for entry in r.json()['entries'] if entry['summonerName'] != ''][:300]
            elif idx == 1:
                print(len(self.summonerId))
                self.summonerId += [entry['summonerName'] for entry in r.json()['entries'] if entry['summonerName'] != ''][:314]
            else:
                print(len(self.summonerId))
                self.summonerId += [entry['summonerName'] for entry in r.json() if entry.get('summonerName', '') != ''][:75]

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
    
    
    def get_summoner_invertal_list(self, summoner_start, num_matches):

        with open('backend/api_summoner_id.json', 'r', encoding="utf-8") as f:
            summonerId = json.load(f)

        data_list = []
        win_lose_list = []
        num = 0
        summoner_num = summoner_start
        summonerId = summonerId[summoner_num:summoner_num + 500]

        for summoner_name in summonerId:

            puuid = self.get_puuid(summoner_name)
            match_ids = self.get_matchid(puuid)
    
            for match_id in match_ids:

                num += 1
                
                self.get_match_data(match_id)
                self.get_timeline_data(match_id)

                with open('backend/api_match_info.json', 'r', encoding="utf-8") as f:
                    match_info = json.load(f)

                with open('backend/api_timeline_info.json', 'r', encoding="utf-8") as f:
                    timeline_info = json.load(f)

                if "status" in match_info:
                    print("데이터 가져오기 실패: " + str(num))
                    continue

                elif "status" in timeline_info:
                    print("데이터 가져오기 실패: " + str(num))
                    continue
                
                test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

                interval_list = test.get_condition_timeline(10000)
                win_lose = test.get_match_data()[1]
                
                if not interval_list:
                    print("데이터 가져오기 실패: " + str(num))
                    pass
                else:
                    interval_list = [interval.tolist() if isinstance(interval, np.ndarray) else interval for interval in interval_list]
                    data_list.append(interval_list)
                    win_lose_list.append(win_lose)
                    print("데이터 가져오기 : " + str(num))

                time.sleep(3)


                if num == num_matches:
                    break
                
            
            if num == num_matches:
                #with open('backend/api_interval_list1.json', 'w', encoding='utf-8') as json_file:
                #    json.dump(data_list, json_file, ensure_ascii=False, indent=4)
                with open('backend/api_interval_list2.json', 'w', encoding='utf-8') as json_file:
                    json.dump(data_list, json_file, ensure_ascii=False, indent=4)
                # with open('backend/api_interval_list3.json', 'w', encoding='utf-8') as json_file:
                #     json.dump(data_list, json_file, ensure_ascii=False, indent=4)
                # with open('backend/api_interval_list4.json', 'w', encoding='utf-8') as json_file:
                #     json.dump(data_list, json_file, ensure_ascii=False, indent=4)
                # with open('backend/api_interval_list5.json', 'w', encoding='utf-8') as json_file:
                #     json.dump(data_list, json_file, ensure_ascii=False, indent=4)
                # with open('backend/api_interval_list6.json', 'w', encoding='utf-8') as json_file:
                #     json.dump(data_list, json_file, ensure_ascii=False, indent=4)      
                break

if __name__ == "__main__":
    load_data_instance1 = LoadData(api_key='RGAPI-0a7e5bf3-79b3-4b29-93d4-b750f72924c1')
    #load_data_instance2 = LoadData(api_key='RGAPI-9d4a2055-7363-43f5-a1d4-e3747acd9a7e')
    #load_data_instance3 = LoadData(api_key='재혁api')
    # load_data_instance4 = LoadData(api_key='현욱api')
    # load_data_instance5 = LoadData(api_key='재원api')
    # load_data_instance6 = LoadData(api_key='수빈api')

    # load_data_instance1.get_summoner_Id() # 함수 안에서 하면 계속 리스트가 섞이거나 다른 닉네임으로 교체되는 경우가 있어서 여기서 필요하면 한 번만 실행 (건들이지 말 것)

    load_data_instance1.get_summoner_invertal_list(summoner_start=0, num_matches=20) #10000개 데이터 리스트 저장
    #load_data_instance2.get_summoner_invertal_list(summoner_start=500, num_matches=10000)
    #load_data_instance3.get_summoner_invertal_list(summoner_start=1000, num_matches=10000)
    # load_data_instance4.get_summoner_invertal_list(summoner_start=1500, num_matches=10000)
    # load_data_instance5.get_summoner_invertal_list(summoner_start=2000, num_matches=10000)
    # load_data_instance6.get_summoner_invertal_list(summoner_start=2500, num_matches=10000)

    #with open('backend/api_interval_list.json', 'r', encoding="utf-8") as f:
    #    api_interval_list = json.load(f)

    # 리스트(.json 파일) 안 내용 엔터 없애는거 (나중에 모델에서 쓰셈)
    #api_interval_list = [[interval.tolist()[:-1] if isinstance(interval, np.ndarray) else interval[:-1] for interval in sublist] for sublist in api_interval_list]
    #print(api_interval_list)