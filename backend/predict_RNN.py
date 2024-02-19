from load_data import LoadData
from models import GeneralRNN
import numpy as np
from utils import PreprocessData
import tensorflow as tf



api_key = 'RGAPI-edea93ad-3df3-481e-802a-8803b447dfb9'

test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

# 데이터 가져오기
train_data = test.get_condition_timeline(10000)
playtime = len(train_data)

train_data = np.array(train_data)
print(train_data)

LIST_LEN = 87

# 시계열 데이터의 최대 길이 계산
max_length_data = 301

# Instantiate the GeneralRNN model
model_parameters = {
    'task': 'regression',
    'model_type': 'rnn',  # or 'rnn', 'lstm'
    'h_dim': 64,  # Hidden dimension
    'n_layer': 2,  # Number of layers
    'batch_size': 32,  # Batch size
    'epoch': 10,  # Number of epochs
    'learning_rate': 0.001,  # Learning rate
    'filename': 'time_10',  # Learning rate
    'use_filename': 'time_10'  # Learning rate
}
rnn_model = GeneralRNN(model_parameters)

winning_rate = []

for i in range(1, playtime):

    predict_data = train_data[:i].copy()

    # 패딩을 적용한 배열 생성
    padded_predict_data = np.zeros((max_length_data, LIST_LEN))
    for i, seq in enumerate(predict_data):
        padded_predict_data[i, :] = seq[:, :LIST_LEN]


    # Now you can use the trained model to predict
    predictions = rnn_model.predict(padded_predict_data)

    winning_rate.append(predictions)
    print(predictions)
