import tensorflow as tf
import numpy as np
from load_data import LoadData
from transformer_model import MultiHeadAttention

LIST_LEN = 88

api_key = 'RGAPI-849c1324-5898-415b-b34e-2066bb9e8c80'

def create_padding_mask(data):
    # 입력 시퀀스에서 0인 부분을 찾아내는 마스크 생성
    mask = 1 - tf.cast(tf.reduce_all(tf.math.equal(data, 0), axis=-1), tf.float32)
    # 패딩된 부분을 1로, 그렇지 않은 부분을 0으로 변경
    mask = tf.expand_dims(mask, axis=-1)  # 마스크 차원 확장
    return mask  # 3차원으로 확장된 마스크를 LIST_LEN만큼 복제하여 모든 특성에 대해 적용

def padded_binary_crossentropy(y_true, y_pred):
    # 패딩된 부분의 가중치를 0으로 설정
    mask = tf.cast(tf.reduce_all(tf.math.equal(y_true, 0), axis=-1), tf.float32)
    weights = 1 - mask
    
    # 손실 계산
    loss = tf.keras.losses.binary_crossentropy(y_true, y_pred)
    
    # 패딩된 부분의 손실을 0으로 설정
    loss *= weights
    
    return loss


load_instance = LoadData(api_key)

# 데이터 가져오기
train_data, win_lose_list = load_instance.get_diamond1_data_list(200)


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


padding_mask = create_padding_mask(padded_data)

print(padded_data.shape)
print(padding_mask.shape)

# win_lose_list를 넘파이 배열로 변환
win_lose_array = np.array(win_lose_list)

# 시간 단계별로 각 특성의 평균과 표준편차 계산
mean_values = np.mean(padded_data, axis=(0, 1))
std_values = np.std(padded_data, axis=(0, 1))

# 데이터 정규화
normalized_data = (padded_data - mean_values) / std_values

# LSTM 모델 정의
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(units=100, input_shape=(max_length_data, LIST_LEN)),
    tf.keras.layers.Dense(units=64, activation='relu'),  # 추가된 Dense 레이어
    tf.keras.layers.Dense(units=2, activation='softmax')  # 출력 레이어
])

# 사용자 정의 손실 함수 등록
tf.keras.utils.get_custom_objects()['padded_binary_crossentropy'] = padded_binary_crossentropy

# 모델 컴파일
model.compile(optimizer='adam', loss='padded_binary_crossentropy', metrics=['accuracy'])

# 모델 훈련
model.fit(normalized_data, win_lose_array, epochs=100, batch_size=32, sample_weight=padding_mask)