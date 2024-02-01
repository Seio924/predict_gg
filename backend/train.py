from utils import PreprocessData
import numpy as np

test = PreprocessData('C:/GitHub/predict_gg/backend/api_match_info.json', 'C:/GitHub/predict_gg/backend/api_timeline_info.json')

f = open("log.txt", 'w')
#test.get_data('젠지 한별')

event_list = test.get_event()

participant_frame_list = test.get_participant_frame()

interval_list = test.get_condition_timeline(10000)


interval_list = np.array(interval_list, dtype=int)


np.savetxt(f, interval_list, fmt='%10d', delimiter=' ')



f.close()