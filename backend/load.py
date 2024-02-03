from load_data import LoadData


api_key = 'RGAPI-3cfedfee-6699-4af0-8139-28420199de7a'

load_instance = LoadData(api_key)

load_instance.process_challenger_data(180)
