import os
import tensorflow as tf
import numpy as np
from datetime import datetime
from keras.callbacks import ModelCheckpoint  # keras의 ModelCheckpoint 사용
from utils_2 import binary_cross_entropy_loss, mse_loss, rnn_sequential
from load_data import LoadData

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
        self.predictor_model = None

        # Set path for model saving
        model_path = 'backend/model'
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        self.save_file_name = '{}'.format(model_path) + \
                            datetime.now().strftime('%H%M%S') + '.hdf5'
    
    def _build_model(self, x, y):
        """Construct the model using feature and label statistics.
        
        Args:
            - x: features
            - y: labels
            
        Returns:
            - model: predictor model
        """    
        

        # Parameters
        h_dim = self.h_dim
        n_layer = self.n_layer
        dim = len(x[0][0][:])
        max_seq_len = len(x[0][:])       

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Masking(mask_value=0., input_shape=(max_seq_len, dim)))

        for _ in range(n_layer - 1):
            model = rnn_sequential(model, self.model_type, h_dim, return_seq=True)

        model = rnn_sequential(model, self.model_type, h_dim, 
                            return_seq=False)
        adam = tf.keras.optimizers.Adam(learning_rate=self.learning_rate, 
                                        beta_1=0.9, beta_2=0.999, amsgrad=False)

        if self.task == 'classification':
            model.add(tf.keras.layers.Dense(y.shape[-1], activation='sigmoid'))
            model.compile(loss=binary_cross_entropy_loss, optimizer=adam)
            
        elif self.task == 'regression':
            model.add(tf.keras.layers.Dense(y.shape[-1], activation='linear'))
            model.compile(loss=mse_loss, optimizer=adam, metrics=['mse'])

        return model
    
    def fit(self, x, y):
        """Fit the predictor model.
        
        Args:
            - x: training features
            - y: training labels
            
        Returns:
            - self.predictor_model: trained predictor model
        """
        idx = np.random.permutation(len(x))
        train_idx = idx[:int(len(idx)*0.8)]
        valid_idx = idx[int(len(idx)*0.8):]

        # Convert train_idx and valid_idx to integer scalar arrays
        train_idx = np.arange(len(x))[train_idx]
        valid_idx = np.arange(len(x))[valid_idx]
        
        train_x, train_y = x, y
        
        self.predictor_model = self._build_model(train_x, train_y)

        # Callback for the best model saving
        save_best = ModelCheckpoint(self.save_file_name, monitor='val_loss',
                                    mode='min', verbose=False,
                                    save_best_only=True)

        # Train the model
        self.predictor_model.fit(train_x, train_y, 
                                batch_size=self.batch_size, epochs=self.epoch, 
                                 
                                callbacks=[save_best], verbose=True)

        self.predictor_model.load_weights(self.save_file_name)
        os.remove(self.save_file_name)

        return self.predictor_model
    
    def predict(self, test_x):
        """Return the temporal and feature importance.
        
        Args:
            - test_x: testing features
            
        Returns:
            - test_y_hat: predictions on testing set
        """
        test_y_hat = self.predictor_model.predict(test_x)
        return test_y_hat

if __name__ == "__main__":
    api_key = 'RGAPI-6d3dda9d-b317-4db1-88ed-340d31cad6d4'
    load_instance = LoadData(api_key)

    train_data, win_lose_list = load_instance.get_diamond1_data_list(10)

    LIST_LEN = 88

        

    # 시계열 데이터의 최대 길이 계산
    max_length_data = 301
    max_length_target = 301

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

    # Assuming you have your time-series data 'x' and corresponding labels 'y'
    # x should be of shape (num_samples, max_seq_len, num_features)
    # y should be of shape (num_samples, num_labels) for regression
    # Train the model

    trained_model = rnn_model.fit(padded_data, win_lose_list)

    # Now you can use the trained model to predict
    # Assuming you have test data 'test_x' of shape (num_samples_test, max_seq_len, num_features)
    predictions = rnn_model.predict(padded_data[0])
