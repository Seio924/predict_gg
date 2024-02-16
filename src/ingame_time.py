import cv2
import numpy as np
import pytesseract
import mss
import win32api
import win32con
import time

# Tesseract OCR 엔진의 경로를 설정합니다. 본인의 컴퓨터에 맞게 수정하세요.
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# 윈도우의 중간 좌표 계산
screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
middle_x = screen_width // 2

# 관심 영역 크기 설정
roi_width = 50
roi_height = 50

# 관심 영역 좌표 설정
x = middle_x - (roi_width // 2) + 198
y = 49  # 원하는 위치로 수정하세요
w = roi_width
h = roi_height

# 관심 영역의 좌표 (x, y, width, height)
ROI = (x, y, w, h)

text_tmp = "00:00"
# 실제 플레이 타임
m = 23; s = 43

# 화면 캡처 함수 (관심 영역만 캡처)
def capture_screen(roi):
    with mss.mss() as sct:
        # 화면 캡처
        img = np.array(sct.grab({"left": x, "top": y, "width": w, "height": h}))

        # 이미지를 그레이스케일로 변환합니다.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return gray

# OCR을 수행하여 텍스트를 추출하는 함수
def extract_text(image):
    # 이미지에서 텍스트를 추출합니다.
    text = pytesseract.image_to_string(image)
    text = text.rstrip()
    return text

# 메인 함수
def main():
    global text_tmp, m, s

    # 93:40 인 경우 신경쓰기 또는 실제 플레이타임보다 큰 시간 나오면 처리하기
    sleep_num = 2
    while True:
        # 화면 캡처
        screen = capture_screen(ROI)

        # 텍스트 추출
        text = extract_text(screen)
        
        if len(text) == 5 and text[2] == ":":
            check_min = int(text[0:2]); check_sec = int(text[3:])
            if check_min >= m and check_sec > s:
                # 만약에 93:40일때 앞에 시간 더해서 text에 넣어주기
                min = int(text_tmp[0:2]); sec = int(text_tmp[3:]) # 바로 앞 추출텍스트
            
                #sleep_num 만큼 더한다.
                sec += 3
                if sec >= 60:
                    sec_tmp = sec % 60
                    sec_to_min = sec // 60
                
                    min += sec_to_min; sec = sec_tmp

                # 더한 시간이 플레이타임보다 크다면
                if min >= m and sec > s:
                    min = m; sec = s

                str_min = str(min); str_sec = str(sec)

                if len(str_min) < 2:
                    str_min = "0" + str_min
                
                if len(str_sec) < 2:
                    str_sec = "0" + str_sec

                text = str_min + ":" + str_sec
            
            # 추출된 텍스트 출력
            print("추출된 텍스트:", text)
            text_tmp = text
        else:
            min = int(text_tmp[0:2]); sec = int(text_tmp[3:]) # 바로 앞 추출텍스트
            
            #sleep_num 만큼 더한다.
            sec += 3
            if sec >= 60:
                sec_tmp = sec % 60
                sec_to_min = sec // 60
            
                min += sec_to_min; sec = sec_tmp

            # 더한 시간이 플레이타임보다 크다면
            if min >= m and sec > s:
                min = m; sec = s

            str_min = str(min); str_sec = str(sec)

            if len(str_min) < 2:
                str_min = "0" + str_min
            
            if len(str_sec) < 2:
                str_sec = "0" + str_sec

            text = str_min + ":" + str_sec
            print("수정된 텍스트:", text)
            text_tmp = text

        # 1초 대기
        time.sleep(sleep_num)

        # 'q'를 누르면 종료합니다.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
