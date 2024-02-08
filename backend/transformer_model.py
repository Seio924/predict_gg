import tensorflow as tf
import numpy as np

class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self):
        super(PositionalEncoding, self).__init__()

    def call(self, data):
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

        return data + pos_enc

class ScaledDotProductAttention(tf.keras.layers.Layer):
    def __init__(self):
        super(ScaledDotProductAttention, self).__init__()

    def call(self, query, key, value):
        # query와 key를 내적하여 attention score 계산
        attention_score = tf.matmul(query, key, transpose_b=True)
        
        # scale factor로 나누어줌
        d_model = tf.cast(tf.shape(key)[-1], tf.float32)
        attention_score /= tf.math.sqrt(d_model)
        
        # softmax 함수를 사용하여 attention score 계산 -> 0~1사이로 정규화
        attention_weights = tf.nn.softmax(attention_score, axis=-1)
        
        # attention score와 value를 내적하여 self-attention value 계산
        self_attention_value = tf.matmul(attention_weights, value)
        
        return self_attention_value

class TransformerLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads):
        super(TransformerLayer, self).__init__()
        self.query_dense = tf.keras.layers.Dense(d_model)
        self.key_dense = tf.keras.layers.Dense(d_model)
        self.value_dense = tf.keras.layers.Dense(d_model)
        self.attention = ScaledDotProductAttention()
        self.num_heads = num_heads
        self.d_model = d_model

    def call(self, data, look_ahead_mask=None):
        data_with_pos_enc = PositionalEncoding()(data)

        # query, key, value의 차원을 d_model로 줄이기 -> Linear layer와 곱하기
        query = self.query_dense(data_with_pos_enc)
        key = self.key_dense(data_with_pos_enc)
        value = self.value_dense(data_with_pos_enc)
        
         # 다음 연산을 위해 각각의 차원을 num_heads로 나누기
        query = tf.concat(tf.split(query, self.num_heads, axis=-1), axis=0)
        key = tf.concat(tf.split(key, self.num_heads, axis=-1), axis=0)
        value = tf.concat(tf.split(value, self.num_heads, axis=-1), axis=0)
        
        # scaled_dot_product_attention 함수를 호출하여 self-attention value 계산
        self_attention_value = self.attention(query, key, value)

        # 룩어헤드 마스크 적용 (현재 시점에서 이후의 시점에 대한 정보를 모델이 보지못하도록)
        if look_ahead_mask is not None:
            self_attention_value *= look_ahead_mask
        
        return self_attention_value

class MultiHeadAttention(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        self.query_dense = tf.keras.layers.Dense(d_model)
        self.key_dense = tf.keras.layers.Dense(d_model)
        self.value_dense = tf.keras.layers.Dense(d_model)
        self.attention = ScaledDotProductAttention()
        self.final_dense = tf.keras.layers.Dense(d_model)
        self.num_heads = num_heads
        self.d_model = d_model

    def call(self, data):
        # Multi-head self-attention 수행을 위해 query, key, value 생성
        query = self.query_dense(data)
        key = self.key_dense(data)
        value = self.value_dense(data)

        # 다음 연산을 위해 각각의 차원을 num_heads로 나누기
        query = tf.concat(tf.split(query, self.num_heads, axis=-1), axis=0)
        key = tf.concat(tf.split(key, self.num_heads, axis=-1), axis=0)
        value = tf.concat(tf.split(value, self.num_heads, axis=-1), axis=0)
        
        # scaled_dot_product_attention 함수를 호출하여 각 head 별 self-attention value 계산
        self_attention_value = self.attention(query, key, value)
        
        # 각 head의 self-attention value를 다시 합치기
        concat_attention = tf.concat(tf.split(self_attention_value, self.num_heads, axis=0), axis=-1)
        
        # 마지막 linear layer 적용
        return self.final_dense(concat_attention)
