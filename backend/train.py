from load_data import LoadData
from utils import PreprocessData


api_key = 'RGAPI-b5c0a11a-0ffb-48af-8aad-30a224a287ec'

test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

# 데이터 가져오기
train_data = test.get_condition_timeline(10000)

print(train_data)

