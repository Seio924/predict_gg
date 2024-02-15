import win32gui
import win32con
import win32api
import ctypes
import threading
import time
import json

class OverlayWindow:
    def __init__(self):
        # 화면의 너비와 높이 가져오기
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)

        # 윈도우 클래스 등록
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = 'OverlayWindow'
        wc.lpfnWndProc = self.window_proc
        self.class_atom = win32gui.RegisterClass(wc)

        # 오버레이 윈도우 생성
        self.hwnd = win32gui.CreateWindow(
            self.class_atom,
            'Overlay Window',
            win32con.WS_POPUP | win32con.WS_EX_LAYERED,  # WS_EX_LAYERED 스타일 추가
            self.screen_width - 200, 10, 180, 70,  # 화면 오른쪽 위에 위치시키기 및 높이 조정
            None, None, wc.hInstance, None
        )

        # 항상 위에 띄우기
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

        # 모서리를 둥글게 만들기
        self.make_rounded_corners()

        # 초기 데이터 설정
        self.blue_percentage = 50
        self.red_percentage = 50
        self.increasing = True  # 파란색 영역이 증가 중인지 여부를 나타내는 플래그

        # 버튼 생성
        self.create_button()

        # 시작 시간 초기화
        self.start_time = 0

        # 움직임 지속 시간 설정 (초 단위)
        self.duration = self.get_match_duration()  # 매치 지속 시간 가져오기

    def make_rounded_corners(self):
        # 둥근 모서리를 가진 리전 생성
        region = win32gui.CreateRoundRectRgn(0, 0, 180, 70, 20, 20)  # 높이 조정
        # 윈도우에 리전 적용
        win32gui.SetWindowRgn(self.hwnd, region, True)

    def create_button(self):
        # 버튼 생성
        self.button_hwnd = win32gui.CreateWindow(
            "BUTTON",
            "시작하기",  # 텍스트 변경
            win32con.WS_VISIBLE | win32con.WS_CHILD,
            20, 9, 140, 50,  # 위치 및 크기 조정
            self.hwnd,
            None,
            win32gui.GetModuleHandle(None),
            None
        )

    def get_match_duration(self):
        # api_match_info.json 파일에서 매치 지속 시간 가져오기
        with open('backend/api_match_info.json', 'r', encoding="utf-8") as f:
            match_info = json.load(f)
            duration = match_info['info']['gameEndTimestamp'] - match_info['info']['gameStartTimestamp']
        return duration / 1000

    def start_update_thread(self):
        # 데이터 업데이트 스레드 시작
        self.update_thread = threading.Thread(target=self.update_data_thread)
        self.update_thread.daemon = True  # 메인 스레드 종료 시 함께 종료
        self.update_thread.start()

    def update_data_thread(self):
        self.start_time = time.time()  # 시작 시간 설정
        while True:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            if elapsed_time < self.duration:
                if self.increasing:
                    # 파란색 영역의 비율 증가
                    self.blue_percentage = min(self.blue_percentage + 1, 100)  # 최대값이 100이 됨
                    self.red_percentage = 100 - self.blue_percentage
                    if self.blue_percentage == 100:
                        self.increasing = False
                else:
                    # 파란색 영역의 비율 감소
                    self.blue_percentage = max(self.blue_percentage - 1, 0)  # 최소값이 0이 됨
                    self.red_percentage = 100 - self.blue_percentage
                    if self.blue_percentage == 0:
                        self.increasing = True
                # UI 업데이트 요청
                win32gui.PostMessage(self.hwnd, win32con.WM_USER + 1, 0, 0)
            else:
                # 움직임 종료 후 재설정
                self.start_time = time.time()  # 시작 시간 재설정
                self.blue_percentage = 50  # 파란색 영역 비율 초기화
                self.red_percentage = 50  # 빨간색 영역 비율 초기화
                self.increasing = True  # 증가 여부 초기화
                # UI 업데이트 요청
                win32gui.PostMessage(self.hwnd, win32con.WM_USER + 1, 0, 0)
            time.sleep(1)  # 1초마다 업데이트

    def window_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_PAINT:
            hdc, ps = win32gui.BeginPaint(hwnd)
            rect = win32gui.GetClientRect(hwnd)
            # 전체 윈도우 크기
            window_width = rect[2]
            window_height = rect[3]

            # 파란색 영역의 폭과 높이 계산
            blue_width = int(window_width * self.blue_percentage / 100)
            blue_height = window_height
            # 빨간색 영역의 폭 계산
            red_width = window_width - blue_width
            red_height = window_height

            # 파란색 영역 그리기
            win32gui.FillRect(hdc, (0, 0, blue_width, blue_height), win32gui.CreateSolidBrush(win32api.RGB(0, 0, 255)))
            # 빨간색 영역 그리기
            win32gui.FillRect(hdc, (blue_width, 0, blue_width + red_width, red_height), win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0)))

            # 텍스트 출력
            blue_text = f"{self.blue_percentage}%"
            red_text = f"{self.red_percentage}%"
            # 파란색 부분에 파란 팀 텍스트 출력
            blue_rect = (0, 0, blue_width, blue_height)
            win32gui.SetBkMode(hdc, win32con.TRANSPARENT)  # 투명 배경 모드 설정
            win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))
            font = win32gui.LOGFONT()
            font.lfHeight = 28
            font.lfWeight = win32con.FW_BOLD
            font.lfFaceName = "Arial"
            hfont = win32gui.CreateFontIndirect(font)
            win32gui.SelectObject(hdc, hfont)
            win32gui.DrawText(hdc, blue_text, -1, blue_rect,
                            win32con.DT_CENTER | win32con.DT_VCENTER | win32con.DT_SINGLELINE)
            # 빨간색 부분에 빨간 팀 텍스트 출력
            red_rect = (blue_width, 0, blue_width + red_width, red_height)
            win32gui.SetBkMode(hdc, win32con.TRANSPARENT)  # 투명 배경 모드 설정
            win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))
            win32gui.DrawText(hdc, red_text, -1, red_rect,
                            win32con.DT_CENTER | win32con.DT_VCENTER | win32con.DT_SINGLELINE)
            
            # 현재 경과 시간 계산
            current_time = int(time.time() - self.start_time)
            # 분과 초로 분리
            minutes = current_time // 60
            seconds = current_time % 60
            # 시간을 문자열로 변환
            time_str = f"{minutes:02}:{seconds:02}"

            # 텍스트를 그릴 위치 계산
            text_rect_width = rect[2]  # 사각형의 너비
            text_rect_height = rect[3]  # 사각형의 높이
            text_width, text_height = win32gui.GetTextExtentPoint32(hdc, time_str)  # 텍스트의 너비와 높이 가져오기
            x = (text_rect_width - text_width) // 2 + 15  # 수평 위치 계산
            y = text_rect_height // 10  # 수직 위치 계산 (사각형의 상단 부분에서 1/4 지점)

            # 텍스트 출력
            win32gui.SetBkMode(hdc, win32con.TRANSPARENT)  # 투명 배경 모드 설정
            win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))
            font.lfHeight = 16  # 글꼴 크기 변경
            hfont = win32gui.CreateFontIndirect(font)
            win32gui.SelectObject(hdc, hfont)
            # 텍스트 출력
            win32gui.DrawText(hdc, time_str, -1, (x, y, x + text_width, y + text_height),
                            win32con.DT_LEFT | win32con.DT_TOP | win32con.DT_SINGLELINE)

            win32gui.EndPaint(hwnd, ps)
            return 0
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        elif msg == win32con.WM_USER + 1:  # 사용자 정의 메시지
            self.update_ui()  # UI 업데이트
            return 0
        elif msg == win32con.WM_COMMAND and win32gui.HIWORD(wparam) == win32con.BN_CLICKED:  # 버튼 클릭 이벤트
            # 버튼이 클릭되었을 때 처리
            win32gui.ShowWindow(self.button_hwnd, win32con.SW_HIDE)  # 버튼 숨기기
            self.start_update_thread()  # 데이터 업데이트 스레드 시작
            return 0
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def update_ui(self):
        # 화면 다시 그리기 요청
        win32gui.InvalidateRect(self.hwnd, None, True)

    def run(self):
        # 오버레이 창 표시
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
        # 메시지 루프 시작
        win32gui.PumpMessages()


def main():
    overlay_window = OverlayWindow()
    overlay_window.run()


if __name__ == "__main__":
    main()
