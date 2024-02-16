import tensorboard as tf
import numpy as np
from load_data import LoadData

Pmodel = tf.keras.load_model('backend/model')


LIST_LEN = 88

api_key = 'RGAPI-673aae6c-9f30-49f5-bef9-4b0e4a0cc72e'


load_instance = LoadData(api_key)

# 데이터 가져오기
get_train_data, get_win_lose_list = load_instance.get_diamond1_data_list(1)

train_data = []
win_lose_list = []

for one_game_data in get_train_data:
    for one_list in one_game_data:
        train_data.append(one_list)



predict_data = Pmodel.predict(train_data[:100])
print(predict_data)