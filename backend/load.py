from load_data import LoadData


api_key = 'RGAPI-59ffd1a9-2677-40b0-be5d-24151cd90ec9'

load_instance = LoadData(api_key)

load_instance.process_challenger_data(65)

#load_instance.get_challenger_info()
