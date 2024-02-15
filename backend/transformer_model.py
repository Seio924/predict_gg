import tensorflow as tf
import numpy as np

class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self):
        super(PositionalEncoding, self).__init__()

    def call(self, data):
        print(data.shape)
        t, n, dim = data.shape
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

    def call(self, data, look_ahead_mask=None, padding_mask=None):
        data_with_pos_enc = PositionalEncoding()(data)

        query = self.query_dense(data_with_pos_enc)
        key = self.key_dense(data_with_pos_enc)
        value = self.value_dense(data_with_pos_enc)
        
        query = tf.concat(tf.split(query, self.num_heads, axis=-1), axis=0)
        key = tf.concat(tf.split(key, self.num_heads, axis=-1), axis=0)
        value = tf.concat(tf.split(value, self.num_heads, axis=-1), axis=0)
        
        self_attention_value = self.attention(query, key, value)

        if look_ahead_mask is not None:
            # 룩어헤드 마스크 적용
            self_attention_value *= look_ahead_mask

        if padding_mask is not None:
            # 패딩 마스크 적용
            self_attention_value *= padding_mask
        
        return self_attention_value


class MultiHeadAttention(tf.keras.Model):
    def __init__(self, d_model, num_heads, num_transformer_layers):
        super(MultiHeadAttention, self).__init__()
        self.num_transformer_layers = num_transformer_layers
        self.transformer_layers = [TransformerLayer(d_model, num_heads) for _ in range(num_transformer_layers)]
        self.final_dense = tf.keras.layers.Dense(2, activation='softmax')

    def call(self, data):  # padding_mask 인수 추가
        output, target, padding_mask = data
        print("패딩마스크")
        print(padding_mask)
        for i in range(self.num_transformer_layers):
            output = self.transformer_layers[i](output, look_ahead_mask=None, padding_mask=padding_mask)  # 패딩 마스크를 적용하는 부분, look_ahead_mask=None으로 수정
        
        # 모델의 출력을 받아서 이진 분류를 위한 로짓값으로 변환
        logits = self.final_dense(output)
        
        # 손실을 계산하기 위해 예측값(logits)과 타겟 데이터(target) 반환
        return logits


