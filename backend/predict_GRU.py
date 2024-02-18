import tensorflow as tf
from load_data import LoadData
import numpy as np

from train_GRU import CustomGRU  # RNN 클래스 대신 CustomGRU 클래스 가져오기

# 사용자 정의 클래스를 포함하여 모델 로드
Pmodel = tf.keras.models.load_model('backend/modelGRU', custom_objects={'CustomGRU': CustomGRU})


LIST_LEN = 88
api_key = 'RGAPI-a67d1c19-7c88-407a-92af-21b2e5945829'
load_instance = LoadData(api_key)

# 데이터 가져오기
get_train_data, get_win_lose_list = load_instance.get_diamond1_data_list(1)

train_data = []
win_lose_list = []

max_length_data = 301

 # 패딩을 적용한 배열 생성
padded_predict_data = np.zeros((len(get_train_data), max_length_data, LIST_LEN), dtype=int)
for i, seq in enumerate(train_data):
    padded_predict_data[i, :len(seq), :] = seq

mean_values = np.mean(padded_predict_data[:, :, 1:], axis=(0, 1))  # 타임스탬프를 제외한 특성의 평균
std_values = np.std(padded_predict_data[:, :, 1:], axis=(0, 1))    # 타임스탬프를 제외한 특성의 표준편차

normalized_predict_data = padded_predict_data.copy()
normalized_predict_data[:, :, 1:] = (padded_predict_data[:, :, 1:] - mean_values) / std_values


# 예측 수행
predict_data = Pmodel.predict(normalized_predict_data)
print(predict_data)
