from load_data import LoadData


api_key = 'RGAPI-45f32b24-d486-4041-b2e0-c5e9b961ab4f'

load_instance = LoadData(api_key)

#load_instance.process_challenger_data(1000)

load_instance.process_diamond1_data(500)

# load_instance.get_diamond1_info()

# load_instance.get_challenger_info()
