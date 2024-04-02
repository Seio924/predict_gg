import tensorflow as tf
import numpy as np
from attention import Attention


def read_interval_file(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            data = [float(num) for num in line.strip('[]\n').replace('[', ' ').replace(']', '').split(',')]
            list_len = 177
            data_list = [data[i:i + list_len] for i in range(0, len(data), list_len)]
            result.append(data_list)
    return result

def read_win_lose_file(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            # 대괄호를 제거한 후, 각 줄을 숫자로 변환하여 리스트로 만듦
            data = [int(num) for num in line.strip().replace('[', '').replace(']', '').split(',')]
            result.append(data)
    return result

if __name__ == "__main__":

    model_parameters = {
    'task': 'regression',  # 또는 'classification'
    'h_dim': 12,
    'batch_size': 64,
    'epoch': 10,
    'learning_rate': 0.001,
    'save_file_directory': 'C:/GitHub/predict_gg/backend/model_trained_ATTENTION'

    }

    attention_model = Attention(model_parameters)


    n = 1

    for file_num in range():
        train_data = []
        win_lose_list = []

        train_data += read_interval_file("api_data/data/interval_split_"+str(file_num)+".txt")
        win_lose_list += read_win_lose_file("api_data/data/win_lose_split_"+str(file_num)+".txt")

        LIST_LEN = 177

        # 시계열 데이터의 최대 길이 계산
        max_length_data = 500

        # 패딩을 적용한 배열 생성
        padded_data = np.zeros((len(train_data), max_length_data, LIST_LEN))
        for i, seq in enumerate(train_data):
            padded_data[i, :len(seq), :] = np.array(seq)[:,:]
        
        # for i, seq in enumerate(train_data):
        #     padded_data[i, :len(seq), :] = seq

        win_lose_list = np.array(win_lose_list, dtype="float32")

        print(padded_data[0])

        attention_model.fit(padded_data, win_lose_list)

        
        print(str(n) + "번째 학습 완료")
        n += 1

    