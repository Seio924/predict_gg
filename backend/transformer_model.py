import tensorflow as tf

def scaled_dot_product_attention(q, k, v, mask):
    matmul_qk = tf.matmul(q, k, transpose_b=True)
    dk = tf.cast(tf.shape(k)[-1], tf.float32)
    scaled_attention_logits = matmul_qk / tf.math.sqrt(dk)

    if mask is not None:
        scaled_attention_logits += (mask * -1e9)

    attention_weights = tf.nn.softmax(scaled_attention_logits, axis=-1)
    output = tf.matmul(attention_weights, v)

    return output, attention_weights

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

def build_transformer_model(num_blocks, units, d_model, num_heads, dropout, input_shape):
    inputs = tf.keras.layers.Input(shape=input_shape, name="inputs")
    padding_mask = tf.keras.layers.Input(shape=(1, 1, None), name="padding_mask")

    x = inputs

    for i in range(num_blocks):
        x = transformer_encoder_block(units=units, d_model=d_model, num_heads=num_heads, dropout=dropout, name=f"transformer_block_{i}")([x, padding_mask])

    return tf.keras.Model(inputs=[inputs, padding_mask], outputs=x, name="transformer")

# Example usage:
num_blocks = 2
units = 512
d_model = 128
num_heads = 4
dropout = 0.3
input_shape = (seq_len, feature_dim)  # 실제 입력 모양으로 교체

model = build_transformer_model(num_blocks, units, d_model, num_heads, dropout, input_shape)
