from utils import PreprocessData
import matplotlib.pyplot as plt
import numpy as np

test = PreprocessData('C:/GitHub/predict_gg/backend/api_match_info.json', 'C:/GitHub/predict_gg/backend/api_timeline_info.json')


interval_list = test.get_condition_timeline(10000)
line = test.get_match_data()[-1]

interval_list = np.array(interval_list, dtype=int)

time = interval_list[:, 0]
team1_gold = interval_list[:, 1:6]
team2_gold = interval_list[:, 1+9:6+9]

for i in range(1, 6):
    plt.plot(time, team1_gold[:, i-1:i], label=f'Team 1 {line[i]}')

for i in range(6, 11):
    plt.plot(time, team2_gold[:, i-6:i-5], label=f'Team 2 {line[i]}')


plt.xlabel('Time')
plt.ylabel('Gold')
plt.title('Gold Over Time')
plt.legend()
plt.grid(True)

plt.show()