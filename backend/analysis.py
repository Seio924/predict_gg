import matplotlib.pyplot as plt
import numpy as np
import time as t
from utils import PreprocessData

TIMESTAMP = 0

TEAM1_TOP_CHAMPION = 1
TEAM1_TOP_GOLD = 2
TEAM1_TOP_ITEM_GOLD = 3
TEAM1_TOP_K = 4
TEAM1_TOP_D = 5
TEAM1_TOP_A = 6
TEAM1_TOP_STATPERK_DEFENCE = 7
TEAM1_TOP_STATPERK_FLEX = 8
TEAM1_TOP_STATPERK_OFFENSE = 9
TEAM1_TOP_PRIMARY1 = 10
TEAM1_TOP_PRIMARY2 = 11
TEAM1_TOP_PRIMARY3 = 12
TEAM1_TOP_PRIMARY4 = 13
TEAM1_TOP_SUBSTYLE1 = 14
TEAM1_TOP_SUBSTYLE2 = 15
TEAM1_TOP_WARD = 16

TEAM1_JUNGLE_CHAMPION = 17
TEAM1_JUNGLE_GOLD = 18
TEAM1_JUNGLE_ITEM_GOLD = 19
TEAM1_JUNGLE_K = 20
TEAM1_JUNGLE_D = 21
TEAM1_JUNGLE_A = 22
TEAM1_JUNGLE_STATPERK_DEFENCE = 23
TEAM1_JUNGLE_STATPERK_FLEX = 24
TEAM1_JUNGLE_STATPERK_OFFENSE = 25
TEAM1_JUNGLE_PRIMARY1 = 26
TEAM1_JUNGLE_PRIMARY2 = 27
TEAM1_JUNGLE_PRIMARY3 = 28
TEAM1_JUNGLE_PRIMARY4 = 29
TEAM1_JUNGLE_SUBSTYLE1 = 30
TEAM1_JUNGLE_SUBSTYLE2 = 31
TEAM1_JUNGLE_WARD = 32

TEAM1_MIDDLE_CHAMPION = 33
TEAM1_MIDDLE_GOLD = 34
TEAM1_MIDDLE_ITEM_GOLD = 35
TEAM1_MIDDLE_K = 36
TEAM1_MIDDLE_D = 37
TEAM1_MIDDLE_A = 38
TEAM1_MIDDLE_STATPERK_DEFENCE = 39
TEAM1_MIDDLE_STATPERK_FLEX = 40
TEAM1_MIDDLE_STATPERK_OFFENSE = 41
TEAM1_MIDDLE_PRIMARY1 = 42
TEAM1_MIDDLE_PRIMARY2 = 43
TEAM1_MIDDLE_PRIMARY3 = 44
TEAM1_MIDDLE_PRIMARY4 = 45
TEAM1_MIDDLE_SUBSTYLE1 = 46
TEAM1_MIDDLE_SUBSTYLE2 = 47
TEAM1_MIDDLE_WARD = 48

TEAM1_BOTTOM_CHAMPION = 49
TEAM1_BOTTOM_GOLD = 50
TEAM1_BOTTOM_ITEM_GOLD = 51
TEAM1_BOTTOM_K = 52
TEAM1_BOTTOM_D = 53
TEAM1_BOTTOM_A = 54
TEAM1_BOTTOM_STATPERK_DEFENCE = 55
TEAM1_BOTTOM_STATPERK_FLEX = 56
TEAM1_BOTTOM_STATPERK_OFFENSE = 57
TEAM1_BOTTOM_PRIMARY1 = 58
TEAM1_BOTTOM_PRIMARY2 = 59
TEAM1_BOTTOM_PRIMARY3 = 60
TEAM1_BOTTOM_PRIMARY4 = 61
TEAM1_BOTTOM_SUBSTYLE1 = 62
TEAM1_BOTTOM_SUBSTYLE2 = 63
TEAM1_BOTTOM_WARD = 64

TEAM1_UTILITY_CHAMPION = 65
TEAM1_UTILITY_GOLD = 66
TEAM1_UTILITY_ITEM_GOLD = 67
TEAM1_UTILITY_K = 68
TEAM1_UTILITY_D = 69
TEAM1_UTILITY_A = 70
TEAM1_UTILITY_STATPERK_DEFENCE = 71
TEAM1_UTILITY_STATPERK_FLEX = 72
TEAM1_UTILITY_STATPERK_OFFENSE = 73
TEAM1_UTILITY_PRIMARY1 = 74
TEAM1_UTILITY_PRIMARY2 = 75
TEAM1_UTILITY_PRIMARY3 = 76
TEAM1_UTILITY_PRIMARY4 = 77
TEAM1_UTILITY_SUBSTYLE1 = 78
TEAM1_UTILITY_SUBSTYLE2 = 79
TEAM1_UTILITY_WARD = 80

