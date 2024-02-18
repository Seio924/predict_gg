import os
import tensorflow as tf
import numpy as np
from datetime import datetime
from keras.callbacks import ModelCheckpoint  # keras의 ModelCheckpoint 사용
from utils_2 import binary_cross_entropy_loss, mse_loss, rnn_sequential
from load_data import LoadData
import h5py

class GeneralRNN():
    """RNN predictive model for time-series data.
    
    Attributes:
        - model_parameters:
            - task: classification or regression
            - model_type: 'rnn', 'lstm', or 'gru'
            - h_dim: hidden dimensions
            - n_layer: the number of layers
            - batch_size: the number of samples in each batch
            - epoch: the number of iteration epochs
            - learning_rate: the learning rate of model training
    """

    def __init__(self, model_parameters):
        self.task = model_parameters['task']
        self.model_type = model_parameters['model_type']
        self.h_dim = model_parameters['h_dim']
        self.n_layer = model_parameters['n_layer']
        self.batch_size = model_parameters['batch_size']
        self.epoch = model_parameters['epoch']
        self.learning_rate = model_parameters['learning_rate']
        
        assert self.model_type in ['rnn', 'lstm', 'gru']

        # Predictor model define
        self.predictor_model = self._build_model()  # 모델 빌드

        timestamp = datetime.now().strftime('%H%M%S')
        
        # Set path for model saving
        if self.model_type == 'rnn':
            model_folder = 'backend/modelRNN'
        elif self.model_type == 'lstm':
            model_folder = 'backend/modelLSTM'
        elif self.model_type == 'gru':
            model_folder = 'backend/modelGRU'

        if not os.path.exists(model_folder):
            os.makedirs(model_folder)

        # Create HDF5 file
        self.save_file_name = os.path.join(model_folder, f'{timestamp}.hdf5')
        with h5py.File(self.save_file_name, 'w'):
            pass  # 아무 작업도 수행하지 않고 빈 HDF5 파일 생성

    def _build_model(self):
        """Construct the model using feature and label statistics."""
        # Parameters
        h_dim = self.h_dim
        n_layer = self.n_layer
        dim = 88  # Assuming LIST_LEN is always 88
        max_seq_len = 301  # Assuming max_length_data is always 301

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Masking(mask_value=0., input_shape=(max_seq_len, dim)))

        for _ in range(n_layer - 1):
            model = rnn_sequential(model, self.model_type, h_dim, return_seq=True)

        model = rnn_sequential(model, self.model_type, h_dim, 
                            return_seq=False)
        adam = tf.keras.optimizers.Adam(learning_rate=self.learning_rate, 
                                        beta_1=0.9, beta_2=0.999, amsgrad=False)

        if self.task == 'classification':
            model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
            model.compile(loss=binary_cross_entropy_loss, optimizer=adam)
            
        elif self.task == 'regression':
            model.add(tf.keras.layers.Dense(2, activation='softmax'))
            model.compile(loss=binary_cross_entropy_loss, optimizer=adam, metrics=['accuracy', 'mse'])

        return model
    
    def fit(self, x, y):
        """Fit the predictor model."""
        # Callback for the best model saving
        save_best = ModelCheckpoint(self.save_file_name, monitor='val_loss',
                                    mode='min', verbose=False,
                                    save_best_only=True)

        # Train the model
        self.predictor_model.fit(x, y, 
                                batch_size=self.batch_size, epochs=self.epoch, 
                                callbacks=[save_best], verbose=True)

        return self.predictor_model
    
    def predict(self, test_x):
        """Return the temporal and feature importance."""
        # Add a new axis to make the input data a sequence
        test_x = np.expand_dims(test_x, axis=0)
        test_y_hat = self.predictor_model.predict(test_x)
        return test_y_hat

if __name__ == "__main__":
    api_key = 'RGAPI-6d3dda9d-b317-4db1-88ed-340d31cad6d4'
    load_instance = LoadData(api_key)

    train_data, win_lose_list = load_instance.get_diamond1_data_list(3)
    d = len(train_data[0])
    print(d)

    LIST_LEN = 88

    # 시계열 데이터의 최대 길이 계산
    max_length_data = 301

    # 패딩을 적용한 배열 생성
    padded_data = np.zeros((len(train_data), max_length_data, LIST_LEN))
    for i, seq in enumerate(train_data):
        padded_data[i, :len(seq), :] = seq

    win_lose_list = np.array(win_lose_list, dtype="float32")

    # Instantiate the GeneralRNN model
    model_parameters = {
        'task': 'regression',
        'model_type': 'gru',  # or 'rnn', 'lstm'
        'h_dim': 64,  # Hidden dimension
        'n_layer': 2,  # Number of layers
        'batch_size': 32,  # Batch size
        'epoch': 10,  # Number of epochs
        'learning_rate': 0.001  # Learning rate
    }
    rnn_model = GeneralRNN(model_parameters)

    # Train the model
    trained_model = rnn_model.fit(padded_data, win_lose_list)

    predict_data = padded_data[0][:1].copy()
    print(predict_data.shape)

    # 패딩을 적용한 배열 생성
    padded_predict_data = np.zeros((max_length_data, LIST_LEN))
    for i, seq in enumerate(predict_data):
        padded_predict_data[i, :] = seq

    print(padded_predict_data.shape)
    print(padded_predict_data)

    # Now you can use the trained model to predict
    predictions = rnn_model.predict(padded_predict_data)

    print(predictions)

    predict_data = padded_data[0][:30].copy()


    padded_predict_data = np.zeros((max_length_data, LIST_LEN))
    for i, seq in enumerate(predict_data):
        padded_predict_data[i, :] = seq

    predictions = rnn_model.predict(padded_predict_data)

    print(predictions)

    predict_data = padded_data[0][:60].copy()


    padded_predict_data = np.zeros((max_length_data, LIST_LEN))
    for i, seq in enumerate(predict_data):
        padded_predict_data[i, :] = seq

    predictions = rnn_model.predict(padded_predict_data)

    print(predictions)

    predict_data = padded_data[0][:91].copy()


    padded_predict_data = np.zeros((max_length_data, LIST_LEN))
    for i, seq in enumerate(predict_data):
        padded_predict_data[i, :] = seq

    predictions = rnn_model.predict(padded_predict_data)

    print(predictions)

    predict_data = padded_data[0][:121].copy()


    padded_predict_data = np.zeros((max_length_data, LIST_LEN))
    for i, seq in enumerate(predict_data):
        padded_predict_data[i, :] = seq

    predictions = rnn_model.predict(padded_predict_data)

    print(predictions)