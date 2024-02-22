import math
import cv2
import numpy as np
import pytesseract
import mss
import win32gui 
import win32con
import win32api
import time
import threading
import json

OVERLAY_WIDTH = 350
OVERLAY_HEIGHT = 125

def get_match_duration():
    # api_match_info.json 파일에서 매치 지속 시간 가져오기
    with open('backend/api_match_info.json', 'r', encoding="utf-8") as f:
        match_info = json.load(f)
        duration = match_info['info']['gameEndTimestamp'] - match_info['info']['gameStartTimestamp']
    return duration

def get_text_file():
    with open('src/predict_data.txt', 'r', encoding="utf-8") as f:
        # 예측 승률 리스트로 변환
        lines = f.readlines()
        predict_data = [eval(line.strip()) for line in lines]
        print(predict_data)
    return predict_data

with open('backend/userInput.txt', 'r', encoding="utf-8") as f:
    time_num = f.read().strip()

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
m = get_match_duration() // 60000
s = int((get_match_duration() % 60000) / 1000)
print(m, s)
sleep_num = 0.3
cnt = 0
predict_txt = ""

increasing = True
blue_percentage = 100

predict_list = get_text_file()
time_num = int(time_num)

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

# 오버레이 윈도우를 생성하는 함수
def create_overlay():
    # 윈도우 클래스 등록
    wc = win32gui.WNDCLASS()
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.lpszClassName = 'OverlayWindowClass'
    wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = win32gui.CreateSolidBrush(win32api.RGB(0, 0, 255))  # 파란색 배경 생성
    wc.lpfnWndProc = {
        win32con.WM_PAINT: on_paint,
    }

    # 윈도우 등록
    wnd_class_atom = win32gui.RegisterClass(wc)

    # 윈도우 생성
    hwnd = win32gui.CreateWindow(
        wnd_class_atom,
        'Overlay Window',
        win32con.WS_POPUP | win32con.WS_VISIBLE,
        20,
        10,
        OVERLAY_WIDTH,
        OVERLAY_HEIGHT,
        0,
        0,
        win32api.GetModuleHandle(None),
        None
    )

    # 항상 위에 표시
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                           win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

    # 모서리를 둥글게 만들기
    region = win32gui.CreateRoundRectRgn(0, 0, OVERLAY_WIDTH, OVERLAY_HEIGHT, 20, 20)
    win32gui.SetWindowRgn(hwnd, region, True)

    return hwnd

# 오버레이에 배경을 그리는 함수
def draw_background(hwnd, hdc, text):
    global increasing, blue_percentage

    rect = (0, 0, OVERLAY_WIDTH, OVERLAY_HEIGHT)  # 전체 윈도우 크기

    if increasing:
        blue_percentage += 2
    else:
        blue_percentage -= 2

    background_rect = (rect[0], rect[1], rect[2], rect[3])

    bar_rect = (rect[0] + 20, rect[1] + OVERLAY_HEIGHT-50 , rect[2] - 20, rect[3] -45)
    

    # 파랑색 영역 계산
    blue_width = blue_percentage
    blue_rect = (bar_rect[0], bar_rect[1], bar_rect[0] + blue_width, bar_rect[3])


    # 빨강색 영역 계산
    red_width = rect[2] - blue_width  # 전체 가로 길이에서 파란색 영역의 너비를 뺀 값
    red_rect = (blue_rect[2], bar_rect[1], bar_rect[2], bar_rect[3])

    win32gui.FillRect(hdc, background_rect, win32gui.CreateSolidBrush(win32api.RGB(50, 53, 57)))

    # 파랑색 영역 채우기
    win32gui.FillRect(hdc, blue_rect, win32gui.CreateSolidBrush(win32api.RGB(94, 130, 255)))  # 파랑색 배경 채우기

    # 빨강색 영역 채우기
    win32gui.FillRect(hdc, red_rect, win32gui.CreateSolidBrush(win32api.RGB(214, 78, 91)))  # 빨강색 배경 채우기

    if blue_percentage == OVERLAY_WIDTH:
        increasing = False
    elif blue_percentage == 0:
        increasing = True


# 오버레이에 텍스트를 그리는 함수
def on_paint(hwnd, msg, wparam, lparam):
    global text_tmp, predict_txt  # text_tmp를 전역 변수로 선언
    
    hdc, ps = win32gui.BeginPaint(hwnd)

    

    # 텍스트 출력에 사용할 HDC 생성
    hdc = win32gui.GetDC(None)

    # 배경 그리기
    draw_background(hwnd, hdc, text_tmp)
    
    # 텍스트 그리기
    rect_text = (20, 20, OVERLAY_WIDTH-20, OVERLAY_HEIGHT-20)  # 텍스트가 출력될 영역

    win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))  # 텍스트 색상 설정 (흰색)
    win32gui.SetBkMode(hdc, win32con.TRANSPARENT)  # 배경 투명으로 설정
    win32gui.DrawText(hdc, text_tmp, -1, rect_text, win32con.DT_CENTER | win32con.DT_VCENTER | win32con.DT_SINGLELINE)  # 텍스트 출력 위치 및 스타일 설정
    
    
    # BLUE와 RED 텍스트 출력
    blue_text = "BLUE"
    red_text = "RED"

    win32gui.DrawText(hdc, blue_text, -1, rect_text, win32con.DT_LEFT | win32con.DT_VCENTER | win32con.DT_SINGLELINE)  # 텍스트 출력 위치 및 스타일 설정
    win32gui.DrawText(hdc, red_text, -1, rect_text, win32con.DT_RIGHT | win32con.DT_VCENTER | win32con.DT_SINGLELINE)  # 텍스트 출력 위치 및 스타일 설정
    
    win32gui.EndPaint(hwnd, ps)
    
    return 0   # 반환 값으로 0을 사용하여 정상적으로 처리되었음을 나타냄