TEAM1_GOLD = 81

HORDE_COUNT = 82
DRAGON_COUNT = 83
RIFTHERALD_COUNT = 84
BARON_NASHOR_COUNT = 85

TOWER_TOP_COUNT = 86
TOWER_MIDDLE_COUNT = 87
TOWER_BOTTOM_COUNT = 88

TEAM_INTERVAL = 88

LIST_LEN = 178

class AnalysisData:
    def __init__(self):
        self.fig, self.axes = plt.subplots(1, 2, sharex=True, sharey=True)
        self.win_std = []
        self.lose_std = []
        self.min_length = float('inf')
        self.time = [i for i in range(0, 10000000, 10000)]

    def analyze_data(self):
        test = PreprocessData('./api_data/api_match_info.json', './api_data/api_timeline_info.json')

        interval_list = test.get_condition_timeline(10000)
        if interval_list == 0:
            pass
        else:
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
        if len(win_std_20) > 0:
            win_std_15_mean = [sum(row[i] for row in win_std_15) / len(win_std_15) for i in range(91)]
            self.axes[0].plot(self.time[:91], win_std_15_mean, label='15 Win Mean std_dev')
            self.axes[0].set_xlabel('Time') 
            self.axes[0].set_ylabel('Gold')
            self.axes[0].legend()
            self.axes[0].grid(True)


        if len(lose_std_20) > 0:
            lose_std_15_mean = [sum(row[i] for row in lose_std_15) / len(lose_std_15) for i in range(91)]
            self.axes[1].plot(self.time[:91], lose_std_15_mean, label='15 Lose Mean std_dev')
            self.axes[1].set_xlabel('Time')
            self.axes[1].set_ylabel('Gold')
            self.axes[1].legend()
            self.axes[1].grid(True)


        """ # 20분
        if len(win_std_20) > 0:
            win_std_20_mean = [sum(row[i] for row in win_std_20) / len(win_std_20) for i in range(121)]
            self.axes[0].plot(self.time[:121], win_std_20_mean, label='20 Win Mean std_dev')
            self.axes[0].set_xlabel('Time')
            self.axes[0].set_ylabel('Gold')
            self.axes[0].legend()
            self.axes[0].grid(True)


        if len(lose_std_20) > 0:
            lose_std_20_mean = [sum(row[i] for row in lose_std_20) / len(lose_std_20) for i in range(121)]
            self.axes[1].plot(self.time[:121], lose_std_20_mean, label='20 Lose Mean std_dev')
            self.axes[1].set_xlabel('Time')
            self.axes[1].set_ylabel('Gold')
            self.axes[1].legend()
            self.axes[1].grid(True) """


        """ # 30분
        if len(win_std_30) > 0:
            win_std_30_mean = [sum(row[i] for row in win_std_30) / len(win_std_30) for i in range(181)]
            self.axes[0].plot(self.time[:181], win_std_30_mean, label='30 Win Mean std_dev')
            self.axes[0].set_xlabel('Time')
            self.axes[0].set_ylabel('Gold')
            self.axes[0].legend()
            self.axes[0].grid(True)

        if len(lose_std_30) > 0:
            lose_std_30_mean = [sum(row[i] for row in lose_std_30) / len(lose_std_30) for i in range(181)]
            self.axes[1].plot(self.time[:181], lose_std_30_mean, label='30 Lose Mean std_dev')
            self.axes[1].set_xlabel('Time')
            self.axes[1].set_ylabel('Gold')
            self.axes[1].legend()
            self.axes[1].grid(True) """

        """ # 40분
        if len(win_std_40) > 0:
            win_std_40_mean = [sum(row[i] for row in win_std_40) / len(win_std_40) for i in range(241)]
            self.axes[0].plot(self.time[:241], win_std_40_mean, label='40 Win Mean std_dev')
            self.axes[0].set_xlabel('Time')
            self.axes[0].set_ylabel('Gold')
            self.axes[0].legend()
            self.axes[0].grid(True)

        if len(lose_std_40) > 0:
            lose_std_40_mean = [sum(row[i] for row in lose_std_40) / len(lose_std_40) for i in range(241)]
            self.axes[1].plot(self.time[:241], lose_std_40_mean, label='40 Lose Mean std_dev')
            self.axes[1].set_xlabel('Time')
            self.axes[1].set_ylabel('Gold')
            self.axes[1].legend()
            self.axes[1].grid(True) """
        

        self.fig.suptitle('Win   Lose')

        plt.show()
