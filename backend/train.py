from utils import PreprocessData

test = PreprocessData('C:\GitHub\predict_gg/backend/api_match_info.json', 'C:\GitHub\predict_gg/backend/api_timeline_info.json')

#test.get_data('젠지 한별')

test.get_item_data()