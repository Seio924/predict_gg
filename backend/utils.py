import json
import numpy as np

TIMESTAMP = 0

TEAM1_TOP_CHAMPION = 1
TEAM1_TOP_GOLD = 2
TEAM1_TOP_ITEM_GOLD = 3
TEAM1_TOP_K = 4
TEAM1_TOP_D = 5
TEAM1_TOP_A = 6
TEAM1_TOP_STATPERK_DEFENCE = 7
TEAM1_TOP_STATPERK_FLEX = 8
TEAM1_TOP_STATPERK_OFFENSE = 9
TEAM1_TOP_PRIMARY1 = 10
TEAM1_TOP_PRIMARY2 = 11
TEAM1_TOP_PRIMARY3 = 12
TEAM1_TOP_PRIMARY4 = 13
TEAM1_TOP_SUBSTYLE1 = 14
TEAM1_TOP_SUBSTYLE2 = 15

TEAM1_JUNGLE_CHAMPION = 16
TEAM1_JUNGLE_GOLD = 17
TEAM1_JUNGLE_ITEM_GOLD = 18
TEAM1_JUNGLE_K = 19
TEAM1_JUNGLE_D = 20
TEAM1_JUNGLE_A = 21
TEAM1_JUNGLE_STATPERK_DEFENCE = 22
TEAM1_JUNGLE_STATPERK_FLEX = 23
TEAM1_JUNGLE_STATPERK_OFFENSE = 24
TEAM1_JUNGLE_PRIMARY1 = 25
TEAM1_JUNGLE_PRIMARY2 = 26
TEAM1_JUNGLE_PRIMARY3 = 27
TEAM1_JUNGLE_PRIMARY4 = 28
TEAM1_JUNGLE_SUBSTYLE1 = 29
TEAM1_JUNGLE_SUBSTYLE2 = 30

TEAM1_MIDDLE_CHAMPION = 31
TEAM1_MIDDLE_GOLD = 32
TEAM1_MIDDLE_ITEM_GOLD = 33
TEAM1_MIDDLE_K = 34
TEAM1_MIDDLE_D = 35
TEAM1_MIDDLE_A = 36
TEAM1_MIDDLE_STATPERK_DEFENCE = 37
TEAM1_MIDDLE_STATPERK_FLEX = 38
TEAM1_MIDDLE_STATPERK_OFFENSE = 39
TEAM1_MIDDLE_PRIMARY1 = 40
TEAM1_MIDDLE_PRIMARY2 = 41
TEAM1_MIDDLE_PRIMARY3 = 42
TEAM1_MIDDLE_PRIMARY4 = 43
TEAM1_MIDDLE_SUBSTYLE1 = 44
TEAM1_MIDDLE_SUBSTYLE2 = 45

TEAM1_BOTTOM_CHAMPION = 46
TEAM1_BOTTOM_GOLD = 47
TEAM1_BOTTOM_ITEM_GOLD = 48
TEAM1_BOTTOM_K = 49
TEAM1_BOTTOM_D = 50
TEAM1_BOTTOM_A = 51
TEAM1_BOTTOM_STATPERK_DEFENCE = 52
TEAM1_BOTTOM_STATPERK_FLEX = 53
TEAM1_BOTTOM_STATPERK_OFFENSE = 54
TEAM1_BOTTOM_PRIMARY1 = 55
TEAM1_BOTTOM_PRIMARY2 = 56
TEAM1_BOTTOM_PRIMARY3 = 57
TEAM1_BOTTOM_PRIMARY4 = 58
TEAM1_BOTTOM_SUBSTYLE1 = 59
TEAM1_BOTTOM_SUBSTYLE2 = 60

TEAM1_UTILITY_CHAMPION = 61
TEAM1_UTILITY_GOLD = 62
TEAM1_UTILITY_ITEM_GOLD = 63
TEAM1_UTILITY_K = 64
TEAM1_UTILITY_D = 65
TEAM1_UTILITY_A = 66
TEAM1_UTILITY_STATPERK_DEFENCE = 67
TEAM1_UTILITY_STATPERK_FLEX = 68
TEAM1_UTILITY_STATPERK_OFFENSE = 69
TEAM1_UTILITY_PRIMARY1 = 70
TEAM1_UTILITY_PRIMARY2 = 71
TEAM1_UTILITY_PRIMARY3 = 72
TEAM1_UTILITY_PRIMARY4 = 73
TEAM1_UTILITY_SUBSTYLE1 = 74
TEAM1_UTILITY_SUBSTYLE2 = 75

TEAM1_GOLD = 76
WARD_PLACED = 77
WARD_KILL = 78

HORDE_COUNT = 79
DRAGON_COUNT = 80
RIFTHERALD_COUNT = 81
BARON_NASHOR_COUNT = 82

TOWER_TOP_COUNT = 83
TOWER_MIDDLE_COUNT = 84
TOWER_BOTTOM_COUNT = 85

TEAM_INTERVAL = 85

LIST_LEN = 172

