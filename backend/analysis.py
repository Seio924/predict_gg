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

team1_std_dev = np.std(team1_gold, axis=1)
team2_std_dev = np.std(team2_gold, axis=1)

team1_mean = []
team2_mean = []

print(team1_std_dev)

fig, axes = plt.subplots(1, 2, sharex=True, sharey=True)  # 두 개의 서브플롯 생성

for i in range(5):
    axes[0].plot(time, team1_gold[:, i], label=f'Team 1 {line[i+1]}')


axes[0].plot(time, team1_std_dev, label=f'Team 1 mean')


for i in range(5):
    axes[1].plot(time, team2_gold[:, i], label=f'Team 2 {line[i+6]}')


axes[1].plot(time, team2_std_dev, label=f'Team 1 mean')



axes[1].set_xlabel('Time')  # 공유 x 축을 가진 두 번째 서브플롯만 x 축 레이블을 표시
axes[0].set_ylabel('Gold')
axes[1].set_ylabel('Gold')

fig.suptitle('Gold Over Time')  # 전체 제목

axes[0].legend()
axes[0].grid(True)
axes[1].legend()
axes[1].grid(True)

plt.show()
