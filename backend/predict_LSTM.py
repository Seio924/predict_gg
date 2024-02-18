import tensorflow as tf

import numpy as np
from load_data import LoadData

Pmodel = tf.keras.models.load_model('backend/modelLSTM')


LIST_LEN = 87

api_key = 'RGAPI-a67d1c19-7c88-407a-92af-21b2e5945829'


load_instance = LoadData(api_key)

# 데이터 가져오기
get_train_data, get_win_lose_list = load_instance.get_diamond1_data_list(1)

train_data = []
win_lose_list = []

for one_game_data in get_train_data:
    for one_list in one_game_data:
        train_data.append(one_list[:-1])

train_data = np.array(train_data)

train_data = train_data.reshape(train_data.shape[0], 1, train_data.shape[1])
print(train_data)

first_input = tf.expand_dims(train_data[148], axis=0)
predict_data = Pmodel.predict(first_input)
print(predict_data)