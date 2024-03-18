import os
import tensorflow as tf
import numpy as np
from models import GeneralRNN
import matplotlib.pyplot as plt

def read_interval_file(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            data = [int(num) for num in line.strip('[]\n').replace('[', ' ').replace(']', '').split(',')]
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

    # Instantiate the GeneralRNN model
    model_parameters = {
        'task': 'regression',
        'model_type': 'gru',  # or 'rnn', 'lstm'
        'h_dim': 20,  # Hidden dimension
        'n_layer': 2,  # Number of layers
        'batch_size': 32,  # Batch size
        'epoch': 30,  # Number of epochs
        'learning_rate': 0.001  # Learning rate
    }
    rnn_model = GeneralRNN(model_parameters)

    file_num_list = [204, 204, 209, 199, 204, 204, 209, 199, 202, 209, 148, 194, 202, 209, 148, 194, 193, 210, 200, 196, 193, 210, 200, 196]
    
    n = 1

    for file_num1, file_num2 in enumerate(file_num_list):
        for repeat_num in range(file_num2):
            train_data = []
            win_lose_list = []

            train_data += read_interval_file("api_data/data_split/interval_split_" + str(file_num1+1) + "_" + str(repeat_num+1) + ".txt")
            win_lose_list += read_win_lose_file("api_data/data_split/win_lose_split_" + str(file_num1+1) + "_" + str(repeat_num+1) + ".txt")

            LIST_LEN = 177

            # 시계열 데이터의 최대 길이 계산
            max_length_data = 500

            for game_num, d in enumerate(train_data):
                for n in range(1,len(d)):
                    train_data.append(d[:n])
                    win_lose_list.append(win_lose_list[game_num])

            # 패딩을 적용한 배열 생성
            padded_data = np.zeros((len(train_data), max_length_data, LIST_LEN))
            for i, seq in enumerate(train_data):
                padded_data[i, :len(seq), :] = np.array(seq)[:,:]
                

                for j in range(1, LIST_LEN):
                    seq_data = np.array(seq)[:, j]
                    seq_data_mean = seq_data.mean()
                    seq_data_std = seq_data.std()

                    if seq_data_std == 0:
                        seq_data_std = 1
                    
                    normalized_seq_data = (seq_data - seq_data_mean) / seq_data_std
                    padded_data[i, :len(seq), j] = normalized_seq_data
            
            # for i, seq in enumerate(train_data):
            #     padded_data[i, :len(seq), :] = seq

            win_lose_list = np.array(win_lose_list, dtype="float32")

            print(padded_data[0])


            trained_model = rnn_model.fit(padded_data, win_lose_list)
            
            print(str(n) + "번째 학습 완료")
            n += 1
    
    
    trained_model.save('C:/GitHub/predict_gg/backend/modelGRU20')

    # # Plot loss
    # plt.plot(trained_model.history['mse'], label='Training mse')
    # plt.plot(trained_model.history['val_mse'], label='Validation mse')
    # plt.title('Model Loss')
    # plt.xlabel('Epoch')
    # plt.ylabel('Loss')
    # plt.show()

    # # Plot accuracy
    # plt.plot(trained_model.history['accuracy'], label='Training Accuracy')
    # plt.plot(trained_model.history['val_accuracy'], label='Validation Accuracy')
    # plt.title('Model Accuracy')
    # plt.xlabel('Epoch')
    # plt.ylabel('Accuracy')
    # plt.show()