# 캡처 및 텍스트 추출을 수행하는 함수
def capture_and_extract(hwnd):
    global text_tmp, m, s, cnt, predict_list, predict_txt, time_num

    while True:
        # 화면 캡처
        screen = capture_screen(ROI)

        # 텍스트 추출
        text = extract_text(screen)

        if (len(text) == 5 and text[2] == ":" and text[0].isdigit() and text[1].isdigit() and text[3].isdigit() and text[4].isdigit()):
            check_min = int(text[0:2]); check_sec = int(text[3:])
            if check_min >= m and check_sec >= s:
                cnt += 1
                if cnt >= 2:
                    continue
                # 만약에 93:40일때 앞에 시간 더해서 text에 넣어주기
                min = int(text_tmp[0:2]); sec = int(text_tmp[3:]) # 바로 앞 추출텍스트
            
                #sleep_num 만큼 더한다.
                sec += math.ceil(sleep_num)
                if sec >= 60:
                    sec_tmp = sec % 60
                    sec_to_min = sec // 60
                
                    min += sec_to_min; sec = sec_tmp

                # 더한 시간이 플레이타임보다 크다면
                if min >= m and sec >= s:
                    min = m; sec = s

                str_min = str(min); str_sec = str(sec)
                

                if len(str_min) < 2:
                    str_min = "0" + str_min
                
                if len(str_sec) < 2:
                    str_sec = "0" + str_sec

                text = str_min + ":" + str_sec
                text_tmp = text

                predict_txt = str(predict_list[(min*60+sec)//time_num][1]) + "% :" + str(predict_list[(min*60+sec)//time_num][2]) + "%"

                print(min*60+sec)

                
            
            else:
                text_tmp = text
                predict_txt = str(predict_list[(int(text_tmp[0:2])*60+int(text_tmp[3:]))//time_num][1]) + "% :" + str(predict_list[(int(text_tmp[0:2])*60+int(text_tmp[3:]))//time_num][2]) + "%"
                print(int(text_tmp[0:2])*60+int(text_tmp[3:]))
                cnt = 0
        else:
            cnt += 1
            if cnt >= 2:
                continue

            min = int(text_tmp[0:2]); sec = int(text_tmp[3:]) # 바로 앞 추출텍스트
            
            # 프로그램 시작 후 이전의 텍스트가 00:00 일때 즉 아직 리플레이 속 시간 인식을 시작하지 않았을 때 00:00 유지 (파/빨 비율도 1:1)
            if min == 0 and sec == 0:
                text = text_tmp
                text_tmp = text
                predict_txt = str(predict_list[(min*60+sec)//time_num][1]) + "% :" + str(predict_list[(min*60+sec)//time_num][2]) + "%"
                print(min*60+sec)
                continue

            #sleep_num 만큼 더한다.
            sec += math.ceil(sleep_num)
            if sec >= 60:
                sec_tmp = sec % 60
                sec_to_min = sec // 60
            
                min += sec_to_min; sec = sec_tmp

            # 더한 시간이 플레이타임보다 크다면
            if min >= m and sec >= s:
                min = m; sec = s

            str_min = str(min); str_sec = str(sec)

            if len(str_min) < 2:
                str_min = "0" + str_min
            
            if len(str_sec) < 2:
                str_sec = "0" + str_sec

            text = str_min + ":" + str_sec
            text_tmp = text
            predict_txt = str(predict_list[(min*60+sec)//time_num][1]) + "% :" + str(predict_list[(min*60+sec)//time_num][2]) + "%"
            print(min*60+sec)

        

        # 텍스트를 오버레이에 출력
        win32gui.InvalidateRect(hwnd, None, True)
        win32gui.UpdateWindow(hwnd)

        time.sleep(sleep_num)

if __name__ == '__main__':
    overlay_hwnd = create_overlay()
    
    # 캡처 및 텍스트 추출을 별도의 스레드에서 실행
    capture_thread = threading.Thread(target=capture_and_extract, args=(overlay_hwnd,))
    capture_thread.daemon = True
    capture_thread.start()
    
    # 메시지 루프 실행
    win32gui.PumpMessages()