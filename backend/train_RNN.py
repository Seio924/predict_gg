import os
import tensorflow as tf
import numpy as np
from load_data import LoadData
from models import GeneralRNN

if __name__ == "__main__":
    api_key = 'RGAPI-1120a582-1b6f-4fc6-b1c3-9de51edfabbb'
    load_instance = LoadData(api_key)

    train_data, win_lose_list = load_instance.get_diamond1_data_list(5000)
    d = len(train_data[0])
    print(d)

    LIST_LEN = 88

    # 시계열 데이터의 최대 길이 계산
    max_length_data = 301

    # 패딩을 적용한 배열 생성
    padded_data = np.zeros((len(train_data), max_length_data, LIST_LEN))
    for i, seq in enumerate(train_data):
        padded_data[i, :len(seq), :] = seq

    win_lose_list = np.array(win_lose_list, dtype="float32")

    # Instantiate the GeneralRNN model
    model_parameters = {
        'task': 'regression',
        'model_type': 'rnn',  # or 'rnn', 'lstm'
        'h_dim': 64,  # Hidden dimension
        'n_layer': 2,  # Number of layers
        'batch_size': 32,  # Batch size
        'epoch': 10,  # Number of epochs
        'learning_rate': 0.001  # Learning rate
    }
    rnn_model = GeneralRNN(model_parameters)

    # Train the model
    trained_model = rnn_model.fit(padded_data, win_lose_list)
