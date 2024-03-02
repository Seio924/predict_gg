from load_data import LoadData
from models import GeneralRNN
import numpy as np
from utils import PreprocessData
import tensorflow as tf
from utils_2 import binary_cross_entropy_loss, mse_loss, rnn_sequential
import matplotlib.pyplot as plt


api_key = 'RGAPI-0a3a44de-d1aa-4789-b49a-96db4790807c'

with open('backend/userInput.txt', 'r', encoding="utf-8") as f:
    time_num = f.read().strip()

time_num = int(time_num)

test = PreprocessData('./api_data/api_match_info.json', './api_data/api_timeline_info.json')

# 데이터 가져오기
train_data = test.get_condition_timeline(time_num*1000)
playtime = len(train_data)
train_data = np.array(train_data)
print(train_data)

LIST_LEN = 169

# 시계열 데이터의 최대 길이 계산
max_length_data = 301

winning_rate = []
winning_rate2 = []


with tf.keras.utils.custom_object_scope({'binary_cross_entropy_loss': binary_cross_entropy_loss}):
    loaded_model = tf.keras.models.load_model('C:/GitHub/predict_gg/backend/model_trained_GRU')

for i in range(playtime):

    predict_data = train_data[:i+1].copy()

    # 패딩을 적용한 배열 생성
    padded_predict_data = np.zeros((max_length_data, LIST_LEN))
    for h, seq in enumerate(predict_data):
        padded_predict_data[h, :] = seq


    pred_x = np.expand_dims(padded_predict_data, axis=0)
    predictions = loaded_model.predict(pred_x)

    winning_rate2.append([predictions[0][0], predictions[0][1]])
    winning_rate.append([(i*time_num), round(predictions[0][0]*100), round(predictions[0][1]*100)])

#print(winning_rate)



with open("src/predict_data.txt", "w") as file:
    for rate in winning_rate:
        file.write(f"{rate}\n")


# 그래프 그리기
x_values = range(0, len(winning_rate2) * 10, 10)
team1_winning_rates = [item[0] for item in winning_rate2]
team2_winning_rates = [item[1] for item in winning_rate2]

plt.plot(x_values, team1_winning_rates, label='Team 1 Winning Rate')
#plt.plot(x_values, team2_winning_rates, label='Team 2 Winning Rate')
plt.xlabel('Time (seconds)')
plt.ylabel('Winning Rate')
plt.title('Winning Rate Over Time')
plt.legend()
plt.show()