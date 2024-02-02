from utils import PreprocessData
import matplotlib.pyplot as plt
import numpy as np
import time as t

fig, axes = plt.subplots(1, 2, sharex=True, sharey=True)
win_std = []
lose_std = []
min_length = float('inf')

for i in range(30):
    test = PreprocessData('C:/Users/ksb02/Documents/GitHub/predict_gg/backend/api_match_info.json', 'C:/Users/ksb02/Documents/GitHub/predict_gg/backend/api_timeline_info.json')

    interval_list = test.get_condition_timeline(10000)
    team1, team2, win_lose, line, aram = test.get_match_data()

    if aram == 1:
        t.sleep(5)
        continue

    interval_list = np.array(interval_list, dtype=int)

    time = interval_list[:, 0]
    team1_gold = interval_list[:, 1:6]
    team2_gold = interval_list[:, 1+9:6+9]

    team1_std_dev = np.std(team1_gold, axis=1)
    team2_std_dev = np.std(team2_gold, axis=1)

    min_length = min(min_length, len(team1_std_dev), len(team2_std_dev))


    if win_lose[0] == 1:
        win_std.append(team1_std_dev)
        lose_std.append(team2_std_dev)
    elif win_lose[1] == 1:
        win_std.append(team2_std_dev)
        lose_std.append(team1_std_dev)

    
    print("분석 완료")

    t.sleep(5)


win_std_mean = [sum(row[i] for row in win_std) / len(win_std) for i in range(min_length)]
lose_std_mean = [sum(row[i] for row in lose_std) / len(lose_std) for i in range(min_length)]


axes[0].plot(time[:min_length], win_std_mean, label='Win Mean std_dev')
axes[1].plot(time[:min_length], lose_std_mean, label='Lose Mean std_dev')

axes[1].set_xlabel('Time')
axes[0].set_ylabel('Gold')
axes[1].set_ylabel('Gold')

fig.suptitle('Win   Lose')

axes[0].legend()
axes[0].grid(True)
axes[1].legend()
axes[1].grid(True)

plt.show()
