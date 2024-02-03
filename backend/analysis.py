import matplotlib.pyplot as plt
import numpy as np
import time as t
from utils import PreprocessData

TIMESTAMP = 0

TEAM1_TOP_CHAMPION = 1
TEAM1_TOP_GOLD = 2
TEAM1_TOP_POTION = 3
TEAM1_TOP_K = 4
TEAM1_TOP_D = 5
TEAM1_TOP_A = 6

TEAM1_JUNGLE_CHAMPION = 7
TEAM1_JUNGLE_GOLD = 8
TEAM1_JUNGLE_POTION = 9
TEAM1_JUNGLE_K = 10
TEAM1_JUNGLE_D = 11
TEAM1_JUNGLE_A = 12

TEAM1_MIDDLE_CHAMPION = 13
TEAM1_MIDDLE_GOLD = 14
TEAM1_MIDDLE_POTION = 15
TEAM1_MIDDLE_K = 16
TEAM1_MIDDLE_D = 17
TEAM1_MIDDLE_A = 18

TEAM1_BOTTOM_CHAMPION = 19
TEAM1_BOTTOM_GOLD = 20
TEAM1_BOTTOM_POTION = 21
TEAM1_BOTTOM_K = 22
TEAM1_BOTTOM_D = 23
TEAM1_BOTTOM_A = 24

TEAM1_UTILITY_CHAMPION = 25
TEAM1_UTILITY_GOLD = 26
TEAM1_UTILITY_POTION = 27
TEAM1_UTILITY_K = 28
TEAM1_UTILITY_D = 29
TEAM1_UTILITY_A = 30

TEAM1_GOLD = 31

START_ITEM = 32
TIER1_ITEM = 33
TIER2_ITEM = 34
TIER3_ITEM = 35
BOOTS_ITEM = 36
SPECIAL_ITEM = 37
WARD_ITEM = 38

WARD_COUNT = 39
OBJECT_COUNT = 40

TOWER_TOP_COUNT = 41
TOWER_MIDDLE_COUNT = 42
TOWER_BOTTOM_COUNT = 43

TEAM_INTERVAL = 43

LIST_LEN = 88

