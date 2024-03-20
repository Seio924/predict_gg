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

            
if __name__ == "__main__":
    interval_files = ['api_interval_list1-1', 'api_interval_list1-2', 'api_interval_list1-3', 'api_interval_list1-4', 'api_interval_list1-5', 'api_interval_list1-6', 'api_interval_list1-7', 'api_interval_list1-8',
                     'api_interval_list2-1', 'api_interval_list2-2', 'api_interval_list2-3', 'api_interval_list2-4', 'api_interval_list2-5', 'api_interval_list2-6', 'api_interval_list2-7', 'api_interval_list2-8',
                     'api_interval_list3-1', 'api_interval_list3-2', 'api_interval_list3-3', 'api_interval_list3-4', 'api_interval_list3-5', 'api_interval_list3-6', 'api_interval_list3-7', 'api_interval_list3-8']
    
    win_lose_files = ['api_win_lose_list1-1', 'api_win_lose_list1-2', 'api_win_lose_list1-3', 'api_win_lose_list1-4', 'api_win_lose_list1-5', 'api_win_lose_list1-6', 'api_win_lose_list1-7', 'api_win_lose_list1-8',
                     'api_win_lose_list2-1', 'api_win_lose_list2-2', 'api_win_lose_list2-3', 'api_win_lose_list2-4', 'api_win_lose_list2-5', 'api_win_lose_list2-6', 'api_win_lose_list2-7', 'api_win_lose_list2-8',
                     'api_win_lose_list3-1', 'api_win_lose_list3-2', 'api_win_lose_list3-3', 'api_win_lose_list3-4', 'api_win_lose_list3-5', 'api_win_lose_list3-6', 'api_win_lose_list3-7', 'api_win_lose_list3-8']
    
    line_num = 0
    file_num = 0
    
    for interval_file, win_lose_file in zip(interval_files, win_lose_files):
        train_data = []
        win_lose_list = []

        train_data += read_interval_file("api_data/data/" + interval_file + ".txt")
        win_lose_list += read_win_lose_file("api_data/data/" + win_lose_file + ".txt")

        for train_data1, win_lose_list1 in zip(train_data, win_lose_list):
            for d in range(len(train_data1)):
                line_num += 1
                if line_num % 2000 == 0:
                    file_num += 1
                    print(file_num)

                output_file1 = f"api_data/data_normalized_split/interval_split_"+ str(file_num) + ".txt" 
                output_file2 = f"api_data/data_normalized_split/win_lose_split_"+ str(file_num) + ".txt" 

                with open(output_file1, 'a') as f:
                    f.write(str(train_data1[:d+1]) + "\n")

                with open(output_file2, 'a') as f:
                    f.write(str(win_lose_list1) + "\n")
                
                
