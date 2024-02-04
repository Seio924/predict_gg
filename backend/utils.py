import json
import numpy as np

TIMESTAMP = 0

TEAM1_TOP_CHAMPION = 1
TEAM1_TOP_GOLD = 2
TEAM1_TOP_POTION = 3
TEAM1_TOP_K = 4
TEAM1_TOP_D = 5
TEAM1_TOP_A = 6

TEAM1_JUNGLE_CHAMPION = 7
TEAM1_JUNGLE_GOLD = 8
TEAM1_JUNGLE_POTION = 9
TEAM1_JUNGLE_K = 10
TEAM1_JUNGLE_D = 11
TEAM1_JUNGLE_A = 12

TEAM1_MIDDLE_CHAMPION = 13
TEAM1_MIDDLE_GOLD = 14
TEAM1_MIDDLE_POTION = 15
TEAM1_MIDDLE_K = 16
TEAM1_MIDDLE_D = 17
TEAM1_MIDDLE_A = 18

TEAM1_BOTTOM_CHAMPION = 19
TEAM1_BOTTOM_GOLD = 20
TEAM1_BOTTOM_POTION = 21
TEAM1_BOTTOM_K = 22
TEAM1_BOTTOM_D = 23
TEAM1_BOTTOM_A = 24

TEAM1_UTILITY_CHAMPION = 25
TEAM1_UTILITY_GOLD = 26
TEAM1_UTILITY_POTION = 27
TEAM1_UTILITY_K = 28
TEAM1_UTILITY_D = 29
TEAM1_UTILITY_A = 30

TEAM1_GOLD = 31

START_ITEM = 32
TIER1_ITEM = 33
TIER2_ITEM = 34
TIER3_ITEM = 35
BOOTS_ITEM = 36
SPECIAL_ITEM = 37
WARD_ITEM = 38

WARD_COUNT = 39
OBJECT_COUNT = 40

TOWER_TOP_COUNT = 41
TOWER_MIDDLE_COUNT = 42
TOWER_BOTTOM_COUNT = 43

TEAM_INTERVAL = 43

LIST_LEN = 88

