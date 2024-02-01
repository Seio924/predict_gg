from utils import PreprocessData
import matplotlib.pyplot as plt
import numpy as np
import time

fig, axes = plt.subplots(1, 2, sharex=True, sharey=True)

for i in range(10):
    test = PreprocessData('C:/GitHub/predict_gg/api_match_info.json', 'C:/GitHub/predict_gg/api_timeline_info.json')

    interval_list = test.get_condition_timeline(10000)
    line = test.get_match_data()[-1]

    interval_list = np.array(interval_list, dtype=int)

    time = interval_list[:, 0]
    team1_gold = interval_list[:, 1:6]
    team2_gold = interval_list[:, 1+9:6+9]

    team1_std_dev = np.std(team1_gold, axis=1)
    team2_std_dev = np.std(team2_gold, axis=1)

    axes[0].plot(time, team1_std_dev, label=f'Team 1 std_dev')
    axes[1].plot(time, team2_std_dev, label=f'Team 2 std_dev')

    time.sleep(2)

axes[1].set_xlabel('Time')
axes[0].set_ylabel('Gold')
axes[1].set_ylabel('Gold')

fig.suptitle('Team gold std_dev')

axes[0].legend()
axes[0].grid(True)
axes[1].legend()
axes[1].grid(True)

plt.show()