class PreprocessData():
    def __init__(self, match_file_dir, timeline_file_dir):
        self.match_file_dir = match_file_dir
        self.timeline_file_dir = timeline_file_dir
    
    def get_match_data(self):

        with open(self.match_file_dir, encoding='utf-8') as f:
            initial_match_data = json.load(f)

        aram = 1
        win_lose = [0, 0] #어떤 팀이 이겼는지 [team1, team2]
        team = {}
        line = {}
        champion_list = ["MONKEYKING", "SMOLDER", "AATROX", "AHRI", "AKALI", "AKSHAN", "ALISTAR", "AMUMU", "ANIVIA", "ANNIE", "APHELIOS", "ASHE", "AURELIONSOL", "AZIR", "BARD", "BELVETH", "BLITZCRANK", "BRAND", "BRAUM", "BRIAR", "CAITLYN", "CAMILLE", "CASSIOPEIA", "CHOGATH", "CORKI", "DARIUS", "DIANA", "DRMUNDO", "DRAVEN", "EKKO", "ELISE", "EVELYNN", "EZREAL", "FIDDLESTICKS", "FIORA", "FIZZ", "GALIO", "GANGPLANK", "GAREN", "GNAR", "GRAGAS", "GRAVES", "GWEN", "HECARIM", "HEIMERDINGER", "HWEI", "ILLAOI", "IRELIA", "IVERN", "JANNA", "JARVANIV", "JAX", "JAYCE", "JHIN", "JINX", "KSANTE", "KAISA", "KALISTA", "KARMA", "KARTHUS", "KASSADIN", "KATARINA", "KAYLE", "KAYN", "KENNEN", "KHAZIX", "KINDRED", "KLED", "KOGMAW", "LEBLANC", "LEESIN", "LEONA", "LILLIA", "LISSANDRA", "LUCIAN", "LULU", "LUX", "MALPHITE", "MALZAHAR", "MAOKAI", "MASTERYI", "MILIO", "MISSFORTUNE", "MORDEKAISER", "MORGANA", "NAAFIRI", "NAMI", "NASUS", "NAUTILUS", "NEEKO", "NIDALEE", "NILAH", "NOCTURNE", "NUNU", "OLAF", "ORIANNA", "ORNN", "PANTHEON", "POPPY", "PYKE", "QIYANA", "QUINN", "RAKAN", "RAMMUS", "REKSAI", "RELL", "RENATA", "RENEKTON", "RENGAR", "RIVEN", "RUMBLE", "RYZE", "SAMIRA", "SEJUANI", "SENNA", "SERAPHINE", "SETT", "SHACO", "SHEN", "SHYVANA", "SINGED", "SION", "SIVIR", "SKARNER", "SONA", "SORAKA", "SWAIN", "SYLAS", "SYNDRA", "TAHMKENCH", "TALIYAH", "TALON", "TARIC", "TEEMO", "THRESH", "TRISTANA", "TRUNDLE", "TRYNDAMERE", "TWISTEDFATE", "TWITCH", "UDYR", "URGOT", "VARUS", "VAYNE", "VEIGAR", "VELKOZ", "VEX", "VI", "VIEGO", "VIKTOR", "VLADIMIR", "VOLIBEAR", "WARWICK", "WUKONG", "XAYAH", "XERATH", "XINZHAO", "YASUO", "YONE", "YORICK", "YUUMI", "ZAC", "ZED", "ZERI", "ZIGGS", "ZILEAN", "ZOE", "ZYRA"]
        perk_list = []
        champion_dic = {}
        champion = {}

        for i, c in enumerate(champion_list):
            champion_dic[c] = i

        if initial_match_data['info']["gameMode"] == "CLASSIC":
            aram = 0

            all_participants_data = initial_match_data['info']['participants']

            for i, participant_data in enumerate(all_participants_data):
                
                if participant_data['teamId'] == 100:
                    team[i+1] = 0
                    line[i+1] = participant_data['teamPosition']
                    
                    if participant_data['win'] == True:
                        win_lose[0] = 1

                elif participant_data['teamId'] == 200:
                    team[i+1] = TEAM_INTERVAL
                    line[i+1] = participant_data['teamPosition']

                    if participant_data['win'] == True:
                        win_lose[1] = 1
                
                champion[participant_data['participantId']] = champion_dic[participant_data['championName'].upper()]
                
                statperk_defense = participant_data['perks']['statPerks']['defense']
                statperk_flex = participant_data['perks']['statPerks']['flex']
                statperk_offense = participant_data['perks']['statPerks']['offense']
                primary_perk = []
                substyle_perk = []

                for p in participant_data['perks']['styles']:
                    if p['description'] == "primaryStyle":
                        for perk in p['selections']:
                            primary_perk.append(perk['perk'])
                    elif p['description'] == "subStyle":
                        for perk in p['selections']:
                            substyle_perk.append(perk['perk'])

                perk_list.append([statperk_defense, statperk_flex, statperk_offense, primary_perk[0], primary_perk[1], primary_perk[2], primary_perk[3], substyle_perk[0], substyle_perk[1]])

        return (team, win_lose, line, champion, aram, perk_list)

    def get_item_data(self):
        with open('./api_data/item.json', encoding="utf-8") as f:
            item_data = json.load(f)

        item_base_cost = {}
        item_total_cost = {}
        item_sold_cost = {}
        
        for i in list(item_data['data'].keys()):
            item_base_cost[i] = item_data['data'][i]['gold']['base']
            item_total_cost[i] = item_data['data'][i]['gold']['total']
            item_sold_cost[i] = item_data['data'][i]['gold']['sell']

        return (item_base_cost, item_total_cost, item_sold_cost)
  
    def get_item_from_data(self, beforeId):
        with open('./api_data/item.json', encoding="utf-8") as f:
            item_data = json.load(f)       
        item_info = item_data['data'].get(beforeId, {})
        item_from = item_info.get('from', [])
        return item_from

    def get_event(self):
        try:
            with open(self.timeline_file_dir, encoding='utf-8') as f:
                initial_data = json.load(f)
            
            initial_data = initial_data['info']['frames']
            item_base_cost, item_total_cost, item_sold_cost = self.get_item_data()
            team, win_lose, line, champion, aram, perk_list = self.get_match_data()

            event_list_result = []
            item_real_cost = 0

            if aram == 0:

                for i in initial_data:
                    for j in i['events']:
                        event_list = [0 for h in range(LIST_LEN)]
                        event_list[TIMESTAMP] = j['timestamp']
                        
                        if j['type'] == 'ITEM_PURCHASED':
                            if item_base_cost[str(j['itemId'])] == item_total_cost[str(j['itemId'])]:
                                item_real_cost = item_base_cost[str(j['itemId'])]
                            elif item_base_cost[str(j['itemId'])] != item_total_cost[str(j['itemId'])]:
                                item_real_cost = item_total_cost[str(j['itemId'])] - item_base_cost[str(j['itemId'])]

                            team_interval = team[j['participantId']]
                            
                            if line[j['participantId']] == "TOP":
                                event_list[TEAM1_TOP_ITEM_GOLD+team_interval] += item_real_cost

                            elif line[j['participantId']] == "JUNGLE":
                                event_list[TEAM1_JUNGLE_ITEM_GOLD+team_interval] += item_real_cost

                            elif line[j['participantId']] == "MIDDLE":
                                event_list[TEAM1_MIDDLE_ITEM_GOLD+team_interval] += item_real_cost

                            elif line[j['participantId']] == "BOTTOM":
                                event_list[TEAM1_BOTTOM_ITEM_GOLD+team_interval] += item_real_cost

                            elif line[j['participantId']] == "UTILITY":
                                event_list[TEAM1_UTILITY_ITEM_GOLD+team_interval] += item_real_cost


                        elif j['type'] == 'ITEM_SOLD':
                            team_interval = team[j['participantId']]
                            minus_gold = item_sold_cost[str(j['itemId'])] - item_base_cost[str(j['itemId'])]

                            if line[j['participantId']] == "TOP":
                                event_list[TEAM1_TOP_GOLD+team_interval] = minus_gold
                                event_list[TEAM1_TOP_ITEM_GOLD+team_interval] -= item_sold_cost[str(j['itemId'])]

                            elif line[j['participantId']] == "JUNGLE":
                                event_list[TEAM1_JUNGLE_GOLD+team_interval] = minus_gold
                                event_list[TEAM1_JUNGLE_ITEM_GOLD+team_interval] -= item_sold_cost[str(j['itemId'])]

                            elif line[j['participantId']] == "MIDDLE":
                                event_list[TEAM1_MIDDLE_GOLD+team_interval] = minus_gold
                                event_list[TEAM1_MIDDLE_ITEM_GOLD+team_interval] -= item_sold_cost[str(j['itemId'])]

                            elif line[j['participantId']] == "BOTTOM":
                                event_list[TEAM1_BOTTOM_GOLD+team_interval] = minus_gold
                                event_list[TEAM1_BOTTOM_ITEM_GOLD+team_interval] -= item_sold_cost[str(j['itemId'])]
                                
                            elif line[j['participantId']] == "UTILITY":
                                event_list[TEAM1_UTILITY_GOLD+team_interval] = minus_gold
                                event_list[TEAM1_UTILITY_ITEM_GOLD+team_interval] -= item_sold_cost[str(j['itemId'])]
                            
        
                        elif j['type'] == 'ITEM_UNDO':
                            team_interval = team[j['participantId']]
                            if j['beforeId'] == 0:
                                # beforeId가 0이라는 말은 팔았던걸 되돌렸다는 말. 그러면 afterId만큼 tear를 올려줘야 한다.
                                # 판금 장화 가지고 있는데 이걸 판다. 그리고 UNDO before 0 after 3000
                                #event_list[9] += item_tear[str(j['afterId'])]
                                if line[j['participantId']] == "TOP":
                                    event_list[TEAM1_TOP_ITEM_GOLD+team_interval] += item_sold_cost[str(j['afterId'])]

                                elif line[j['participantId']] == "JUNGLE":
                                    event_list[TEAM1_JUNGLE_ITEM_GOLD+team_interval] += item_sold_cost[str(j['afterId'])]

                                elif line[j['participantId']] == "MIDDLE":
                                    event_list[TEAM1_MIDDLE_ITEM_GOLD+team_interval] += item_sold_cost[str(j['afterId'])]

                                elif line[j['participantId']] == "BOTTOM":
                                    event_list[TEAM1_BOTTOM_ITEM_GOLD+team_interval] += item_sold_cost[str(j['afterId'])]

                                elif line[j['participantId']] == "UTILITY":
                                    event_list[TEAM1_UTILITY_ITEM_GOLD+team_interval] += item_sold_cost[str(j['afterId'])]
                                        
                            else:
                                # beforeId가 0이 아니라는 말은 샀던걸 되돌렸다는 말. 그러면 beforeId만큼 tear를 내려줘야한다. 대신 상위아이템인 경우는 하위아이템만큼 더해준다.
                                #시작아이템 물약2 + 신발 UNDO3번 before 2003 after 0
                                if item_base_cost[str(j['beforeId'])] == item_total_cost[str(j['beforeId'])]:
                                    item_real_cost = item_base_cost[str(j['beforeId'])]
                                elif item_base_cost[str(j['beforeId'])] != item_total_cost[str(j['beforeId'])]:
                                    item_real_cost = item_total_cost[str(j['beforeId'])] - item_base_cost[str(j['beforeId'])]
                        
                                if line[j['participantId']] == "TOP":
                                    event_list[TEAM1_TOP_ITEM_GOLD+team_interval] -= item_real_cost

                                elif line[j['participantId']] == "JUNGLE":
                                    event_list[TEAM1_JUNGLE_ITEM_GOLD+team_interval] -= item_real_cost

                                elif line[j['participantId']] == "MIDDLE":
                                    event_list[TEAM1_MIDDLE_ITEM_GOLD+team_interval] -= item_real_cost

                                elif line[j['participantId']] == "BOTTOM":
                                    event_list[TEAM1_BOTTOM_ITEM_GOLD+team_interval] -= item_real_cost

                                elif line[j['participantId']] == "UTILITY":
                                    event_list[TEAM1_UTILITY_ITEM_GOLD+team_interval] -= item_real_cost 

                                
                        elif j['type'] == 'WARD_PLACED':
                            if j['creatorId'] != 0:
                                team_interval = team[j['creatorId']]
                                event_list[WARD_PLACED+team_interval] += 1


                        elif j['type'] == 'WARD_KILL':
                            if j['killerId'] != 0:
                                if j['killerId'] <= 5:
                                    j['killerId'] = 6
                                    team_interval = team[j['killerId']]
                                else:
                                    j['killerId'] = 1
                                    team_interval = team[j['killerId']]
                                event_list[WARD_KILL+team_interval] += 1


                        elif j['type'] == 'ELITE_MONSTER_KILL':
                            if j['killerId'] != 0:
                                team_interval = team[j['killerId']]
                                if j['monsterType'] == 'HORDE':
                                    event_list[HORDE_COUNT+team_interval] += 1
                                elif j['monsterType'] == "DRAGON":
                                    event_list[DRAGON_COUNT+team_interval] += 1
                                elif j['monsterType'] == "RIFTHERALD":
                                    event_list[RIFTHERALD_COUNT+team_interval] += 1
                                elif j['monsterType'] == "BARON_NASHOR":
                                    event_list[BARON_NASHOR_COUNT+team_interval] += 1


                        elif j['type'] == 'CHAMPION_KILL':
                            #어시스트 골드 계산 더 찾아보기
                            if j['killerId'] != 0:
                                try:
                                    assist_participant_length = len(j['assistingParticipantIds'])
                                    assist_participant = j['assistingParticipantIds']
                                    if j['bounty'] > 300:
                                        assist_total_gold = 150
                                    elif j['bounty'] <= 300:
                                        assist_total_gold = j['bounty'] / 2
                                    assist_gold = assist_total_gold / assist_participant_length
                                except KeyError:
                                    assist_participant_length = 0
                                    assist_participant = []
                                    assist_gold = 0
                                
                                team_interval = team[j['killerId']]

                                if line[j['killerId']] == "TOP":
                                    event_list[TEAM1_TOP_GOLD+team_interval] = j['bounty']
                                    event_list[TEAM1_TOP_K+team_interval] += 1
                                
                                elif line[j['killerId']] == "JUNGLE":
                                    event_list[TEAM1_JUNGLE_GOLD+team_interval] = j['bounty']
                                    event_list[TEAM1_JUNGLE_K+team_interval] += 1
                                
                                elif line[j['killerId']] == "MIDDLE":
                                    event_list[TEAM1_MIDDLE_GOLD+team_interval] = j['bounty']
                                    event_list[TEAM1_MIDDLE_K+team_interval] += 1
                                
                                elif line[j['killerId']] == "BOTTOM":
                                    event_list[TEAM1_BOTTOM_GOLD+team_interval] = j['bounty']
                                    event_list[TEAM1_BOTTOM_K+team_interval] += 1
                                
                                elif line[j['killerId']] == "UTILITY":
                                    event_list[TEAM1_UTILITY_GOLD+team_interval] = j['bounty']
                                    event_list[TEAM1_UTILITY_K+team_interval] += 1
                                        
                                for assist in assist_participant:

                                    if line[assist] == "TOP":
                                        event_list[TEAM1_TOP_GOLD+team_interval] = assist_gold
                                        event_list[TEAM1_TOP_A+team_interval] += 1

                                    elif line[assist] == "JUNGLE":
                                        event_list[TEAM1_JUNGLE_GOLD+team_interval] = assist_gold
                                        event_list[TEAM1_JUNGLE_A+team_interval] += 1
                                    
                                    elif line[assist] == "MIDDLE":
                                        event_list[TEAM1_MIDDLE_GOLD+team_interval] = assist_gold
                                        event_list[TEAM1_MIDDLE_A+team_interval] += 1
                                    
                                    elif line[assist] == "BOTTOM":
                                        event_list[TEAM1_BOTTOM_GOLD+team_interval] = assist_gold
                                        event_list[TEAM1_BOTTOM_A+team_interval] += 1
                                    
                                    elif line[assist] == "UTILITY":
                                        event_list[TEAM1_UTILITY_GOLD+team_interval] = assist_gold
                                        event_list[TEAM1_UTILITY_A+team_interval] += 1
                                    
                                team_interval = team[j['victimId']]

                                if line[j['victimId']] == "TOP":
                                    event_list[TEAM1_TOP_D+team_interval] += 1

                                elif line[j['victimId']] == "JUNGLE":
                                    event_list[TEAM1_JUNGLE_D+team_interval] += 1
                                
                                elif line[j['victimId']] == "MIDDLE":
                                    event_list[TEAM1_MIDDLE_D+team_interval] += 1
                                
                                elif line[j['victimId']] == "BOTTOM":
                                    event_list[TEAM1_BOTTOM_D+team_interval] += 1
                                
                                elif line[j['victimId']] == "UTILITY":
                                    event_list[TEAM1_UTILITY_D+team_interval] += 1


                        elif j['type'] == 'BUILDING_KILL':
                            if j['killerId'] == 0 and j['teamId'] == 100: #빨간팀 미니언 (팀id는 무너진 팀id임)
                                team_interval = team[6]
                            elif j['killerId'] == 0 and j['teamId'] == 200: #파란팀 미니언
                                team_interval = team[1]
                            else:
                                team_interval = team[j['killerId']]

                            if j['laneType'] == "TOP_LANE":
                                event_list[TOWER_TOP_COUNT+team_interval] += 1

                            elif j['laneType'] == "MID_LANE":
                                event_list[TOWER_MIDDLE_COUNT+team_interval] += 1
                                
                            elif j['laneType'] == "BOT_LANE":
                                event_list[TOWER_BOTTOM_COUNT+team_interval] += 1
                                
                        else:
                            continue
                        
                        event_list[-1] = 1111
                        event_list_result.append(event_list)

        except KeyError as e:
            print(f"KeyError 발생: {e}")
            event_list_result = []

        return event_list_result

    def get_participant_frame(self):
        try:
            with open(self.timeline_file_dir, encoding='utf-8') as f:
                initial_data = json.load(f)
            
            initial_data = initial_data['info']['frames']
            team, win_lose, line, champion, aram, perk_list = self.get_match_data()

            participant_frame_list_result = []

            if aram == 0:

                for i in initial_data:
                    
                    participant_frame_list = [0 for h in range(LIST_LEN)]

                    participant_frame_list[TIMESTAMP] = i['timestamp']

                    for j in range(1, 11):
                        team_interval = team[j]
                        if line[j] == "TOP":
                            participant_frame_list[TEAM1_TOP_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                        elif line[j] == "JUNGLE":
                            participant_frame_list[TEAM1_JUNGLE_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                        elif line[j] == "MIDDLE":
                            participant_frame_list[TEAM1_MIDDLE_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                        elif line[j] == "BOTTOM":
                            participant_frame_list[TEAM1_BOTTOM_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                        elif line[j] == "UTILITY":
                            participant_frame_list[TEAM1_UTILITY_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                        
                    participant_frame_list[-1] = 2222
                    participant_frame_list_result.append(participant_frame_list)

        except KeyError as e:
            print(f"KeyError 발생: {e}")
            participant_frame_list_result = []

        return participant_frame_list_result
                     

    def get_condition_timeline(self, interval):

        event_list = self.get_event()

        participant_frame_list = self.get_participant_frame()

        champion = self.get_match_data()[3]
        perk_list = self.get_match_data()[-1]

        interval_list_result = []

        if len(event_list) != 0 and len(participant_frame_list) != 0:

            whole_list = event_list + participant_frame_list

            whole_list = sorted(whole_list, key = lambda x: x[0])

            whole_list = np.array(whole_list, dtype=int)

            for i in range(1, len(whole_list)):
                if whole_list[i][-1] != 1111:
                    participant_list = whole_list[i].copy()
                    whole_list[i] = whole_list[i-1].copy()

                    for j in [TEAM1_TOP_GOLD, TEAM1_JUNGLE_GOLD, TEAM1_MIDDLE_GOLD, TEAM1_BOTTOM_GOLD, TEAM1_UTILITY_GOLD]:
                        whole_list[i][j] = participant_list[j]
                        whole_list[i][j+TEAM_INTERVAL] = participant_list[j+TEAM_INTERVAL]
                    continue

                sum_result = whole_list[i-1][1:-2] + whole_list[i][1:-2]
                whole_list[i][1:-2] = sum_result
                
                if whole_list[i-1][TEAM1_TOP_A] < whole_list[i][TEAM1_TOP_A]:
                    if whole_list[i-1][TEAM1_TOP_A] - whole_list[i-1][TEAM1_TOP_K] == 2:
                        whole_list[i-1][TEAM1_TOP_GOLD] += 30
                    elif whole_list[i-1][TEAM1_TOP_A] - whole_list[i-1][TEAM1_TOP_K] == 3:
                        whole_list[i-1][TEAM1_TOP_GOLD] += 40
                    elif whole_list[i-1][TEAM1_TOP_A] - whole_list[i-1][TEAM1_TOP_K] >= 4:
                        whole_list[i-1][TEAM1_TOP_GOLD] += 60

                if whole_list[i-1][TEAM1_MIDDLE_A] < whole_list[i][TEAM1_MIDDLE_A]:
                    if whole_list[i-1][TEAM1_MIDDLE_A] - whole_list[i-1][TEAM1_MIDDLE_K] == 2:
                        whole_list[i-1][TEAM1_MIDDLE_GOLD] += 30
                    elif whole_list[i-1][TEAM1_MIDDLE_A] - whole_list[i-1][TEAM1_MIDDLE_K] == 3:
                        whole_list[i-1][TEAM1_MIDDLE_GOLD] += 40
                    elif whole_list[i-1][TEAM1_MIDDLE_A] - whole_list[i-1][TEAM1_MIDDLE_K] >= 4:
                        whole_list[i-1][TEAM1_MIDDLE_GOLD] += 60

                if whole_list[i-1][TEAM1_JUNGLE_A] < whole_list[i][TEAM1_JUNGLE_A]:
                    if whole_list[i-1][TEAM1_JUNGLE_A] - whole_list[i-1][TEAM1_JUNGLE_K] == 2:
                        whole_list[i-1][TEAM1_JUNGLE_GOLD] += 30
                    elif whole_list[i-1][TEAM1_JUNGLE_A] - whole_list[i-1][TEAM1_JUNGLE_K] == 3:
                        whole_list[i-1][TEAM1_JUNGLE_GOLD] += 40
                    elif whole_list[i-1][TEAM1_JUNGLE_A] - whole_list[i-1][TEAM1_JUNGLE_K] >= 4:
                        whole_list[i-1][TEAM1_JUNGLE_GOLD] += 60   

                if whole_list[i-1][TEAM1_BOTTOM_A] < whole_list[i][TEAM1_BOTTOM_A]:
                    if whole_list[i-1][TEAM1_BOTTOM_A] - whole_list[i-1][TEAM1_BOTTOM_K] == 2:
                        whole_list[i-1][TEAM1_BOTTOM_GOLD] += 30
                    elif whole_list[i-1][TEAM1_BOTTOM_A] - whole_list[i-1][TEAM1_BOTTOM_K] == 3:
                        whole_list[i-1][TEAM1_BOTTOM_GOLD] += 40
                    elif whole_list[i-1][TEAM1_BOTTOM_A] - whole_list[i-1][TEAM1_BOTTOM_K] >= 4:
                        whole_list[i-1][TEAM1_BOTTOM_GOLD] += 60  

                if whole_list[i-1][TEAM1_UTILITY_A] < whole_list[i][TEAM1_UTILITY_A]:
                    if whole_list[i-1][TEAM1_UTILITY_A] - whole_list[i-1][TEAM1_UTILITY_K] == 2:
                        whole_list[i-1][TEAM1_UTILITY_GOLD] += 30
                    elif whole_list[i-1][TEAM1_UTILITY_A] - whole_list[i-1][TEAM1_UTILITY_K] == 3:
                        whole_list[i-1][TEAM1_UTILITY_GOLD] += 40
                    elif whole_list[i-1][TEAM1_UTILITY_A] - whole_list[i-1][TEAM1_UTILITY_K] >= 4:
                        whole_list[i-1][TEAM1_UTILITY_GOLD] += 60                           

                if whole_list[i-1][TEAM1_TOP_A+TEAM_INTERVAL] < whole_list[i][TEAM1_TOP_A+TEAM_INTERVAL]:
                    if whole_list[i-1][TEAM1_TOP_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_TOP_K+TEAM_INTERVAL] == 2:
                        whole_list[i-1][TEAM1_TOP_GOLD] += 30
                    elif whole_list[i-1][TEAM1_TOP_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_TOP_K+TEAM_INTERVAL] == 3:
                        whole_list[i-1][TEAM1_TOP_GOLD+TEAM_INTERVAL] += 40
                    elif whole_list[i-1][TEAM1_TOP_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_TOP_K+TEAM_INTERVAL] >= 4:
                        whole_list[i-1][TEAM1_TOP_GOLD+TEAM_INTERVAL] += 60

                if whole_list[i-1][TEAM1_MIDDLE_A+TEAM_INTERVAL] < whole_list[i][TEAM1_MIDDLE_A+TEAM_INTERVAL]:
                    if whole_list[i-1][TEAM1_MIDDLE_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_MIDDLE_K+TEAM_INTERVAL] == 2:
                        whole_list[i-1][TEAM1_MIDDLE_GOLD+TEAM_INTERVAL] += 30
                    elif whole_list[i-1][TEAM1_MIDDLE_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_MIDDLE_K+TEAM_INTERVAL] == 3:
                        whole_list[i-1][TEAM1_MIDDLE_GOLD+TEAM_INTERVAL] += 40
                    elif whole_list[i-1][TEAM1_MIDDLE_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_MIDDLE_K+TEAM_INTERVAL] >= 4:
                        whole_list[i-1][TEAM1_MIDDLE_GOLD+TEAM_INTERVAL] += 60

                if whole_list[i-1][TEAM1_JUNGLE_A+TEAM_INTERVAL] < whole_list[i][TEAM1_JUNGLE_A+TEAM_INTERVAL]:
                    if whole_list[i-1][TEAM1_JUNGLE_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_JUNGLE_K+TEAM_INTERVAL] == 2:
                        whole_list[i-1][TEAM1_JUNGLE_GOLD+TEAM_INTERVAL] += 30
                    elif whole_list[i-1][TEAM1_JUNGLE_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_JUNGLE_K+TEAM_INTERVAL] == 3:
                        whole_list[i-1][TEAM1_JUNGLE_GOLD+TEAM_INTERVAL] += 40
                    elif whole_list[i-1][TEAM1_JUNGLE_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_JUNGLE_K+TEAM_INTERVAL] >= 4:
                        whole_list[i-1][TEAM1_JUNGLE_GOLD+TEAM_INTERVAL] += 60   

                if whole_list[i-1][TEAM1_BOTTOM_A+TEAM_INTERVAL] < whole_list[i][TEAM1_BOTTOM_A+TEAM_INTERVAL]:
                    if whole_list[i-1][TEAM1_BOTTOM_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_BOTTOM_K+TEAM_INTERVAL] == 2:
                        whole_list[i-1][TEAM1_BOTTOM_GOLD+TEAM_INTERVAL] += 30
                    elif whole_list[i-1][TEAM1_BOTTOM_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_BOTTOM_K+TEAM_INTERVAL] == 3:
                        whole_list[i-1][TEAM1_BOTTOM_GOLD+TEAM_INTERVAL] += 40
                    elif whole_list[i-1][TEAM1_BOTTOM_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_BOTTOM_K+TEAM_INTERVAL] >= 4:
                        whole_list[i-1][TEAM1_BOTTOM_GOLD+TEAM_INTERVAL] += 60  

                if whole_list[i-1][TEAM1_UTILITY_A+TEAM_INTERVAL] < whole_list[i][TEAM1_UTILITY_A+TEAM_INTERVAL]:
                    if whole_list[i-1][TEAM1_UTILITY_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_UTILITY_K+TEAM_INTERVAL] == 2:
                        whole_list[i-1][TEAM1_UTILITY_GOLD+TEAM_INTERVAL] += 30
                    elif whole_list[i-1][TEAM1_UTILITY_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_UTILITY_K+TEAM_INTERVAL] == 3:
                        whole_list[i-1][TEAM1_UTILITY_GOLD+TEAM_INTERVAL] += 40
                    elif whole_list[i-1][TEAM1_UTILITY_A+TEAM_INTERVAL] - whole_list[i-1][TEAM1_UTILITY_K+TEAM_INTERVAL] >= 4:
                        whole_list[i-1][TEAM1_UTILITY_GOLD+TEAM_INTERVAL] += 60                  

            s_d = [TEAM1_TOP_STATPERK_DEFENCE, TEAM1_JUNGLE_STATPERK_DEFENCE, TEAM1_MIDDLE_STATPERK_DEFENCE, TEAM1_BOTTOM_STATPERK_DEFENCE, TEAM1_UTILITY_STATPERK_DEFENCE]
            s_f = [TEAM1_TOP_STATPERK_FLEX, TEAM1_JUNGLE_STATPERK_FLEX, TEAM1_MIDDLE_STATPERK_FLEX, TEAM1_BOTTOM_STATPERK_FLEX, TEAM1_UTILITY_STATPERK_FLEX]
            s_o = [TEAM1_TOP_STATPERK_OFFENSE, TEAM1_JUNGLE_STATPERK_OFFENSE, TEAM1_MIDDLE_STATPERK_OFFENSE, TEAM1_BOTTOM_STATPERK_OFFENSE, TEAM1_UTILITY_STATPERK_OFFENSE]
            p_1 = [TEAM1_TOP_PRIMARY1, TEAM1_JUNGLE_PRIMARY1, TEAM1_MIDDLE_PRIMARY1, TEAM1_BOTTOM_PRIMARY1, TEAM1_UTILITY_PRIMARY1]
            p_2 = [TEAM1_TOP_PRIMARY2, TEAM1_JUNGLE_PRIMARY2, TEAM1_MIDDLE_PRIMARY2, TEAM1_BOTTOM_PRIMARY2, TEAM1_UTILITY_PRIMARY2]
            p_3 = [TEAM1_TOP_PRIMARY3, TEAM1_JUNGLE_PRIMARY3, TEAM1_MIDDLE_PRIMARY3, TEAM1_BOTTOM_PRIMARY3, TEAM1_UTILITY_PRIMARY3]
            p_4 = [TEAM1_TOP_PRIMARY4, TEAM1_JUNGLE_PRIMARY4, TEAM1_MIDDLE_PRIMARY4, TEAM1_BOTTOM_PRIMARY4, TEAM1_UTILITY_PRIMARY4]
            s_1 = [TEAM1_TOP_SUBSTYLE1, TEAM1_JUNGLE_SUBSTYLE1, TEAM1_MIDDLE_SUBSTYLE1, TEAM1_BOTTOM_SUBSTYLE1, TEAM1_UTILITY_SUBSTYLE1]
            s_2 = [TEAM1_TOP_SUBSTYLE2, TEAM1_JUNGLE_SUBSTYLE2, TEAM1_MIDDLE_SUBSTYLE2, TEAM1_BOTTOM_SUBSTYLE2, TEAM1_UTILITY_SUBSTYLE2]

            for i in whole_list:
                for j, loc in enumerate([TEAM1_TOP_CHAMPION, TEAM1_JUNGLE_CHAMPION, TEAM1_MIDDLE_CHAMPION, TEAM1_BOTTOM_CHAMPION, TEAM1_UTILITY_CHAMPION]):
                    i[loc] = champion[j+1]
                    i[loc+TEAM_INTERVAL] = champion[j+1+5]

                for h in range(5):
                    i[s_d[h]] = perk_list[h][0]
                    i[s_f[h]] = perk_list[h][1]
                    i[s_o[h]] = perk_list[h][2]
                    i[p_1[h]] = perk_list[h][3]
                    i[p_2[h]] = perk_list[h][4]
                    i[p_3[h]] = perk_list[h][5]
                    i[p_4[h]] = perk_list[h][6]
                    i[s_1[h]] = perk_list[h][7]
                    i[s_2[h]] = perk_list[h][8]

                for h in range(5, 10):
                    i[s_d[h-5]+TEAM_INTERVAL] = perk_list[h][0]
                    i[s_f[h-5]+TEAM_INTERVAL] = perk_list[h][1]
                    i[s_o[h-5]+TEAM_INTERVAL] = perk_list[h][2]
                    i[p_1[h-5]+TEAM_INTERVAL] = perk_list[h][3]
                    i[p_2[h-5]+TEAM_INTERVAL] = perk_list[h][4]
                    i[p_3[h-5]+TEAM_INTERVAL] = perk_list[h][5]
                    i[p_4[h-5]+TEAM_INTERVAL] = perk_list[h][6]
                    i[s_1[h-5]+TEAM_INTERVAL] = perk_list[h][7]
                    i[s_2[h-5]+TEAM_INTERVAL] = perk_list[h][8]

                
                team1_gold = 0
                team2_gold = 0

                for j in [TEAM1_TOP_GOLD, TEAM1_JUNGLE_GOLD, TEAM1_MIDDLE_GOLD, TEAM1_BOTTOM_GOLD, TEAM1_UTILITY_GOLD]:
                    team1_gold += i[j]
                    team2_gold += i[j+TEAM_INTERVAL]
                    
                i[TEAM1_GOLD] = team1_gold
                i[TEAM1_GOLD+TEAM_INTERVAL] = team2_gold

            max_timeline = np.max(whole_list[:, 0])

            for i in range(0, max_timeline, interval):
                interval_list = [sublist for sublist in whole_list if sublist[0] <= i]
                interval_list[-1][0] = i
                interval_list_result.append(interval_list[-1][:LIST_LEN-1].copy())
                interval_list_result[-1] = interval_list_result[-1].tolist()
                    
        return interval_list_result