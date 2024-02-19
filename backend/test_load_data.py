import pandas as pd
from utils import PreprocessData
import numpy as np
from load_data import LoadData

api_key = 'RGAPI-ec317f41-4135-419a-a6fa-d5f8a4ee2649'

test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

load_instance = LoadData(api_key)
# 데이터 가져오기
#interval_list = test.get_condition_timeline(10000)
#interval_list = test.get_event()
interval_list, get_win_lose_list = load_instance.get_diamond1_data_list(1)

interval_list = np.array(interval_list[0], dtype=int)

# 헤더 정의
n = [
    "TIMESTAMP",
    "TEAM1_TOP_CHAMPION", "TEAM1_TOP_GOLD", "TEAM1_TOP_ITEM_GOLD","TEAM1_TOP_POTION",
    "TEAM1_TOP_K", "TEAM1_TOP_D", "TEAM1_TOP_A",
    "TEAM1_JUNGLE_CHAMPION", "TEAM1_JUNGLE_GOLD", "TEAM1_JUNGLE_ITEM_GOLD", "TEAM1_JUNGLE_POTION",
    "TEAM1_JUNGLE_K", "TEAM1_JUNGLE_D", "TEAM1_JUNGLE_A",
    "TEAM1_MIDDLE_CHAMPION", "TEAM1_MIDDLE_GOLD", "TEAM1_MIDDLE_POTION",
    "TEAM1_MIDDLE_K", "TEAM1_MIDDLE_D", "TEAM1_MIDDLE_A",
    "TEAM1_BOTTOM_CHAMPION", "TEAM1_BOTTOM_GOLD", "TEAM1_BOTTOM_POTION",
    "TEAM1_BOTTOM_K", "TEAM1_BOTTOM_D", "TEAM1_BOTTOM_A",
    "TEAM1_UTILITY_CHAMPION", "TEAM1_UTILITY_GOLD", "TEAM1_UTILITY_POTION",
    "TEAM1_UTILITY_K", "TEAM1_UTILITY_D", "TEAM1_UTILITY_A",
    "TEAM1_GOLD",
    "BOOTS_ITEM", "WARD_ITEM",
    "WARD_COUNT", "OBJECT_COUNT",
    "TOWER_TOP_COUNT", "TOWER_MIDDLE_COUNT", "TOWER_BOTTOM_COUNT",
    "TEAM1_TOP_CHAMPION", "TEAM1_TOP_GOLD", "TEAM1_TOP_POTION",
    "TEAM1_TOP_K", "TEAM1_TOP_D", "TEAM1_TOP_A",
    "TEAM1_JUNGLE_CHAMPION", "TEAM1_JUNGLE_GOLD", "TEAM1_JUNGLE_POTION",
    "TEAM1_JUNGLE_K", "TEAM1_JUNGLE_D", "TEAM1_JUNGLE_A",
    "TEAM1_MIDDLE_CHAMPION", "TEAM1_MIDDLE_GOLD", "TEAM1_MIDDLE_POTION",
    "TEAM1_MIDDLE_K", "TEAM1_MIDDLE_D", "TEAM1_MIDDLE_A",
    "TEAM1_BOTTOM_CHAMPION", "TEAM1_BOTTOM_GOLD", "TEAM1_BOTTOM_POTION",
    "TEAM1_BOTTOM_K", "TEAM1_BOTTOM_D", "TEAM1_BOTTOM_A",
    "TEAM1_UTILITY_CHAMPION", "TEAM1_UTILITY_GOLD", "TEAM1_UTILITY_POTION",
    "TEAM1_UTILITY_K", "TEAM1_UTILITY_D", "TEAM1_UTILITY_A",
    "TEAM1_GOLD",
    "BOOTS_ITEM", "WARD_ITEM",
    "WARD_COUNT", "OBJECT_COUNT",
    "TOWER_TOP_COUNT", "TOWER_MIDDLE_COUNT", "TOWER_BOTTOM_COUNT",
    "category"
]


# DataFrame 생성
df = pd.DataFrame(data=interval_list, columns=n)

#df = pd.DataFrame(data=interval_list)


# DataFrame을 엑셀 파일로 저장
df.to_excel("log.xlsx", index=False)