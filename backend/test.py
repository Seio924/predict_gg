def split_and_save(interval_file, win_lose_file, num, chunk_size):
    with open(interval_file, 'r') as f:
        data1 = f.readlines()

    with open(win_lose_file, 'r') as f:
        data2 = f.readlines()

    num_chunks1 = len(data1) // chunk_size + (1 if len(data1) % chunk_size != 0 else 0)
    num_chunks2 = len(data2) // chunk_size + (1 if len(data2) % chunk_size != 0 else 0)


    for i in range(num_chunks1):
        chunk = data1[i * chunk_size: (i + 1) * chunk_size]
        output_file = f'api_data/data_split/interval_split_{num}_{i+1}.txt'

        with open(output_file, 'w') as f:
            f.writelines(chunk)

    for i in range(num_chunks2):
        chunk = data2[i * chunk_size: (i + 1) * chunk_size]
        output_file = f'api_data/data_split/win_lose_split_{num}_{i+1}.txt'    

        with open(output_file, 'w') as f:
            f.writelines(chunk)

if __name__ == "__main__":
    chunk_size = 200  # 각 청크 크기
    num = 1

    interval_files = ['api_interval_list1-1', 'api_interval_list1-2', 'api_interval_list1-3', 'api_interval_list1-4', 'api_interval_list1-5', 'api_interval_list1-6', 'api_interval_list1-7', 'api_interval_list1-8',
                     'api_interval_list2-1', 'api_interval_list2-2', 'api_interval_list2-3', 'api_interval_list2-4', 'api_interval_list2-5', 'api_interval_list2-6', 'api_interval_list2-7', 'api_interval_list2-8',
                     'api_interval_list3-1', 'api_interval_list3-2', 'api_interval_list3-3', 'api_interval_list3-4', 'api_interval_list3-5', 'api_interval_list3-6', 'api_interval_list3-7', 'api_interval_list3-8']
    
    win_lose_files = ['api_win_lose_list1-1', 'api_win_lose_list1-2', 'api_win_lose_list1-3', 'api_win_lose_list1-4', 'api_win_lose_list1-5', 'api_win_lose_list1-6', 'api_win_lose_list1-7', 'api_win_lose_list1-8',
                     'api_win_lose_list2-1', 'api_win_lose_list2-2', 'api_win_lose_list2-3', 'api_win_lose_list2-4', 'api_win_lose_list2-5', 'api_win_lose_list2-6', 'api_win_lose_list2-7', 'api_win_lose_list2-8',
                     'api_win_lose_list3-1', 'api_win_lose_list3-2', 'api_win_lose_list3-3', 'api_win_lose_list3-4', 'api_win_lose_list3-5', 'api_win_lose_list3-6', 'api_win_lose_list3-7', 'api_win_lose_list3-8']


    for interval_file, win_lose_file in zip(interval_files, win_lose_files):
        print(interval_file, win_lose_file)
        interval_file = f'api_data/data/{interval_file}.txt'
        win_lose_file = f'api_data/data/{win_lose_file}.txt'
        split_and_save(interval_file, win_lose_file, num, chunk_size)
        num += 1
