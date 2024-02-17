import tensorflow as tf
import numpy as np
from load_data import LoadData
from transformer_model import MultiHeadAttention

LIST_LEN = 88

api_key = 'RGAPI-a67d1c19-7c88-407a-92af-21b2e5945829'


load_instance = LoadData(api_key)

# 데이터 가져오기
get_train_data, get_win_lose_list = load_instance.get_diamond1_data_list(3000)

train_data = []
win_lose_list = []

for one_game_data in get_train_data:
    for one_list in one_game_data:
        train_data.append(one_list)

for one_game_data in get_win_lose_list:
    for one_list in one_game_data:
        win_lose_list.append(one_list[0])

train_data = np.array(train_data)
win_lose_list = np.array(win_lose_list)

model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(100, input_shape=(1, LIST_LEN)),
    tf.keras.layers.Dense(2, activation='softmax'),
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_data, win_lose_list, batch_size=64, epochs=30, verbose=2)

model.save('backend/modelLSTM')