class PreprocessData():
    def __init__(self, match_file_dir, timeline_file_dir):
        self.match_file_dir = match_file_dir
        self.timeline_file_dir = timeline_file_dir
    
    def get_match_data(self):

        with open(self.match_file_dir, encoding='utf-8') as f:
            initial_match_data = json.load(f)

        if 'status' in initial_match_data:
            return 0
        else:
            aram = 1
            win_lose = [0, 0] #어떤 팀이 이겼는지 [team1, team2]
            team = {}
            line = {}
            champion_list = ["MONKEYKING", "SMOLDER", "AATROX", "AHRI", "AKALI", "AKSHAN", "ALISTAR", "AMUMU", "ANIVIA", "ANNIE", "APHELIOS", "ASHE", "AURELIONSOL", "AZIR", "BARD", "BELVETH", "BLITZCRANK", "BRAND", "BRAUM", "BRIAR", "CAITLYN", "CAMILLE", "CASSIOPEIA", "CHOGATH", "CORKI", "DARIUS", "DIANA", "DRMUNDO", "DRAVEN", "EKKO", "ELISE", "EVELYNN", "EZREAL", "FIDDLESTICKS", "FIORA", "FIZZ", "GALIO", "GANGPLANK", "GAREN", "GNAR", "GRAGAS", "GRAVES", "GWEN", "HECARIM", "HEIMERDINGER", "HWEI", "ILLAOI", "IRELIA", "IVERN", "JANNA", "JARVANIV", "JAX", "JAYCE", "JHIN", "JINX", "KSANTE", "KAISA", "KALISTA", "KARMA", "KARTHUS", "KASSADIN", "KATARINA", "KAYLE", "KAYN", "KENNEN", "KHAZIX", "KINDRED", "KLED", "KOGMAW", "LEBLANC", "LEESIN", "LEONA", "LILLIA", "LISSANDRA", "LUCIAN", "LULU", "LUX", "MALPHITE", "MALZAHAR", "MAOKAI", "MASTERYI", "MILIO", "MISSFORTUNE", "MORDEKAISER", "MORGANA", "NAAFIRI", "NAMI", "NASUS", "NAUTILUS", "NEEKO", "NIDALEE", "NILAH", "NOCTURNE", "NUNU", "OLAF", "ORIANNA", "ORNN", "PANTHEON", "POPPY", "PYKE", "QIYANA", "QUINN", "RAKAN", "RAMMUS", "REKSAI", "RELL", "RENATA", "RENEKTON", "RENGAR", "RIVEN", "RUMBLE", "RYZE", "SAMIRA", "SEJUANI", "SENNA", "SERAPHINE", "SETT", "SHACO", "SHEN", "SHYVANA", "SINGED", "SION", "SIVIR", "SKARNER", "SONA", "SORAKA", "SWAIN", "SYLAS", "SYNDRA", "TAHMKENCH", "TALIYAH", "TALON", "TARIC", "TEEMO", "THRESH", "TRISTANA", "TRUNDLE", "TRYNDAMERE", "TWISTEDFATE", "TWITCH", "UDYR", "URGOT", "VARUS", "VAYNE", "VEIGAR", "VELKOZ", "VEX", "VI", "VIEGO", "VIKTOR", "VLADIMIR", "VOLIBEAR", "WARWICK", "WUKONG", "XAYAH", "XERATH", "XINZHAO", "YASUO", "YONE", "YORICK", "YUUMI", "ZAC", "ZED", "ZERI", "ZIGGS", "ZILEAN", "ZOE", "ZYRA"]
            champion_dic = {}
            champion = {}

            for i, c in enumerate(champion_list):
                champion_dic[c] = i

            if initial_match_data['info']["gameMode"] != "ARAM":
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


            return (team, win_lose, line, champion, aram)

    def get_item_data(self):
        with open('./backend/item.json', encoding="utf-8") as f:
            item_data = json.load(f)

        boots = ['장화', '약간 신비한 신발', '신속의 장화', '명석함의 아이오니아 장화', '기동력의 장화', '광전사의 군화', '마법사의 신발', '판금 장화', '헤르메스의 발걸음']
        start = ['암흑의 인장', '여신의 눈물', '도란의 반지', '도란의 검', '수확의 낫', '도란의 방패', '새끼 화염발톱', '새끼 바람돌이', '새끼 이끼쿵쿵이', '세계 지도집', '룬 나침반', '세계의 결실']
        tier1 = ['빛나는 티끌', '요정의 부적', '단검', '천 갑옷', '원기 회복의 구슬', '사파이어 수정', '롱소드', '증폭의 고서', '루비 수정', '마법무효화의 망토', '민첩성의 망토', '방출의 마법봉', '곡괭이', '쓸데없이 큰 지팡이', 'B.F. 대검']
        tier2 = ["처형인의 대검", "흡혈의 낫", "광휘의 검", "콜필드의 전투 망치", "땅굴 채굴기", "탐식의 망치", "티아맷", "강철 인장", "주문포식자", "곡궁", "키르히아이스의 파편", "열정의 검", "온기가 필요한 자의 도끼", "절정의 화살", "수은 장식띠", "최후의 속삭임", "꽁지깃", "톱날 단검", "야수화", "망각의 구", "에테르 환영", "악마의 마법서", "마법공학 교류 발전기", "역병의 보석", "사라진 양피지", "억겁의 카탈리스트", "기괴한 가면", "추적자의 팔목 보호대", "부서진 팔목 보호대", "신록의 장벽", "점화석", "쇠사슬 조끼", "덤불 조끼", "수정 팔 보호구", "비상의 월갑", "얼음 방패", "음전자 망토", "거인의 허리띠", "파수꾼의 갑옷", "바미의 불씨", "망령의 두건", "금지된 우상", "밴들유리 거울", "감시하는 와드석"]
        tier3 = ['마법사의 최후', '강철심장', '무덤꽃', '정수 약탈자', '월식', '맬모셔스의 아귀', '화공 펑크 사슬검', '마나무네', '무라마나', '실험적 마공학판', '선체파괴자', '칠흑의 양날 도끼', '스테락의 도전', '발걸음 분쇄기', '쇼진의 창', '갈라진 하늘', '몰락한 왕의 검', '죽음의 무도', '수호 천사', '굶주린 히드라', '거대한 히드라', '삼위일체', '루난의 허리케인', '유령 무희', '구인수의 격노검', '징수의 총', '크라켄 학살자', '스태틱의 단검', '고속 연사포', '정수 약 탈자', '불멸의 철갑궁', '헤르메스의 시미터', '필멸자의 운명', '도미닉 경의 인사', '경계', '폭풍갈퀴', '무한의 대검', '나보리 신속검', '피바라기', '독사의 송곳니', '그림자 검', '요우무의 유령검', '기회', '밤의 끝자락', '벼락폭풍검', '오만', '원칙의 원형낫', '불경한 히드라', '세릴다의 원한', '메자이의 영혼약탈자', '모렐로노미콘', '마법공학 로켓 벨트', '영겁의 지팡이', '라일라이의 수정홀', '지평선의 초점', '악의', '무 덤꽃', '폭풍 쇄도', '루덴의 동반자', '대천사의 지팡이', '대천사의 포옹', '내셔의 이빨', '리안드리의 고통', '우주의 추진력', '균열 생성기', '공허의 지팡이', '밴시의 장막', '리치베인', '그림자불꽃', '존야의 모래시계', '라바돈의 죽음모자', '지크의 융합', '얼어붙은 심장', '혹한의 손길', '종말의 겨울', '심연의 가면', '증오의 사슬', '얼어붙은 건틀릿', '가시 갑옷', '란두인의 예언', '태양불꽃 방패', '끝없는 절망', '대자연의 힘', '공허한 광휘', '정령의 형상', '케이닉 루컨', '망자의 갑옷', '강 철심장', '워모그의 갑옷', '해신 작쇼', '자자크의 세계가시', '피의 노래', '태양의 썰매', '꿈 생성기', '천상의 이의', '슈렐리아의 군가', '헬리아의 메아리', '월석 재생기', '기사의 맹세', '강철의 솔라리 펜던트', '제국의 명령', '불타는 향로', '흐르는 물의 지팡이', '구원', '미카엘의 축복', '경계의 와드석', '개척자', '새벽심장']
        special = ['가차없는 포격', '수호자의 뿔피리', '포로 간식', '죽음의 여신', '사기진작', '천체 정렬', '터.보.추.진.기', '흑요석 양날 도끼', '몽상파쇄자', '쇼진의 결의', '천상의 몰락', '무한한 삼위일체', '들끓는 슬픔', '쓰러진 용의 제물', '폭풍의 눈', '궁극의 검', '요우무의 각성', '확실성', '선풍검', '영혼의 평정', '업그레이드 비행팩', '무한 융합', '다수의 원한', '무기의 위력', '남작의 선물', '리안드리의 슬픔', '이케시아의 저주', '라바돈의 죽음왕관', '얼어붙은 주먹', '떠도는 희망', '레비아탄', '무언의 기생갑', '슈렐리아의 진혼곡', '비명을 지르는 도시의 외침', '성운 투척기', '황금 새벽의 유물함', '해오름', '칼리스타의 칠흑의 창', '수당', '허수아비', '굳건한 의지의 완전한 비스킷', '미니언 해체분석기', '약간 신비한 신발', '탐욕의 영약', '힘의 영약', '숙련의 영약', '전령의 눈', '흑요석 검', '아낌없이 주는 지팡이', '반딧불이 물약']
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
                item_tear[i] = 'boots'

            elif item_data['data'][i]['name'] in start:
                item_tear[i] = 'start'

            elif item_data['data'][i]['name'] in tier1:
                item_tear[i] = 'tier1'

            elif item_data['data'][i]['name'] in tier2:
                item_tear[i] = 'tier2'
            
            elif item_data['data'][i]['name'] in tier3:
                item_tear[i] = 'tier3'
            
            elif item_data['data'][i]['name'] in special:
                item_tear[i] = 'special'

            elif item_data['data'][i]['name'] in potion:
                item_tear[i] = 'potion'

            elif item_data['data'][i]['name'] in ward:
                item_tear[i] = 'ward'

        return (item_tear, item_cost, item_sold_cost)
  
    def get_item_from_data(self, beforeId):
        with open('./backend/item.json', encoding="utf-8") as f:
            item_data = json.load(f)       
        item_info = item_data['data'].get(beforeId, {})
        item_from = item_info.get('from', [])
        return item_from

    def get_event(self):
        with open(self.timeline_file_dir, encoding='utf-8') as f:
            initial_data = json.load(f)

        if 'status' in initial_data:
            return 0
        else:
            initial_data = initial_data['info']['frames']
            item_tear, item_cost, item_sold_cost = self.get_item_data()
            team, win_lose, line, champion, aram = self.get_match_data()

            event_list_result = []

            if aram == 0:

                for i in initial_data:
                    for j in i['events']:
                        event_list = [0 for h in range(LIST_LEN)]
                        event_list[TIMESTAMP] = j['timestamp']

                        match j['type']:
                            case 'ITEM_PURCHASED':
                                team_interval = team[j['participantId']]
                                
                                match item_tear[str(j['itemId'])]:
                                    case "boots" | "potion":
                                        match line[j['participantId']]:
                                            case "TOP":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_TOP_POTION+team_interval] += 1
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] += 10000
                                            case "JUNGLE":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_JUNGLE_POTION+team_interval] += 1
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] += 1000
                                            case "MIDDLE":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_MIDDLE_POTION+team_interval] += 1
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] += 100
                                            case "BOTTOM":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_BOTTOM_POTION+team_interval] += 1
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] += 10
                                            case "UTILITY":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_UTILITY_POTION+team_interval] += 1
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] += 1
                                    case "start":
                                        event_list[START_ITEM+team_interval] += 1
                                    case "tier1":
                                        event_list[TIER1_ITEM+team_interval] += 1
                                    case "tier2":
                                        event_list[TIER2_ITEM+team_interval] += 1
                                    case "tier3":
                                        event_list[TIER3_ITEM+team_interval] += 1
                                    case "special":
                                        event_list[SPECIAL_ITEM+team_interval] += 1
                                    case "ward":
                                        event_list[WARD_ITEM+team_interval] += 1


                            case 'ITEM_DESTROYED':
                                team_interval = team[j['participantId']]

                                match item_tear[str(j['itemId'])]:
                                    case "boots" | "potion":
                                        match line[j['participantId']]:
                                            case "TOP":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_TOP_POTION+team_interval] -= 1
                                                    event_list[TEAM1_TOP_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 10000
                                            case "JUNGLE":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_JUNGLE_POTION+team_interval] -= 1
                                                    event_list[TEAM1_JUNGLE_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 1000
                                            case "MIDDLE":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_MIDDLE_POTION+team_interval] -= 1
                                                    event_list[TEAM1_MIDDLE_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 100
                                            case "BOTTOM":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_BOTTOM_POTION+team_interval] -= 1
                                                    event_list[TEAM1_BOTTOM_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 10
                                            case "UTILITY":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_UTILITY_POTION+team_interval] -= 1
                                                    event_list[TEAM1_UTILITY_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 1
                                    case "start":
                                        event_list[START_ITEM+team_interval] -= 1
                                    case "tier1":
                                        event_list[TIER1_ITEM+team_interval] -= 1
                                    case "tier2":
                                        event_list[TIER2_ITEM+team_interval] -= 1
                                    case "tier3":
                                        event_list[TIER3_ITEM+team_interval] -= 1
                                    case "special":
                                        event_list[SPECIAL_ITEM+team_interval] -= 1
                                    case "ward":
                                        event_list[WARD_ITEM+team_interval] -= 1


                            case 'ITEM_SOLD':
                                team_interval = team[j['participantId']]
                                minus_gold = item_sold_cost[str(j['itemId'])] - item_cost[str(j['itemId'])]

                                match item_tear[str(j['itemId'])]:
                                    case "boots" | "potion":
                                        match line[j['participantId']]:
                                            case "TOP":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_TOP_POTION+team_interval] -= 1
                                                    event_list[TEAM1_TOP_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 10000
                                            case "JUNGLE":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_JUNGLE_POTION+team_interval] -= 1
                                                    event_list[TEAM1_JUNGLE_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 1000
                                            case "MIDDLE":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_MIDDLE_POTION+team_interval] -= 1
                                                    event_list[TEAM1_MIDDLE_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 100
                                            case "BOTTOM":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_BOTTOM_POTION+team_interval] -= 1
                                                    event_list[TEAM1_BOTTOM_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 10
                                            case "UTILITY":
                                                if item_tear[str(j['itemId'])] == "potion":
                                                    event_list[TEAM1_UTILITY_POTION+team_interval] -= 1
                                                    event_list[TEAM1_UTILITY_GOLD+team_interval] -= item_cost[str(j['itemId'])]
                                                else:
                                                    event_list[BOOTS_ITEM+team_interval] -= 1
                                    case "start":
                                        event_list[START_ITEM+team_interval] -= 1
                                    case "tier1":
                                        event_list[TIER1_ITEM+team_interval] -= 1
                                    case "tier2":
                                        event_list[TIER2_ITEM+team_interval] -= 1
                                    case "tier3":
                                        event_list[TIER3_ITEM+team_interval] -= 1
                                    case "special":
                                        event_list[SPECIAL_ITEM+team_interval] -= 1
                                    case "ward":
                                        event_list[WARD_ITEM+team_interval] -= 1
                                
                                match line[j['participantId']]:
                                    case "TOP":
                                        event_list[TEAM1_TOP_GOLD+team_interval] = minus_gold
                                    case "JUNGLE":
                                        event_list[TEAM1_JUNGLE_GOLD+team_interval] = minus_gold
                                    case "MIDDLE":
                                        event_list[TEAM1_MIDDLE_GOLD+team_interval] = minus_gold
                                    case "BOTTOM":
                                        event_list[TEAM1_BOTTOM_GOLD+team_interval] = minus_gold
                                    case "UTILITY":
                                        event_list[TEAM1_UTILITY_GOLD+team_interval] = minus_gold
                                
                                event_list[TEAM1_GOLD+team_interval] = minus_gold
        
                            case 'ITEM_UNDO':
                                team_interval = team[j['participantId']]
                                if j['beforeId'] == 0:
                                    # beforeId가 0이라는 말은 팔았던걸 되돌렸다는 말. 그러면 afterId만큼 tear를 올려줘야 한다.
                                    # 판금 장화 가지고 있는데 이걸 판다. 그리고 UNDO before 0 after 3000
                                    #event_list[9] += item_tear[str(j['afterId'])]
                                    match item_tear[str(j['afterId'])]:
                                        case "boots" | "potion":
                                            match line[j['participantId']]:
                                                case "TOP":
                                                    if item_tear[str(j['afterId'])] == "potion":
                                                        event_list[TEAM1_TOP_POTION+team_interval] += 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] += 10000
                                                case "JUNGLE":
                                                    if item_tear[str(j['afterId'])] == "potion":
                                                        event_list[TEAM1_JUNGLE_POTION+team_interval] += 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] += 1000
                                                case "MIDDLE":
                                                    if item_tear[str(j['afterId'])] == "potion":
                                                        event_list[TEAM1_MIDDLE_POTION+team_interval] += 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] += 100
                                                case "BOTTOM":
                                                    if item_tear[str(j['afterId'])] == "potion":
                                                        event_list[TEAM1_BOTTOM_POTION+team_interval] += 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] += 10
                                                case "UTILITY":
                                                    if item_tear[str(j['afterId'])] == "potion":
                                                        event_list[TEAM1_UTILITY_POTION+team_interval] += 1
                                                        
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] += 1
                                        case "start":
                                            event_list[START_ITEM+team_interval] += 1
                                        case "tier1":
                                            event_list[TIER1_ITEM+team_interval] += 1
                                        case "tier2":
                                            event_list[TIER2_ITEM+team_interval] += 1
                                        case "tier3":
                                            event_list[TIER3_ITEM+team_interval] += 1
                                        case "special":
                                            event_list[SPECIAL_ITEM+team_interval] += 1
                                        case "ward":
                                            event_list[WARD_ITEM+team_interval] += 1
                                        
                                else:
                                    # beforeId가 0이 아니라는 말은 샀던걸 되돌렸다는 말. 그러면 beforeId만큼 tear를 내려줘야한다. 대신 상위아이템인 경우는 하위아이템만큼 더해준다.
                                    #시작아이템 물약2 + 신발 UNDO3번 before 2003 after 0
                                    match item_tear[str(j['beforeId'])]:
                                        case "boots" | "potion":
                                            match line[j['participantId']]:
                                                case "TOP":
                                                    if item_tear[str(j['beforeId'])] == "potion":
                                                        event_list[TEAM1_TOP_POTION+team_interval] -= 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] -= 10000
                                                case "JUNGLE":
                                                    if item_tear[str(j['beforeId'])] == "potion":
                                                        event_list[TEAM1_JUNGLE_POTION+team_interval] -= 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] -= 1000
                                                case "MIDDLE":
                                                    if item_tear[str(j['beforeId'])] == "potion":
                                                        event_list[TEAM1_MIDDLE_POTION+team_interval] -= 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] -= 100
                                                case "BOTTOM":
                                                    if item_tear[str(j['beforeId'])] == "potion":
                                                        event_list[TEAM1_BOTTOM_POTION+team_interval] -= 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] -= 10
                                                case "UTILITY":
                                                    if item_tear[str(j['beforeId'])] == "potion":
                                                        event_list[TEAM1_UTILITY_POTION+team_interval] -= 1
                                                    else:
                                                        event_list[BOOTS_ITEM+team_interval] -= 1
                                        case "start":
                                            event_list[START_ITEM+team_interval] -= 1
                                        case "tier1":
                                            event_list[TIER1_ITEM+team_interval] -= 1
                                        case "tier2":
                                            event_list[TIER2_ITEM+team_interval] -= 1
                                        case "tier3":
                                            event_list[TIER3_ITEM+team_interval] -= 1
                                        case "special":
                                            event_list[SPECIAL_ITEM+team_interval] -= 1
                                        case "ward":
                                            event_list[WARD_ITEM+team_interval] -= 1
                                    item_from_data = self.get_item_from_data(str(j['beforeId']))
                                    for i in item_from_data:
                                        match item_tear[str(i)]:
                                            case "boots" | "potion":
                                                match line[j['participantId']]:
                                                    case "TOP":
                                                        if item_tear[str(i)] == "potion":
                                                            event_list[TEAM1_TOP_POTION+team_interval] += 1
                                                        else:
                                                            event_list[BOOTS_ITEM+team_interval] += 10000
                                                    case "JUNGLE":
                                                        if item_tear[str(i)] == "potion":
                                                            event_list[TEAM1_JUNGLE_POTION+team_interval] += 1
                                                        else:
                                                            event_list[BOOTS_ITEM+team_interval] += 1000
                                                    case "MIDDLE":
                                                        if item_tear[str(i)] == "potion":
                                                            event_list[TEAM1_MIDDLE_POTION+team_interval] += 1
                                                        else:
                                                            event_list[BOOTS_ITEM+team_interval] += 100
                                                    case "BOTTOM":
                                                        if item_tear[str(i)] == "potion":
                                                            event_list[TEAM1_BOTTOM_POTION+team_interval] += 1
                                                        else:
                                                            event_list[BOOTS_ITEM+team_interval] += 10
                                                    case "UTILITY":
                                                        if item_tear[str(i)] == "potion":
                                                            event_list[TEAM1_UTILITY_POTION+team_interval] += 1
                                                        else:
                                                            event_list[BOOTS_ITEM+team_interval] += 1
                                            case "start":
                                                event_list[START_ITEM+team_interval] += 1
                                            case "tier1":
                                                event_list[TIER1_ITEM+team_interval] += 1
                                            case "tier2":
                                                event_list[TIER2_ITEM+team_interval] += 1
                                            case "tier3":
                                                event_list[TIER3_ITEM+team_interval] += 1
                                            case "special":
                                                event_list[SPECIAL_ITEM+team_interval] += 1
                                            case "ward":
                                                event_list[WARD_ITEM+team_interval] += 1

                            case 'WARD_PLACED':
                                if j['creatorId'] != 0:
                                    team_interval = team[j['creatorId']]

                                    event_list[WARD_COUNT+team_interval] += 1

                            case 'WARD_KILL':
                                if j['killerId'] != 0:

                                    team_interval = team[j['killerId']]

                                    event_list[WARD_COUNT+team_interval] -= 1

                            case 'ELITE_MONSTER_KILL':
                                if j['killerId'] != 0:

                                    team_interval = team[j['killerId']]

                                    event_list[OBJECT_COUNT+team_interval] += 1

                            case 'CHAMPION_KILL':
                                # if j['killerId'] != 0:

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
                                
                                if j['killerId'] != 0:
                                    team_interval = team[j['killerId']]
                                    match line[j['killerId']]:
                                        case "TOP":
                                            event_list[TEAM1_TOP_GOLD+team_interval] = j['bounty']
                                            event_list[TEAM1_TOP_K+team_interval] += 1
                                        case "JUNGLE":
                                            event_list[TEAM1_JUNGLE_GOLD+team_interval] = j['bounty']
                                            event_list[TEAM1_JUNGLE_K+team_interval] += 1
                                        case "MIDDLE":
                                            event_list[TEAM1_MIDDLE_GOLD+team_interval] = j['bounty']
                                            event_list[TEAM1_MIDDLE_K+team_interval] += 1
                                        case "BOTTOM":
                                            event_list[TEAM1_BOTTOM_GOLD+team_interval] = j['bounty']
                                            event_list[TEAM1_BOTTOM_K+team_interval] += 1
                                        case "UTILITY":
                                            event_list[TEAM1_UTILITY_GOLD+team_interval] = j['bounty']
                                            event_list[TEAM1_UTILITY_K+team_interval] += 1

                                for assist in assist_participant:
                                    
                                    match line[assist]:
                                        case "TOP":
                                            event_list[TEAM1_TOP_GOLD+team_interval] = assist_gold
                                            event_list[TEAM1_TOP_A+team_interval] += 1
                                        case "JUNGLE":
                                            event_list[TEAM1_JUNGLE_GOLD+team_interval] = assist_gold
                                            event_list[TEAM1_JUNGLE_A+team_interval] += 1
                                        case "MIDDLE":
                                            event_list[TEAM1_MIDDLE_GOLD+team_interval] = assist_gold
                                            event_list[TEAM1_MIDDLE_A+team_interval] += 1
                                        case "BOTTOM":
                                            event_list[TEAM1_BOTTOM_GOLD+team_interval] = assist_gold
                                            event_list[TEAM1_BOTTOM_A+team_interval] += 1
                                        case "UTILITY":
                                            event_list[TEAM1_UTILITY_GOLD+team_interval] = assist_gold
                                            event_list[TEAM1_UTILITY_A+team_interval] += 1
                                
                                team_interval = team[j['victimId']]
                                match line[j['victimId']]:
                                    case "TOP":
                                        event_list[TEAM1_TOP_D+team_interval] += 1
                                    case "JUNGLE":
                                        event_list[TEAM1_JUNGLE_D+team_interval] += 1
                                    case "MIDDLE":
                                        event_list[TEAM1_MIDDLE_D+team_interval] += 1
                                    case "BOTTOM":
                                        event_list[TEAM1_BOTTOM_D+team_interval] += 1
                                    case "UTILITY":
                                        event_list[TEAM1_UTILITY_D+team_interval] += 1
                        
                            case "BUILDING_KILL":
                                if j['killerId'] == 0 and j['teamId'] == 100: #빨간팀 미니언 (팀id는 무너진 팀id임)
                                    team_interval = team[6]
                                elif j['killerId'] == 0 and j['teamId'] == 200: #파란팀 미니언
                                    team_interval = team[1]
                                else:
                                    team_interval = team[j['killerId']]
                                match j['laneType']:
                                    case "TOP_LANE":
                                        event_list[TOWER_TOP_COUNT+team_interval] += 1
                                    case "MID_LANE":
                                        event_list[TOWER_MIDDLE_COUNT+team_interval] += 1
                                    case "BOT_LANE":
                                        event_list[TOWER_BOTTOM_COUNT+team_interval] += 1

                            # case "TURRET_PLATE_DESTROYED":
                            #     if j['killerId'] == 0 and j['teamId'] == 100: #빨간팀 미니언 (팀id는 무너진 팀id임)
                            #         team_interval = team[6]
                            #     elif j['killerId'] == 0 and j['teamId'] == 200: #파란팀 미니언
                            #         team_interval = team[1]
                            #     else:
                            #         team_interval = team[j['killerId']]
                            #     match j['laneType']:
                            #         case "TOP_LANE":
                            #             event_list[TOWER_TOP_COUNT+team_interval] += 1
                            #         case "MID_LANE":
                            #             event_list[TOWER_MIDDLE_COUNT+team_interval] += 1
                            #         case "BOT_LANE":
                            #             event_list[TOWER_BOTTOM_COUNT+team_interval] += 1

                                    

                            case default:
                                continue # 만약에 미니언이나 포탑이 죽였을 떈 돈은?
                        
                        event_list[-1] = 1111
                        event_list_result.append(event_list)
                
            return event_list_result

    def get_participant_frame(self):
        with open(self.timeline_file_dir, encoding='utf-8') as f:
            initial_data = json.load(f)
        
        if 'status' in initial_data:
            return 0
        else:
            initial_data = initial_data['info']['frames']
            team, win_lose, line, champion, aram = self.get_match_data()

            participant_frame_list_result = []

            if aram == 0:

                for i in initial_data:
                    
                    participant_frame_list = [0 for h in range(LIST_LEN)]
                    team1_gold = 0
                    team2_gold = 0

                    participant_frame_list[TIMESTAMP] = i['timestamp']

                    for j in range(1, 11):
                        team_interval = team[j]

                        match line[j]:
                            case "TOP":
                                participant_frame_list[TEAM1_TOP_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                            case "JUNGLE":
                                participant_frame_list[TEAM1_JUNGLE_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                            case "MIDDLE":
                                participant_frame_list[TEAM1_MIDDLE_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                            case "BOTTOM":
                                participant_frame_list[TEAM1_BOTTOM_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']
                            case "UTILITY":
                                participant_frame_list[TEAM1_UTILITY_GOLD+team_interval] = i['participantFrames'][str(j)]['totalGold']

                    for j in [TEAM1_TOP_GOLD, TEAM1_JUNGLE_GOLD, TEAM1_MIDDLE_GOLD, TEAM1_BOTTOM_GOLD, TEAM1_UTILITY_GOLD]:
                        team1_gold += participant_frame_list[j]
                        team2_gold += participant_frame_list[j+TEAM_INTERVAL]
                        
                    participant_frame_list[TEAM1_GOLD] = team1_gold
                    participant_frame_list[TEAM1_GOLD+TEAM_INTERVAL] = team2_gold

                    participant_frame_list[-1] = 2222

                    participant_frame_list_result.append(participant_frame_list)

            return participant_frame_list_result
                     

    def get_condition_timeline(self, interval):

        event_list = self.get_event()
        if event_list == 0:
            return 0
        else:
            participant_frame_list = self.get_participant_frame()

            champion = self.get_match_data()[3]

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


                for i in whole_list:
                    for j, loc in enumerate([TEAM1_TOP_CHAMPION, TEAM1_JUNGLE_CHAMPION, TEAM1_MIDDLE_CHAMPION, TEAM1_BOTTOM_CHAMPION, TEAM1_UTILITY_CHAMPION]):
                        i[loc] = champion[j+1]
                        i[loc+TEAM_INTERVAL] = champion[j+1+5]

                

                

                max_timeline = np.max(whole_list[:, 0])

                for i in range(0, max_timeline, interval):
                    interval_list = [sublist for sublist in whole_list if sublist[0] <= i]
                    
                    interval_list[-1][0] = i
                    
                    interval_list_result.append(interval_list[-1].copy())
                
                        

            return interval_list_result