import tensorflow as tf
import numpy as np

def scaled_dot_product_attention(q, k, v, mask):
    # 내적을 통해 각 쌍의 유사도를 나타내는 어텐션 스코어 행렬 생성
    matmul_qk = tf.matmul(q, k, transpose_b=True)

    #Key(K)의 차원 수
    dk = tf.cast(tf.shape(k)[-1], tf.float32)

    #스케일링된 어텐션 스코어를 계산 (정규화, 표준화)
    scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)
    
    #모델이 미래의 정보를 사용하여 예측하지 않도록 마스크 적용
    if mask is not None:
        scaled_attention_logits += (mask * -1e9)

    #스케일링된 어텐션 스코어를 정규화하여 어텐션 가중치를 계산 [ 각 Key(K)에 대한 Query(Q)의 중요도 ]
    attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)

    #어텐션 가중치와 Value(V)의 내적을 계산하여 어텐션 출력 생성 -> 각 Key(K)에 대한 가중합
    output = tf.matmul(attention_weights, v)

    return output, attention_weights #가중합, 가중치

class MultiHeadAttentionLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttentionLayer, self).__init__()
        self.num_heads = num_heads
        self.d_model = d_model

        assert d_model % self.num_heads == 0

        self.depth = d_model // self.num_heads

        self.query_dense = tf.keras.layers.Dense(d_model)
        self.key_dense = tf.keras.layers.Dense(d_model)
        self.value_dense = tf.keras.layers.Dense(d_model)

        self.dense = tf.keras.layers.Dense(d_model)

    def split_heads(self, x, batch_size):
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(x, perm=[0, 2, 1, 3])

    def call(self, inputs):
        q, k, v, mask = inputs['q'], inputs['k'], inputs['v'], inputs['mask']
        batch_size = tf.shape(q)[0]

        q = self.query_dense(q)
        k = self.key_dense(k)
        v = self.value_dense(v)

        q = self.split_heads(q, batch_size)
        k = self.split_heads(k, batch_size)
        v = self.split_heads(v, batch_size)

        scaled_attention, _ = scaled_dot_product_attention(q, k, v, mask)
        scaled_attention = tf.transpose(scaled_attention, perm=[0, 2, 1, 3])

        concat_attention = tf.reshape(scaled_attention, (batch_size, -1, self.d_model))
        output = self.dense(concat_attention)

        return output

def positional_encoding(data):
    #순서 정해주기 [행과 열]
    n, dim = data.shape
    pos_enc = np.zeros((n, dim))

    #열 데이터 순서 설정
    for i in range(dim):
        if i % 2 == 0:
            pos_enc[:, i] = np.sin(np.arange(0, n) / 10000**(2 * i / dim))
        else:
            pos_enc[:, i] = np.cos(np.arange(0, n) / 10000**(2 * (i - 1) / dim))

    #행 데이터 순서 설정
    for i in range(n):
        if i % 2 == 0:
            pos_enc[i, :] *= np.sin(np.arange(0, dim) / 10000**(2 * i / n))
        else:
            pos_enc[i, :] *= np.cos(np.arange(0, dim) / 10000**(2 * (i - 1) / n))
        

    return pos_enc

def transformer_encoder_block(units, d_model, num_heads, dropout, name="transformer_encoder_block"):
    inputs = tf.keras.layers.Input(shape=(None, d_model), name="inputs")
    padding_mask = tf.keras.layers.Input(shape=(1, 1, None), name="padding_mask")

    attention = MultiHeadAttentionLayer(d_model, num_heads)({'q': inputs, 'k': inputs, 'v': inputs, 'mask': padding_mask})
    attention = tf.keras.layers.Dropout(rate=dropout)(attention)
    attention = tf.keras.layers.LayerNormalization(epsilon=1e-6)(inputs + attention)

    outputs = tf.keras.layers.Dense(units=units, activation='relu')(attention)
    outputs = tf.keras.layers.Dense(units=d_model)(outputs)
    outputs = tf.keras.layers.Dropout(rate=dropout)(outputs)
    outputs = tf.keras.layers.LayerNormalization(epsilon=1e-6)(attention + outputs)

    return tf.keras.Model(inputs=[inputs, padding_mask], outputs=outputs, name=name)

def build_transformer_model(num_blocks, units, d_model, num_heads, dropout, input_shape, vocab_size):
    #Input layer [모델의 입력 정의] -> seq_len : 데이터 행 길이
    inputs = tf.keras.layers.Input(shape=input_shape, name="inputs")
    
    #마스킹해서 현재 정보만
    padding_mask = tf.keras.layers.Input(shape=(1, 1, None), name="padding_mask")

    # Embedding 레이어 추가 [input embedding과 positional encoding 더해줘야 함]
    embedding = tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=d_model)(inputs)

    x = embedding

    for i in range(num_blocks):
        x = transformer_encoder_block(units=units, d_model=d_model, num_heads=num_heads, dropout=dropout, name=f"transformer_block_{i}")([x, padding_mask])

    return tf.keras.Model(inputs=[inputs, padding_mask], outputs=x, name="transformer")

# Example usage:
num_blocks = 2
units = 512
d_model = 128
num_heads = 4
dropout = 0.3
seq_len = 100  # 예시 값, 실제 데이터에 따라 조정
feature_dim = 32  # 예시 값, 실제 데이터에 따라 조정
vocab_size = 10000  # 예시 값, 실제 데이터에 따라 조정

input_shape = (seq_len,)

model = build_transformer_model(num_blocks, units, d_model, num_heads, dropout, input_shape, vocab_size)
