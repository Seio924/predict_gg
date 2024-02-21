import tensorflow as tf
import numpy as np
from load_data import LoadData
from model_attention import Attention
import matplotlib.pyplot as plt

if __name__ == "__main__":
    api_key = 'RGAPI-80ba1ae9-cccc-4e83-a491-b5db20a7614b'
    load_instance = LoadData(api_key)

    train_data, win_lose_list = load_instance.get_summoner_data_list(5)
    d = len(train_data[0])
    print(d)

    LIST_LEN = 87

    # 시계열 데이터의 최대 길이 계산
    max_length_data = 301

    # 패딩을 적용한 배열 생성
    padded_data = np.zeros((len(train_data), max_length_data, LIST_LEN))
    for i, seq in enumerate(train_data):
        padded_data[i, :len(seq), :] = seq

    win_lose_list = np.array(win_lose_list, dtype="float32")

    model_parameters = {
    'task': 'regression',  # 또는 'classification'
    'h_dim': 128,
    'batch_size': 64,
    'epoch': 10,
    'learning_rate': 0.001,
    'save_file_directory': 'C:/GitHub/predict_gg/backend/model_trained_ATTENTION'

    }

    attention_model = Attention(model_parameters)

    attention_model.fit(padded_data, win_lose_list)
