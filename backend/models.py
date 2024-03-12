import os
import tensorflow as tf
import numpy as np
from datetime import datetime
from keras.callbacks import ModelCheckpoint  # keras의 ModelCheckpoint 사용
from utils_2 import binary_cross_entropy_loss, mse_loss, rnn_sequential
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
        dim = 177  # Assuming LIST_LEN is always 91
        max_seq_len = 366  # Assuming max_length_data is always 301

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
        
        train_x, train_y = x[:40320], y[:40320]
        valid_x, valid_y = x[40320:], y[40320:]
        
        self.predictor_model = self._build_model(train_x, train_y)

        # Callback for the best model saving
        save_best = ModelCheckpoint(self.save_file_name, monitor='val_loss',
                                    mode='min', verbose=False,
                                    save_best_only=True)

        # Train the model
        self.predictor_model.fit(train_x, train_y, 
                                batch_size=self.batch_size, epochs=self.epoch, 
                                validation_data=(valid_x, valid_y), 
                                callbacks=[save_best], verbose=True)

        return self.predictor_model
    
    