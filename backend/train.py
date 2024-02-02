from utils import PreprocessData
from load_data import LoadData
import numpy as np

api_key = 'RGAPI-f84eef00-4bc7-4a2e-809b-bf53e67c8c52'
test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

load = LoadData(api_key)

f = open("log.txt", 'w')

load.process_challenger_data(30)


f.close()