import numpy as np
import tensorflow as tf


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


LIST_LEN = 177
max_length_data = 500

file_count = 3742
checkpoint = [159, 319, 484, 640, 799, 959, 1124, 1280, 1441, 1606, 1724, 1880, 2041, 2206, 2324, 2480, 2633, 2799, 2956, 3111, 3264, 3430, 3587, 3742]

for repeat_num in range(1724, file_count):
    train_data = []
    print(repeat_num)
    
    if repeat_num in checkpoint or repeat_num % 50 == 0:
        print("입력")
        a = input()

    print("다시 시작")
    train_data += read_interval_file("api_data/data_normalized_split/interval_split_" + str(repeat_num) + ".txt")
    output_file = f"api_data/data_normalized_split_tmp/interval_split_" + str(repeat_num) + ".txt" 
    
    with open(output_file, 'w') as f:
        for seq in train_data:
            tmp = np.array(seq, dtype=float)[:,:]
            normalized_seq_data = tf.keras.utils.normalize(np.array(seq)[:,1:].astype(float), axis=1)
            tmp[:, 1:] = normalized_seq_data.copy()

            tmp = tmp.tolist()
            f.write(str(tmp)+"\n")
    
    