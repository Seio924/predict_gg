import tensorflow as tf
import numpy as np
import os
import shutil


class Attention(tf.keras.Model):
    """Attention class.

    Attributes:
      - model_parameters:
        - task: classificiation or regression
        - h_dim: hidden state dimensions
        - batch_size: the number of samples in each mini-batch
        - epoch: the number of iterations
        - learning_rate: learning rate of training
    """

    def __init__(self, model_parameters):
        super(Attention, self).__init__()
        self.task = model_parameters['task']
        self.h_dim = model_parameters['h_dim']
        self.batch_size = model_parameters['batch_size']
        self.epoch = model_parameters['epoch']
        self.learning_rate = model_parameters['learning_rate']
        self.save_file_directory = model_parameters['save_file_directory']

    def process_batch_input_for_RNN(self, batch_input):
        """Function to convert batch input data to use scan ops of tensorflow.

        Args:
          - batch_input: original batch input

        Returns:
          - x: batch_input for RNN
        """
        return tf.transpose(batch_input, perm=[0, 2, 1])

    def sample_X(self, m, n):
        """Sample from the real data (Mini-batch index sampling)."""
        return np.random.permutation(m)[:n]

    def call(self, x):
        pass

    def fit(self, x, y):
        """Train the model.

        Args:
          - x: training feature
          - y: training label
        """

        # Basic parameters
        no, seq_len, x_dim = x.shape
        y_dim = len(y[0, :])

        # Weights for GRU
        Wr = tf.Variable(tf.zeros([x_dim, self.h_dim]))
        Ur = tf.Variable(tf.zeros([self.h_dim, self.h_dim]))
        br = tf.Variable(tf.zeros([self.h_dim]))

        Wu = tf.Variable(tf.zeros([x_dim, self.h_dim]))
        Uu = tf.Variable(tf.zeros([self.h_dim, self.h_dim]))
        bu = tf.Variable(tf.zeros([self.h_dim]))

        Wh = tf.Variable(tf.zeros([x_dim, self.h_dim]))
        Uh = tf.Variable(tf.zeros([self.h_dim, self.h_dim]))
        bh = tf.Variable(tf.zeros([self.h_dim]))

        # Weights for attention mechanism
        Wa1 = tf.Variable(tf.random.truncated_normal([self.h_dim + x_dim, self.h_dim], mean=0, stddev=.01))
        Wa2 = tf.Variable(tf.random.truncated_normal([self.h_dim, y_dim], mean=0, stddev=.01))
        ba1 = tf.Variable(tf.random.truncated_normal([self.h_dim], mean=0, stddev=.01))
        ba2 = tf.Variable(tf.random.truncated_normal([y_dim], mean=0, stddev=.01))

        # Weights for output layers
        Wo = tf.Variable(tf.random.truncated_normal([self.h_dim, y_dim], mean=0, stddev=.01))
        bo = tf.Variable(tf.random.truncated_normal([y_dim], mean=0, stddev=.01))

        # Target
        Y = tf.keras.Input(shape=(1,))

        # Input vector with shape[batch, seq, embeddings]
        _inputs = tf.keras.Input(shape=(None, x_dim), name='inputs')

        # Processing inputs to work with scan function
        processed_input = self.process_batch_input_for_RNN(_inputs)

        # Initial Hidden States
        initial_hidden = _inputs[:, 0, :]
        initial_hidden = tf.matmul(initial_hidden, tf.zeros([x_dim, self.h_dim]))

        def GRU(previous_hidden_state, x):
            # R Gate
            r = tf.sigmoid(tf.matmul(x, Wr) + tf.matmul(previous_hidden_state, Ur) + br)
            # U Gate
            u = tf.sigmoid(tf.matmul(x, Wu) + tf.matmul(previous_hidden_state, Uu) + bu)
            # Final Memory cell
            c = tf.tanh(tf.matmul(x, Wh) + tf.matmul(tf.multiply(r, previous_hidden_state), Uh) + bh)
            # Current Hidden state
            current_hidden_state = tf.multiply((1 - u), previous_hidden_state) + tf.multiply(u, c)
            return current_hidden_state

        def get_states():
          # Getting all hidden state through time
          all_hidden_states = tf.TensorArray(tf.float32, size=seq_len)
          initial_hidden = _inputs[:, 0, :]
          all_hidden_states = all_hidden_states.write(0, initial_hidden)
          
          def step(previous_hidden_state, x):
              current_hidden_state = GRU(previous_hidden_state, x)
              return current_hidden_state
          
          for i in range(1, seq_len):
              current_input = processed_input[i]
              previous_hidden_state = all_hidden_states.read(i - 1)
              current_hidden_state = step(previous_hidden_state, current_input)
              all_hidden_states = all_hidden_states.write(i, current_hidden_state)
          
          all_hidden_states = all_hidden_states.stack()
          
          return all_hidden_states

        def get_attention(hidden_state):
            inputs = tf.concat((hidden_state, processed_input[-1]), axis=1)
            hidden_values = tf.nn.tanh(tf.matmul(inputs, Wa1) + ba1)
            e_values = (tf.matmul(hidden_values, Wa2) + ba2)
            return e_values

        def get_outputs():
          # Get all hidden states through time
          all_hidden_states = get_states()
          
          # Initialize TensorArray to store attention values
          all_attention = tf.TensorArray(tf.float32, size=0, dynamic_size=True)
          
          # Iterate through all hidden states and calculate attention for each
          for hidden_state in all_hidden_states:
              attention = get_attention(hidden_state)
              all_attention = all_attention.write(all_attention.size(), attention)
          
          # Stack the attention values to form a tensor
          all_attention = all_attention.stack()
          
          # Apply softmax to get attention weights
          a_values = tf.nn.softmax(all_attention, axis=0)
          
          # Compute final hidden state using attention weights
          final_hidden_state = tf.einsum('ijk,ijl->jkl', a_values, all_hidden_states)
          
          # Compute output using final hidden state
          output = tf.nn.sigmoid(tf.matmul(final_hidden_state[:, 0, :], Wo) + bo, name='outputs')
          
          return output


        # Getting all outputs from rnn
        outputs = get_outputs()

        # reshape out for sequence_loss
        if self.task == 'classification':
            loss = tf.reduce_mean(Y * tf.log(outputs + 1e-8) + (1 - Y) * tf.log(1 - outputs + 1e-8))
        elif self.task == 'regression':
            loss = tf.sqrt(tf.reduce_mean(tf.square(outputs - Y)))

        # Optimization
        optimizer = tf.keras.optimizers.Adam(self.learning_rate)

        # Compile the model
        self.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

        # Training
        self.fit(x, y, batch_size=self.batch_size, epochs=self.epoch)

    def predict(self, test_x):
        """Prediction with trained model.

        Args:
          - test_x: testing features

        Returns:
          - test_y_hat: predictions on testing set
        """
        test_y_hat = self.predict(test_x)
        return test_y_hat
