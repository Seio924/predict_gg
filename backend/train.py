import tensorflow as tf
import numpy as np
from load_data import LoadData
from transformer_model import MultiHeadAttention

LIST_LEN = 88

api_key = 'RGAPI-b073b9c4-d395-4c94-8f9e-b8c1ad4c9045'

def create_padding_mask(data):
    # 입력 시퀀스에서 0인 부분을 찾아내는 마스크 생성
    mask = tf.cast(tf.reduce_all(tf.math.equal(data, 0), axis=-1), tf.float32)
    # 패딩된 부분을 1로, 그렇지 않은 부분을 0으로 변경
    return mask[:, tf.newaxis, tf.newaxis, :]

# 이진 크로스 엔트로피 손실 함수 정의
def binary_crossentropy_loss(y_true, y_pred):
    # y_true: 실제 승리 여부 데이터
    # y_pred: 모델의 출력 (확률 값)

    # 이진 크로스 엔트로피 손실 계산
    loss = tf.keras.losses.binary_crossentropy(y_true, y_pred)

    return loss

load_instance = LoadData(api_key)

# 데이터 가져오기
train_data, win_lose_list = load_instance.get_summoner_data_list(3)
print(len(train_data[0]))
print(len(train_data[1]))
print(len(win_lose_list[0]))
print(len(win_lose_list[1]))


# 시계열 데이터의 최대 길이 계산
max_length_data = max(len(seq) for seq in train_data)
max_length_target = max(len(seq) for seq in win_lose_list)

print(max_length_data)
print(max_length_target)

# 패딩을 적용한 배열 생성
padded_data = np.zeros((len(train_data), max_length_data, LIST_LEN), dtype=int)
for i, seq in enumerate(train_data):
    padded_data[i, :len(seq), :] = seq

# 패딩을 적용한 배열 생성
padded_data2 = np.zeros((len(win_lose_list), max_length_target, 2), dtype=int)
for i, seq in enumerate(win_lose_list):
    print("len : " + str(len(seq)))
    padded_data2[i, :len(seq), :] = seq

print(padded_data)

print(padded_data2)

padding_mask = create_padding_mask(padded_data)


# Dataset 객체 생성
input_dataset = tf.data.Dataset.from_tensor_slices((padded_data, padded_data2, padding_mask))

# 배치 생성
batch_size = 128
combined_dataset = input_dataset.shuffle(buffer_size=len(train_data)).batch(batch_size)

# 모델 생성
num_heads = 1
d_model = LIST_LEN
num_transformer_layers = 2
learning_rate = 0.001
num_epochs = 100

# 모델 생성 및 컴파일
model = MultiHeadAttention(d_model, num_heads, num_transformer_layers)
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
model.compile(optimizer=optimizer, loss=binary_crossentropy_loss, metrics=['accuracy'])

# 모델 학습
model.fit(combined_dataset, epochs=num_epochs)