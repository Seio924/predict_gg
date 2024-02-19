from load_data import LoadData
from models import GeneralRNN
import numpy as np
from utils import PreprocessData
import tensorflow as tf



api_key = 'RGAPI-f2bf170c-5745-42a5-a8f7-a591e780d2fa'

test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

# 데이터 가져오기
train_data = test.get_condition_timeline(10000)
train_data = np.array(train_data)
print(train_data)
d = len(train_data[0])
print(d)

LIST_LEN = 88

# 시계열 데이터의 최대 길이 계산
max_length_data = 301

# Instantiate the GeneralRNN model
model_parameters = {
    'task': 'regression',
    'model_type': 'gru',  # or 'rnn', 'lstm'
    'h_dim': 64,  # Hidden dimension
    'n_layer': 2,  # Number of layers
    'batch_size': 32,  # Batch size
    'epoch': 10,  # Number of epochs
    'learning_rate': 0.001  # Learning rate
}
rnn_model = GeneralRNN(model_parameters)


predict_data = train_data[:1].copy()
print(predict_data.shape)

# 패딩을 적용한 배열 생성
padded_predict_data = np.zeros((max_length_data, LIST_LEN))
for i, seq in enumerate(predict_data):
    padded_predict_data[i, :] = seq

print(padded_predict_data.shape)
print(padded_predict_data)

# Now you can use the trained model to predict
predictions = rnn_model.predict(padded_predict_data)

print(predictions)

predict_data = train_data[:30].copy()


padded_predict_data = np.zeros((max_length_data, LIST_LEN))
for i, seq in enumerate(predict_data):
    padded_predict_data[i, :] = seq

predictions = rnn_model.predict(padded_predict_data)

print(predictions)

predict_data = train_data[:60].copy()


padded_predict_data = np.zeros((max_length_data, LIST_LEN))
for i, seq in enumerate(predict_data):
    padded_predict_data[i, :] = seq

predictions = rnn_model.predict(padded_predict_data)

print(predictions)

predict_data = train_data[:91].copy()


padded_predict_data = np.zeros((max_length_data, LIST_LEN))
for i, seq in enumerate(predict_data):
    padded_predict_data[i, :] = seq

predictions = rnn_model.predict(padded_predict_data)

print(predictions)

predict_data = train_data[:121].copy()


padded_predict_data = np.zeros((max_length_data, LIST_LEN))
for i, seq in enumerate(predict_data):
    padded_predict_data[i, :] = seq

predictions = rnn_model.predict(padded_predict_data)

print(predictions)