import json
import numpy as np

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
        with open('C:/GitHub/predict_gg/backend/item.json', encoding="utf-8") as f:
            item_data = json.load(f)

        boots = ['장화', '약간 신비한 신발', '신속의 장화', '명석함의 아이오니아 장화', '기동력의 장화', '광전사의 군화', '마법사의 신발', '판금 장화', '헤르메스의 발걸음']
        start = ['암흑의 인장', '여신의 눈물', '도란의 반지', '도란의 검', '수확의 낫', '도란의 방패', '새끼 화염발톱', '새끼 바람돌이', '새끼 이끼쿵쿵이', '세계 지도집', '룬 나침반', '세계의 결실']
        tier1 = ['빛나는 티끌', '요정의 부적', '단검', '천 갑옷', '원기 회복의 구슬', '사파이어 수정', '롱소드', '증폭의 고서', '루비 수정', '마법무효화의 망토', '민첩성의 망토', '방출의 마법봉', '곡괭이', '쓸데없이 큰 지팡이', 'B.F. 대검']
        tier2 = ["처형인의 대검", "흡혈의 낫", "광휘의 검", "콜필드의 전투 망치", "땅굴 채굴기", "탐식의 망치", "티아맷", "강철 인장", "주문포식자", "곡궁", "키르히아이스의 파편", "열정의 검", "온기가 필요한 자의 도끼", "절정의 화살", "수은 장식띠", "최후의 속삭임", "꽁지깃", "톱날 단검", "야수화", "망각의 구", "에테르 환영", "악마의 마법서", "마법공학 교류 발전기", "역병의 보석", "사라진 양피지", "억겁의 카탈리스트", "기괴한 가면", "추적자의 팔목 보호대", "부서진 팔목 보호대", "신록의 장벽", "점화석", "쇠사슬 조끼", "덤불 조끼", "수정 팔 보호구", "비상의 월갑", "얼음 방패", "음전자 망토", "거인의 허리띠", "파수꾼의 갑옷", "바미의 불씨", "망령의 두건", "금지된 우상", "밴들유리 거울", "감시하는 와드석"]
        tier3 = ['마법사의 최후', '월식', '맬모셔스의 아귀', '화공 펑크 사슬검', '마나무네', '무라마나', '실험적 마공학판', '선체파괴자', '칠흑의 양날 도끼', '스테락의 도전', '발걸음 분쇄기', '쇼진의 창', '갈라진 하늘', '몰락한 왕의 검', '죽음의 무도', '수호 천사', '굶주린 히드라', '거대한 히드라', '삼위일체', '루난의 허리케인', '유령 무희', '구인수의 격노검', '징수의 총', '크라켄 학살자', '스태틱의 단검', '고속 연사포', '정수 약 탈자', '불멸의 철갑궁', '헤르메스의 시미터', '필멸자의 운명', '도미닉 경의 인사', '경계', '폭풍갈퀴', '무한의 대검', '나보리 신속검', '피바 라기', '독사의 송곳니', '그림자 검', '요우무의 유령검', '기회', '밤의 끝자락', '벼락폭풍검', '오만', '원칙의 원형낫', '불경한 히드라', '세릴다의 원한', '메자이의 영혼약탈자', '모렐로노미콘', '마법공학 로켓 벨트', '영겁의 지팡이', '라일라이의 수정홀', '지평선의 초점', '악의', '무 덤꽃', '폭풍 쇄도', '루덴의 동반자', '대천사의 지팡이', '대천사의 포옹', '내셔의 이빨', '리안드리의 고통', '우주의 추진력', '균열 생성기', '공허의 지팡이', '밴시의 장막', '리치베인', '그림자불꽃', '존야의 모래 시계', '라바돈의 죽음모자', '지크의 융합', '얼어붙은 심장', '혹한의 손길', '종말의 겨울', '심연의 가면', '증오의 사슬', '얼어붙은 건틀릿', '가시 갑옷', '란두인의 예언', '태양불꽃 방패', '끝없는 절망', '대자연의 힘', '공허한 광휘', '정령의 형상', '케이닉 루컨', '망자의 갑옷', '강 철심장', '워모그의 갑옷', '해신 작쇼', '자자크의 세계가시', '피의 노래', '태양의 썰매', '꿈 생성기', '천상의 이의', '슈렐리아의 군가', '헬리아의 메아리', '월석 재생기', '기사의 맹세', '강철의 솔라리 펜던트', ' 제국의 명령', '불타는 향로', '흐르는 물의 지팡이', '구원', '미카엘의  축복', '경계의 와드석', '개척자', '새벽심장']
        special = ['가차없는 포격', '죽음의 여신', '사기진작', '천체 정렬', '터.보.추.진.기', '흑요석 양날 도끼', '몽상파쇄자', '쇼진의 결의', '천상의 몰락', '무한한 삼위일체', '들끓는 슬픔', '쓰러진 용의 제물', '폭풍의 눈', '궁극의 검', '요우무의 각성', '확실성', '선풍검', '영혼의 평정', '업그레이드 비행팩', '무한 융합', '다수의 원한', '무기의 위력', '남작의 선물', '리안드리의 슬픔', '이케시아의 저주', '라바돈의 죽음왕관', '얼어붙은 주먹', '떠도는 희망', '레비아탄', '무언의 기생갑', '슈렐리아의 진혼곡', '비명을 지르는 도시의 외침', '성운 투척기', '황금 새벽의 유물함', '해오름', '칼리스타의 칠흑의 창', '수당', '허수아비', '굳건한 의지의 완전한 비스킷', '미니언 해체분석기', '약간 신비한 신발', '탐욕의 영약', '힘의 영약', '숙련의 영약', '전령의 눈', '흑요석 검', '아낌없이 주는 지팡이', '반딧불이 물약']
        potion = ['체력 물약', '충전형 물약', '부패 물약', '굳건한 의지의 완전한 비스킷', '마법의 영약', '분노의 영약', '강철의 영약']
        ward = ['투명 와드', '감시하는 와드석', '제어 와드', '예언자의 렌즈', '망원형 개조']
        # boots : 1, start : 10, tier1 : 100, tier2 : 1000, tier3 : 10000, special : 100000, potion : 1000000

        item_tear = {}
        item_cost = {}
        item_sold_cost = {}
        
        for i in list(item_data['data'].keys()):
            item_cost[i] = item_data['data'][i]['gold']['total']
            item_sold_cost[i] = item_data['data'][i]['gold']['sell']

            if item_data['data'][i]['name'] in boots:
                item_tear[i] = 1

            elif item_data['data'][i]['name'] in start:
                item_tear[i] = 10

            elif item_data['data'][i]['name'] in tier1:
                item_tear[i] = 100

            elif item_data['data'][i]['name'] in tier2:
                item_tear[i] = 1000
            
            elif item_data['data'][i]['name'] in tier3:
                item_tear[i] = 10000
            
            elif item_data['data'][i]['name'] in special:
                item_tear[i] = 100000

            elif item_data['data'][i]['name'] in potion:
                item_tear[i] = 1000000

            elif item_data['data'][i]['name'] in ward:
                item_tear[i] = 10000000

        return (item_tear, item_cost, item_sold_cost)

    def get_event(self):
        with open(self.timeline_file_dir, encoding='utf-8') as f:
            initial_data = json.load(f)
        
        initial_data = initial_data['info']['frames']
        item_tear, item_cost, item_sold_cost = self.get_item_data()
        team1, team2, win_lose, line = self.get_match_data()

        team1_participant_id = [item[0] for item in team1]
        team2_participant_id = [item[0] for item in team2]

        event_list_result = []

        for i in initial_data:
            for j in i['events']:
                event_list = [0 for h in range(20)]

                match j['type']:
                    case 'ITEM_PURCHASED':
                        event_list[0] = j['timestamp']

                        if j['participantId'] in team1_participant_id:
                            event_list[9] += item_tear[str(j['itemId'])]
                        elif j['participantId'] in team2_participant_id:
                            event_list[9+9] += item_tear[str(j['itemId'])]

                    case 'ITEM_DESTROYED':
                        # 이상
                        event_list[0] = j['timestamp']

                        if j['participantId'] in team1_participant_id:
                            event_list[9] -= item_tear[str(j['itemId'])]
                            
                            match line[j['participantId']]:
                                case "TOP":
                                    event_list[1] -= item_cost[str(j['itemId'])]
                                case "JUNGLE":
                                    event_list[2] -= item_cost[str(j['itemId'])]
                                case "MIDDLE":
                                    event_list[3] -= item_cost[str(j['itemId'])]
                                case "BOTTOM":
                                    event_list[4] -= item_cost[str(j['itemId'])]
                                case "UTILITY":
                                    event_list[5] -= item_cost[str(j['itemId'])]
                            
                            event_list[6] -= item_cost[str(j['itemId'])]

                        elif j['participantId'] in team2_participant_id:
                            event_list[9+9] -= item_tear[str(j['itemId'])]
                            
                            match line[j['participantId']]:
                                case "TOP":
                                    event_list[1+9] -= item_cost[str(j['itemId'])]
                                case "JUNGLE":
                                    event_list[2+9] -= item_cost[str(j['itemId'])]
                                case "MIDDLE":
                                    event_list[3+9] -= item_cost[str(j['itemId'])]
                                case "BOTTOM":
                                    event_list[4+9] -= item_cost[str(j['itemId'])]
                                case "UTILITY":
                                    event_list[5+9] -= item_cost[str(j['itemId'])]

                            event_list[6+9] -= item_cost[str(j['itemId'])]

                    case 'ITEM_SOLD':
                        event_list[0] = j['timestamp']

                        if j['participantId'] in team1_participant_id:
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

                        elif j['participantId'] in team2_participant_id:
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

                        if j['participantId'] in team1_participant_id:
                            if j['beforeId'] == 0:
                                event_list[9] -= item_tear[str(j['afterId'])]
                            else:
                                event_list[9] -= item_tear[str(j['beforeId'])]

                        elif j['participantId'] in team2_participant_id:
                            if j['beforeId'] == 0:
                                event_list[9+9] -= item_tear[str(j['afterId'])]
                            else:
                                event_list[9+9] -= item_tear[str(j['beforeId'])]

                    case 'WARD_PLACED':
                        event_list[0] = j['timestamp']

                        if j['creatorId'] in team1_participant_id:
                            event_list[7] += 1
                        elif j['creatorId'] in team2_participant_id:
                            event_list[7+9] += 1

                    case 'WARD_KILL':
                        event_list[0] = j['timestamp']

                        if j['killerId'] in team1_participant_id:
                            event_list[7+9] -= 1
                        elif j['killerId'] in team2_participant_id:
                            event_list[7] -= 1

                    case 'ELITE_MONSTER_KILL':
                        event_list[0] = j['timestamp']

                        if j['killerId'] in team1_participant_id:
                            event_list[8] += 1
                        elif j['killerId'] in team2_participant_id:
                            event_list[8+9] += 1

                    case 'CHAMPION_KILL':
                        #어시스트 골드 계산 더 찾아보기
                        event_list[0] = j['timestamp']

                        try:
                            assist_participant_length = len(j['assistingParticipantIds'])
                            assist_participant = j['assistingParticipantIds']
                            assist_gold = 150/assist_participant_length
                        except KeyError:
                            assist_participant_length = 0
                            assist_participant = []
                            assist_gold = 0

                        
                        

                        if j['killerId'] in team1_participant_id:
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

                            for assist in assist_participant:
                                match line[assist]:
                                    case "TOP":
                                        event_list[1] = assist_gold
                                    case "JUNGLE":
                                        event_list[2] = assist_gold
                                    case "MIDDLE":
                                        event_list[3] = assist_gold
                                    case "BOTTOM":
                                        event_list[4] = assist_gold
                                    case "UTILITY":
                                        event_list[5] = assist_gold


                        elif j['killerId'] in team2_participant_id:
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

                            for assist in assist_participant:
                                match line[assist]:
                                    case "TOP":
                                        event_list[1+9] = assist_gold
                                    case "JUNGLE":
                                        event_list[2+9] = assist_gold
                                    case "MIDDLE":
                                        event_list[3+9] = assist_gold
                                    case "BOTTOM":
                                        event_list[4+9] = assist_gold
                                    case "UTILITY":
                                        event_list[5+9] = assist_gold

                    case default:
                        continue
                
                event_list_result.append(event_list)
        
        return event_list_result

    def get_participant_frame(self):
        with open(self.timeline_file_dir, encoding='utf-8') as f:
            initial_data = json.load(f)
        
        initial_data = initial_data['info']['frames']
        item_tear, item_cost, item_sold_cost = self.get_item_data()
        team1, team2, win_lose, line = self.get_match_data()

        team1_participant_id = [item[0] for item in team1]
        team2_participant_id = [item[0] for item in team2]

        participant_frame_list_result = []

        for i in initial_data:
            
            participant_frame_list = [0 for h in range(20)]
            team1_gold = 0
            team2_gold = 0

            participant_frame_list[0] = i['timestamp']

            for j in range(1, 11):
                if j in team1_participant_id:
                    match line[j]:
                        case "TOP":
                            participant_frame_list[1] = i['participantFrames'][str(j)]['totalGold']
                        case "JUNGLE":
                            participant_frame_list[2] = i['participantFrames'][str(j)]['totalGold']
                        case "MIDDLE":
                            participant_frame_list[3] = i['participantFrames'][str(j)]['totalGold']
                        case "BOTTOM":
                            participant_frame_list[4] = i['participantFrames'][str(j)]['totalGold']
                        case "UTILITY":
                            participant_frame_list[5] = i['participantFrames'][str(j)]['totalGold']

                elif j in team2_participant_id:
                    match line[j]:
                        case "TOP":
                            participant_frame_list[1+9] = i['participantFrames'][str(j)]['totalGold']
                        case "JUNGLE":
                            participant_frame_list[2+9] = i['participantFrames'][str(j)]['totalGold']
                        case "MIDDLE":
                            participant_frame_list[3+9] = i['participantFrames'][str(j)]['totalGold']
                        case "BOTTOM":
                            participant_frame_list[4+9] = i['participantFrames'][str(j)]['totalGold']
                        case "UTILITY":
                            participant_frame_list[5+9] = i['participantFrames'][str(j)]['totalGold']

            team1_gold = sum(participant_frame_list[1:6])
            team2_gold = sum(participant_frame_list[1+9:6+9])

            participant_frame_list[6] = team1_gold
            participant_frame_list[6+9] = team2_gold

            participant_frame_list_result.append(participant_frame_list)

        return participant_frame_list_result
                     


                

