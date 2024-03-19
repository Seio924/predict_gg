import numpy as np


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


file_num_list = [508, 510, 521, 496, 508, 510, 521, 496, 503, 521, 370, 485, 503, 521, 370, 485, 481, 524, 498, 490, 481, 524, 498, 490]
LIST_LEN = 177

# 시계열 데이터의 최대 길이 계산
max_length_data = 500

for file_num1, file_num2 in enumerate(file_num_list):
    for repeat_num in range(file_num2):
        train_data = []

        train_data += read_interval_file("api_data/data_split/interval_split_" + str(file_num1+1) + "_" + str(repeat_num+1) + ".txt")
        output_file = f"api_data/data_normalized_split/interval_split_" + str(file_num1+1) + "_" + str(repeat_num+1) + ".txt" 
        
        with open(output_file, 'w') as f:
            for seq in train_data:
                tmp = np.array(seq)[:,:]

                for j in range(1, LIST_LEN):
                    seq_data = np.array(seq)[:, j]
                    seq_data_mean = seq_data.mean()
                    seq_data_std = seq_data.std()

                    if seq_data_std == 0:
                        seq_data_std = 1
                    
                    normalized_seq_data = (seq_data - seq_data_mean) / seq_data_std
                    tmp[:, j] = normalized_seq_data
                
                
                f.writelines(tmp)
            
        