class AnalysisData:
    def __init__(self):
        self.fig, self.axes = plt.subplots(4, 2, sharex=True, sharey=True)
        self.win_std = []
        self.lose_std = []
        self.min_length = float('inf')
        self.time = [i for i in range(0, 10000000, 10000)]

    def analyze_data(self):
        test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

        interval_list = test.get_condition_timeline(10000)

        team, win_lose, line, champion, aram = test.get_match_data()

        team1_gold = []
        team2_gold = []

        if aram == 1:
            t.sleep(5)
        else:
            interval_list = np.array(interval_list, dtype=int)

            for i in interval_list:
                t1 = []
                t2 = []
                for j in [TEAM1_TOP_GOLD, TEAM1_JUNGLE_GOLD, TEAM1_MIDDLE_GOLD, TEAM1_BOTTOM_GOLD, TEAM1_UTILITY_GOLD]:
                    t1.append(i[j])
                    t2.append(i[j+TEAM_INTERVAL])
                team1_gold.append(t1)
                team2_gold.append(t2)

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
        # 91 : 15분, 121 : 20분, 181 : 30분, 241 : 40분

        win_std_15 = []
        win_std_20 = []
        win_std_30 = []
        win_std_40 = []
        lose_std_15 = []
        lose_std_20 = []
        lose_std_30 = []
        lose_std_40 = []

        for i in self.win_std:
            if len(i) < 91:
                continue
            elif len(i) < 121: #20분
                win_std_15.append(i)
            elif len(i) < 181: #30분
                win_std_20.append(i)
            elif len(i) < 241: #40분
                win_std_30.append(i)
            else:
                win_std_40.append(i)

        for i in self.lose_std:
            if len(i) < 91:
                continue
            elif len(i) < 121: #20분
                lose_std_15.append(i)
            elif len(i) < 181: #30분
                lose_std_20.append(i)
            elif len(i) < 241: #40분
                lose_std_30.append(i)
            else:
                lose_std_40.append(i)
            

        # 15분
        if len(win_std_15) > 0:
            win_std_15_mean = [sum(row[i] for row in win_std_15) / len(win_std_15) for i in range(91)]
            self.axes[0, 0].plot(self.time[:91], win_std_15_mean, label='15 Win Mean std_dev')


        if len(lose_std_15) > 0:
            lose_std_15_mean = [sum(row[i] for row in lose_std_15) / len(lose_std_15) for i in range(91)]
            self.axes[0, 1].plot(self.time[:91], lose_std_15_mean, label='15 Lose Mean std_dev')


        # 20분
        if len(win_std_20) > 0:
            win_std_20_mean = [sum(row[i] for row in win_std_20) / len(win_std_20) for i in range(121)]
            self.axes[1, 0].plot(self.time[:121], win_std_20_mean, label='20 Win Mean std_dev')


        if len(lose_std_20) > 0:
            lose_std_20_mean = [sum(row[i] for row in lose_std_20) / len(lose_std_20) for i in range(121)]
            self.axes[1, 1].plot(self.time[:121], lose_std_20_mean, label='20 Lose Mean std_dev')


        # 30분
        if len(win_std_30) > 0:
            win_std_30_mean = [sum(row[i] for row in win_std_30) / len(win_std_30) for i in range(181)]
            self.axes[2, 0].plot(self.time[:181], win_std_30_mean, label='30 Win Mean std_dev')


        if len(lose_std_30) > 0:
            lose_std_30_mean = [sum(row[i] for row in lose_std_30) / len(lose_std_30) for i in range(181)]
            self.axes[2, 1].plot(self.time[:181], lose_std_30_mean, label='30 Lose Mean std_dev')


        # 40분
        if len(win_std_40) > 0:
            win_std_40_mean = [sum(row[i] for row in win_std_40) / len(win_std_40) for i in range(241)]
            self.axes[3, 0].plot(self.time[:241], win_std_40_mean, label='40 Win Mean std_dev')


        if len(lose_std_40) > 0:
            lose_std_40_mean = [sum(row[i] for row in lose_std_40) / len(lose_std_40) for i in range(241)]
            self.axes[3, 1].plot(self.time[:241], lose_std_40_mean, label='40 Lose Mean std_dev')


        self.axes[0, 0].set_xlabel('Time') 
        self.axes[0, 0].set_ylabel('Gold')
        self.axes[0, 1].set_xlabel('Time')
        self.axes[0, 1].set_ylabel('Gold')
        self.axes[1, 0].set_xlabel('Time')
        self.axes[1, 0].set_ylabel('Gold')
        self.axes[1, 1].set_xlabel('Time')
        self.axes[1, 1].set_ylabel('Gold')
        self.axes[2, 0].set_xlabel('Time')
        self.axes[2, 0].set_ylabel('Gold')
        self.axes[2, 1].set_xlabel('Time')
        self.axes[2, 1].set_ylabel('Gold')
        self.axes[3, 0].set_xlabel('Time')
        self.axes[3, 0].set_ylabel('Gold')
        self.axes[3, 1].set_xlabel('Time')
        self.axes[3, 1].set_ylabel('Gold')

        self.fig.suptitle('Win   Lose')

        self.axes[0, 0].legend()
        self.axes[0, 0].grid(True)
        self.axes[0, 1].legend()
        self.axes[0, 1].grid(True)
        self.axes[1, 0].legend()
        self.axes[1, 0].grid(True)
        self.axes[1, 1].legend()
        self.axes[1, 1].grid(True)
        self.axes[2, 0].legend()
        self.axes[2, 0].grid(True)
        self.axes[2, 1].legend()
        self.axes[2, 1].grid(True)
        self.axes[3, 0].legend()
        self.axes[3, 0].grid(True)
        self.axes[3, 1].legend()
        self.axes[3, 1].grid(True)

        plt.show()
