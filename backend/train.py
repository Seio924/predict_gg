from utils import PreprocessData

test = PreprocessData('C:\GitHub\predict_gg/backend/api_match_info.json', 'C:\GitHub\predict_gg/backend/api_timeline_info.json')

f = open("log.txt", 'w')
#test.get_data('젠지 한별')

#event_list = test.get_event()

participant_frame_list = test.get_participant_frame()

for i in participant_frame_list:
    f.write(str(i) + '\n')

f.close()