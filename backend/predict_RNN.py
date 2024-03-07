from load_data import LoadData
from models import GeneralRNN
import numpy as np
from utils import PreprocessData
import tensorflow as tf
from utils_2 import binary_cross_entropy_loss, mse_loss, rnn_sequential
import matplotlib.pyplot as plt

api_key = 'RGAPI-80ba1ae9-cccc-4e83-a491-b5db20a7614b'

test = PreprocessData('./api_data/api_match_info.json', './api_data/api_timeline_info.json')

# 데이터 가져오기
train_data = test.get_condition_timeline(10000)
playtime = len(train_data)
train_data = np.array(train_data)
print(train_data)

LIST_LEN = 177

# 시계열 데이터의 최대 길이 계산
max_length_data = 301

winning_rate = []

with tf.keras.utils.custom_object_scope({'binary_cross_entropy_loss': binary_cross_entropy_loss}):
    loaded_model = tf.keras.models.load_model('C:/GitHub/predict_gg/backend/model_trained_RNN')

for i in range(1, playtime):

    predict_data = train_data[:i].copy()

    # 패딩을 적용한 배열 생성
    padded_predict_data = np.zeros((max_length_data, LIST_LEN))
    for i, seq in enumerate(predict_data):
        padded_predict_data[i, :] = seq


    pred_x = np.expand_dims(padded_predict_data, axis=0)
    predictions = loaded_model.predict(pred_x)


    winning_rate.append([predictions[0][0], predictions[0][1]])

print(winning_rate)


# 그래프 그리기
x_values = range(0, len(winning_rate) * 10, 10)
team1_winning_rates = [item[0] for item in winning_rate]
team2_winning_rates = [item[1] for item in winning_rate]

plt.plot(x_values, team1_winning_rates, label='Team 1 Winning Rate')
plt.plot(x_values, team2_winning_rates, label='Team 2 Winning Rate')
plt.xlabel('Time (seconds)')
plt.ylabel('Winning Rate')
plt.title('Winning Rate Over Time')
plt.legend()
plt.show()