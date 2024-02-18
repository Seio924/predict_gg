import tensorflow as tf
import numpy as np
from load_data import LoadData
from transformer_model import MultiHeadAttention


class CustomGRU(tf.keras.layers.Layer):
    def __init__(self, units):
        super(CustomGRU, self).__init__()
        self.units = units
        self.update_gate = tf.keras.layers.Dense(units, activation='sigmoid')
        self.reset_gate = tf.keras.layers.Dense(units, activation='sigmoid')
        self.new_state = tf.keras.layers.Dense(units, activation='tanh')
        
        # RNN 셀의 상태 크기를 정의
        self.state_size = units  # GRU 셀은 하나의 상태 크기를 가짐

    def call(self, inputs, states):
        prev_hidden_state = states[0]
        
        # 현재 입력과 이전의 히든 상태를 결합하여 업데이트 게이트와 리셋 게이트를 계산
        update = self.update_gate(tf.concat([inputs, prev_hidden_state], axis=-1))
        reset = self.reset_gate(tf.concat([inputs, prev_hidden_state], axis=-1))
        
        # 업데이트 게이트와 리셋 게이트를 사용하여 현재 상태를 업데이트
        new_state = reset * prev_hidden_state
        new_state = new_state + (1 - reset) * self.new_state(tf.concat([inputs, new_state], axis=-1))
        updated_state = update * prev_hidden_state + (1 - update) * new_state
        
        return updated_state, [updated_state]


if __name__ == "__main__":

    LIST_LEN = 88

    api_key = 'RGAPI-6d3dda9d-b317-4db1-88ed-340d31cad6d4'

    def create_padding_mask(data):
        # 입력 시퀀스에서 0인 부분을 찾아내는 마스크 생성
        mask = 1 - tf.cast(tf.reduce_all(tf.math.equal(data, 0), axis=-1), tf.float32)
        # 패딩된 부분을 1로, 그렇지 않은 부분을 0으로 변경
        mask = tf.expand_dims(mask, axis=-1)  # 마스크 차원 확장
        return mask  # 3차원으로 확장된 마스크를 LIST_LEN만큼 복제하여 모든 특성에 대해 적용



    load_instance = LoadData(api_key)

    # 데이터 가져오기
    train_data, win_lose_list = load_instance.get_diamond1_data_list(100)


    # 시계열 데이터의 최대 길이 계산
    max_length_data = 301
    max_length_target = 301

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

    # 시간 단계별로 각 특성의 평균과 표준편차 계산
    mean_values = np.mean(padded_data[:, :, 1:], axis=(0, 1))  # 타임스탬프를 제외한 특성의 평균
    std_values = np.std(padded_data[:, :, 1:], axis=(0, 1))    # 타임스탬프를 제외한 특성의 표준편차

    # 데이터 정규화
    normalized_data = padded_data.copy()  # 원본 데이터를 복사하여 정규화된 데이터를 저장할 배열 생성
    normalized_data[:, :, 1:] = (padded_data[:, :, 1:] - mean_values) / std_values  # 타임스탬프를 제외한 특성을 정규화

    # 입력 데이터의 형태: (batch_size, time_steps, features)
    # 현재의 히든 상태의 형태: (batch_size, units)
    # 각 데이터 샘플에서의 이전의 히든 상태의 초기값: (batch_size, units)

    # 모델 정의
    units = LIST_LEN  # 히든 상태의 크기
    input_shape = (max_length_data, LIST_LEN)  # 입력 데이터의 크기
    batch_size = None  # 배치 크기

    # 입력 레이어
    inputs = tf.keras.layers.Input(shape=input_shape)

    # GRU 레이어
    gru_layer = CustomGRU(units)
    initial_state = tf.zeros_like(inputs[:, 0])
    print(initial_state.shape)
    #initial_state = tf.zeros((batch_size, LIST_LEN))  # 초기 상태의 형태를 변경함
    outputs, _ = tf.keras.layers.RNN(gru_layer, return_sequences=True, return_state=True)(inputs, initial_state=initial_state)

    # 출력 레이어
    outputs = tf.keras.layers.Dense(2, activation='softmax')(outputs)

    # 모델 생성
    model = tf.keras.Model(inputs=inputs, outputs=outputs)

    # 모델 컴파일
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'], weighted_metrics=[])

    # 모델 학습
    model.fit(normalized_data, padded_data2, batch_size=batch_size, epochs=10, validation_split=0.2, sample_weight=padding_mask)

    # 모델 요약
    #model.summary()
    model.save('backend/modelGRU')

    pass