import tensorflow as tf
import numpy as np
from utils import PreprocessData
from transformer_model import TransformerLayer, MultiHeadAttention

test = PreprocessData('./backend/api_match_info.json', './backend/api_timeline_info.json')

train_data = []

for i in range(100):
    # 데이터 가져오기
    interval_list = test.get_condition_timeline(10000)

    # 학습 데이터 로드
    train_data.append(interval_list)

train_data = np.array(train_data, dtype=int)

# Dataset 객체 생성
train_dataset = tf.data.Dataset.from_tensor_slices(train_data)

# 배치 생성
batch_size = 32
train_dataset = train_dataset.shuffle(buffer_size=len(train_data)).batch(batch_size)

# 모델 생성
num_heads = 16
d_model = 4
transformer_layer = TransformerLayer(d_model=d_model, num_heads=num_heads)
multi_head_attention = MultiHeadAttention(d_model=d_model, num_heads=num_heads)
model = tf.keras.Sequential([
    transformer_layer,
    multi_head_attention
])

# 모델 컴파일
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 모델 학습
num_epochs = 10
model.fit(train_dataset, epochs=num_epochs)
