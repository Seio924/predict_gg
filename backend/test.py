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
    
    a = 1; b = 1
    
    for interval_file, win_lose_file in zip(interval_files, win_lose_files):
        train_data = []
        win_lose_list = []

        train_data_split = []
        win_lose_list_split = []

        train_data += read_interval_file("api_data/data/" + interval_file + ".txt")
        win_lose_list += read_win_lose_file("api_data/data/" + win_lose_file + ".txt")

        for train_data1 in train_data: # 한게임
            for d in range(len(train_data1)):
                train_data_split.append(train_data1[:d+1])

                if len(train_data_split) == 63:
                    with open("api_data/data_tmp/interval_tmp_" + str(a) + "_" + str(b) + ".txt", 'w') as file:
                        # 파일에 내용 쓰기
                        file.write(str(train_data_split))

                    train_data_split = []
                    b += 1

        if len(train_data_split) != 0: #이건 맞는지 모르겠다
            with open("api_data/data_tmp/interval_tmp_" + str(a) + "_" + str(b) + ".txt", 'w') as file:
                # 파일에 내용 쓰기
                file.write(str(train_data_split))

        print("파일 한개 완료")
        a += 1
        b = 1
        

