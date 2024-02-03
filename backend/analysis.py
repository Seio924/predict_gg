import matplotlib.pyplot as plt
import numpy as np
import time as t
from utils import PreprocessData

TEAM1_TOP_GOLD = 1
TEAM1_TOP_POTION = 2
TEAM1_TOP_KDA = 3

TEAM1_JUNGLE_GOLD = 4
TEAM1_JUNGLE_POTION = 5
TEAM1_JUNGLE_KDA = 6

TEAM1_MIDDLE_GOLD = 7
TEAM1_MIDDLE_POTION = 8
TEAM1_MIDDLE_KDA = 9

TEAM1_BOTTOM_GOLD = 10
TEAM1_BOTTOM_POTION = 11
TEAM1_BOTTOM_KDA = 12

TEAM1_UTILITY_GOLD = 13
TEAM1_UTILITY_POTION = 14
TEAM1_UTILITY_KDA = 15

TEAM_INTERVAL = 26

class AnalysisData:
    def __init__(self):
        self.fig, self.axes = plt.subplots(1, 2, sharex=True, sharey=True)
        self.win_std = []
        self.lose_std = []
        self.min_length = float('inf')
        self.time = []

    def analyze_data(self):
        test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

        interval_list = test.get_condition_timeline(10000)

        team, win_lose, line, aram = test.get_match_data()

        team1_gold = []
        team2_gold = []

        if aram == 1:
            t.sleep(5)
        else:
            interval_list = np.array(interval_list, dtype=int)

            self.time = interval_list[:, 0]

            for j in [TEAM1_TOP_GOLD, TEAM1_JUNGLE_GOLD, TEAM1_MIDDLE_GOLD, TEAM1_BOTTOM_GOLD, TEAM1_UTILITY_GOLD]:
                team1_gold.append(interval_list[j])
                team2_gold.append(interval_list[j+TEAM_INTERVAL])

            team1_std_dev = np.std(team1_gold, axis=1)
            team2_std_dev = np.std(team2_gold, axis=1)

            self.min_length = min(self.min_length, len(team1_std_dev), len(team2_std_dev))

            if win_lose[0] == 1:
                self.win_std.append(team1_std_dev)
                self.lose_std.append(team2_std_dev)
            elif win_lose[1] == 1:
                self.win_std.append(team2_std_dev)
                self.lose_std.append(team1_std_dev)

            # print("분석 완료")

            # t.sleep(5)

    def plot_results(self):
        win_std_mean = [sum(row[i] for row in self.win_std) / len(self.win_std) for i in range(self.min_length)]
        lose_std_mean = [sum(row[i] for row in self.lose_std) / len(self.lose_std) for i in range(self.min_length)]

        self.axes[0].plot(self.time[:self.min_length], win_std_mean, label='Win Mean std_dev')
        self.axes[1].plot(self.time[:self.min_length], lose_std_mean, label='Lose Mean std_dev')

        self.axes[1].set_xlabel('Time')
        self.axes[0].set_ylabel('Gold')
        self.axes[1].set_ylabel('Gold')

        self.fig.suptitle('Win   Lose')

        self.axes[0].legend()
        self.axes[0].grid(True)
        self.axes[1].legend()
        self.axes[1].grid(True)

        plt.show()
