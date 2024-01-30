import json
import os

class PreprocessData():
    def __init__(self, match_file_dir, timeline_file_dir):
        self.match_file_dir = match_file_dir
        self.timeline_file_dir = timeline_file_dir
    
    def get_match_data(self):

        with open(self.match_file_dir, encoding='utf-8') as f:
            initial_match_data = json.load(f)

        all_participants_data = initial_match_data['info']['participants']

        win_lose = [0, 0] #어떤 팀이 이겼는지 [team1, team2]
        team1 = []
        team2 = []
        line = {}

        for i, participant_data in enumerate(all_participants_data):
            
            if participant_data['teamId'] == 100:
                
                team1.append([i+1, participant_data['puuid'], participant_data['riotIdGameName']])
                line[i+1] = participant_data['teamPosition']
                
                if participant_data['win'] == True:
                    win_lose[0] = 1

            elif participant_data['teamId'] == 200:

                team2.append([i+1, participant_data['puuid'], participant_data['riotIdGameName']])
                line[i+1] = participant_data['teamPosition']

                if participant_data['win'] == True:
                    win_lose[1] = 1

        return (team1,team2, win_lose, line)

    def get_item_data(self):
        with open('C:\GitHub\predict_gg/backend\item.json', encoding="utf-8") as f:
            item_data = json.load(f)

        boots = ['장화', '약간 신비한 신발', '신속의 장화', '명석함의 아이오니아 장화', '기동력의 장화', '광전사의 군화', '마법사의 신발', '판금 장화', '헤르메스의 발걸음']
        start = ['체력 물약', '충전형 물약', '부패 물약', '암흑의 인장', '여신의 눈물', '도란의 반지', '도란의 검', '수확의 낫', '도란의 방패', '새끼 화염발톱', '새끼 바람돌이', '새끼 이끼쿵쿵이', '세계 지도집', '룬 나침반', '세계의 결실']
        tier1 = ['빛나는 티끌', '요정의 부적', '단검', '천 갑옷', '원기 회복의 구슬', '사파이어 수정', '롱소드', '증폭의 고서', '루비 수정', '마법무효화의 망토', '민첩성의 망토', '방출의 마법봉', '곡괭이', '쓸데없이 큰 지팡이', 'B.F. 대검']
        tier2 = []
        tier3 = []
        special = []
        # boots : 1, start : 10, tier1 : 100, tier2 : 1000, tier3 : 10000, special : 100000

        item_tear = {}
        item_cost = {}
        item_sold_cost = {}
        
        for i in list(item_data['data'].keys()):
            item_cost[i] = item_data['data'][i]['gold']['total']
            item_sold_cost[i] = item_data['data'][i]['gold']['sell']

            if item_data['data'][i]['name'] in tier1:
                item_tear[i] = 100
            # 추가

        return (item_tear, item_cost, item_sold_cost)

    def get_event(self, team_num):
        with open(self.timeline_file_dir, encoding='utf-8') as f:
            initial_data = json.load(f)
        
        initial_data = initial_data['info']['frames']
        item_tear, item_cost, item_sold_cost = self.get_item_data()
        team1, team2, win_lose, line = self.get_match_data()

        event_list_result = []

        for i in initial_data:
            for j in i['events']:
                event_list = [0 for h in range(20)]

                match j['type']:
                    case 'ITEM_PURCHASED':
                        event_list[0] = j['timestamp']

                        if j['participantId'] in team1[:, :1]:
                            event_list[9] += item_tear[str(j['itemId'])]
                        elif j['participantId'] in team2[:, :1]:
                            event_list[9+9] += item_tear[str(j['itemId'])]

                    case 'ITEM_DESTROYED':
                        # 이상
                        event_list[0] = j['timestamp']

                        if j['participantId'] in team1[:, :1]:
                            event_list[9] -= item_tear[str(j['itemId'])]
                        elif j['participantId'] in team2[:, :1]:
                            event_list[9+9] -= item_tear[str(j['itemId'])]

                    case 'ITEM_SOLD':
                        event_list[0] = j['timestamp']

                        if j['participantId'] in team1[:, :1]:
                            event_list[9] -= item_tear[str(j['itemId'])]
                            minus_gold = item_sold_cost[str(j['itemId'])] - item_cost[str(j['itemId'])]
                            
                            match line[j['participantId']]:
                                case "TOP":
                                    event_list[1] = minus_gold
                                case "JUNGLE":
                                    event_list[2] = minus_gold
                                case "MIDDLE":
                                    event_list[3] = minus_gold
                                case "BOTTOM":
                                    event_list[4] = minus_gold
                                case "UTILITY":
                                    event_list[5] = minus_gold
                            
                            event_list[6] = minus_gold

                        elif j['participantId'] in team2[:, :1]:
                            event_list[9+9] -= item_tear[str(j['itemId'])]
                            minus_gold = item_sold_cost[str(j['itemId'])] - item_cost[str(j['itemId'])]
                            
                            match line[j['participantId']]:
                                case "TOP":
                                    event_list[1+9] = minus_gold
                                case "JUNGLE":
                                    event_list[2+9] = minus_gold
                                case "MIDDLE":
                                    event_list[3+9] = minus_gold
                                case "BOTTOM":
                                    event_list[4+9] = minus_gold
                                case "UTILITY":
                                    event_list[5+9] = minus_gold

                            event_list[6+9] = minus_gold
                            
                    case 'ITEM_UNDO':
                        event_list[0] = j['timestamp']

                        if j['participantId'] in team1[:, :1]:
                            event_list[9] -= item_tear[str(j['itemId'])]
                        elif j['participantId'] in team2[:, :1]:
                            event_list[9+9] -= item_tear[str(j['itemId'])]

                    case 'WARD_PLACED':
                        event_list[0] = j['timestamp']

                        if j['creatorId'] in team1[:, :1]:
                            event_list[7] += 1
                        elif j['creatorId'] in team2[:, :1]:
                            event_list[7+9] += 1

                    case 'WARD_KILL':
                        event_list[0] = j['timestamp']

                        if j['killerId'] in team1[:, :1]:
                            event_list[7+9] -= 1
                        elif j['killerId'] in team2[:, :1]:
                            event_list[7] -= 1

                    case 'ELITE_MONSTER_KILL':
                        event_list[0] = j['timestamp']

                        if j['killerId'] in team1[:, :1]:
                            event_list[8] += 1
                        elif j['killerId'] in team2[:, :1]:
                            event_list[8+9] += 1

                    case 'CHAMPION_KILL':
                        event_list[0] = j['timestamp']
                        assist_participant_length = len(j['assistingParticipantIds'])
                        assist_gold = 150/assist_participant_length
                        assist_participant = j['assistingParticipantIds']

                        if j['killerId'] in team1[:, :1]:
                            match line[j['killerId']]:
                                case "TOP":
                                    event_list[1] = j['bounty']
                                case "JUNGLE":
                                    event_list[2] = j['bounty']
                                case "MIDDLE":
                                    event_list[3] = j['bounty']
                                case "BOTTOM":
                                    event_list[4] = j['bounty']
                                case "UTILITY":
                                    event_list[5] = j['bounty']


                        elif j['killerId'] in team2[:, :1]:
                            match line[j['killerId']]:
                                case "TOP":
                                    event_list[1+9] = j['bounty']
                                case "JUNGLE":
                                    event_list[2+9] = j['bounty']
                                case "MIDDLE":
                                    event_list[3+9] = j['bounty']
                                case "BOTTOM":
                                    event_list[4+9] = j['bounty']
                                case "UTILITY":
                                    event_list[5+9] = j['bounty']




                

