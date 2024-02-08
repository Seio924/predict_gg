import tensorflow as tf
import numpy as np

def positional_encoding(data):
    n, dim = data.shape
    pos_enc = np.zeros((n, dim))

    for i in range(dim):
        if i % 2 == 0:
            pos_enc[:, i] = np.sin(np.arange(0, n) / 10000**(2 * i / dim))
        else:
            pos_enc[:, i] = np.cos(np.arange(0, n) / 10000**(2 * (i - 1) / dim))

    for i in range(n):
        if i % 2 == 0:
            pos_enc[i, :] *= np.sin(np.arange(0, dim) / 10000**(2 * i / n))
        else:
            pos_enc[i, :] *= np.cos(np.arange(0, dim) / 10000**(2 * (i - 1) / n))

    return pos_enc

def add_positional_encoding(data):
    pos_enc = positional_encoding(data)
    return data + pos_enc

def linear_layer(data, units):
    data_with_pos_enc = add_positional_encoding(data)
    linear_model = tf.keras.Sequential([
        tf.keras.layers.Dense(units)
    ])
    return linear_model(data_with_pos_enc)

# 예제 데이터
data = np.array([[1000, 500, 100, 500], [2000, 550, 150, 500]])

# Linear 연산을 수행한 결과 출력
linear_result = linear_layer(data, units=10)
print(linear_result)
