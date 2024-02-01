from utils import PreprocessData
import numpy as np

test = PreprocessData('C:/GitHub/predict_gg/backend/api_match_info.json', 'C:/GitHub/predict_gg/backend/api_timeline_info.json')

f = open("log.txt", 'w')
#test.get_data('젠지 한별')

event_list = test.get_event()

participant_frame_list = test.get_participant_frame()

whole_list = event_list + participant_frame_list

whole_list = sorted(whole_list, key = lambda x: x[0])

whole_list = np.array(whole_list, dtype=int)



for i in range(1, len(whole_list)):
    if whole_list[i][1] != 0:
        #수정
        whole_list[i][7:10] = whole_list[i-1][7:10]
        whole_list[i][7+9:10+9] = whole_list[i-1][7+9:10+9]
        continue

    sum_result = whole_list[i-1][1:-1] + whole_list[i][1:-1]
    whole_list[i][1:-1] = sum_result


np.savetxt(f, whole_list, fmt='%10d', delimiter='   ')



f.close()