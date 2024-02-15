import tkinter as tk
import win32gui
import win32con
import win32api
import ctypes
import threading
import time

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
            win32con.WS_POPUP,
            self.screen_width - 200, 10, 180, 70,  # 화면 오른쪽 위에 위치시키기
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

        # 데이터 업데이트 스레드 시작
        self.update_thread = threading.Thread(target=self.update_data_thread)
        self.update_thread.daemon = True  # 메인 스레드 종료 시 함께 종료
        self.update_thread.start()

    def make_rounded_corners(self):
        # 둥근 모서리를 가진 리전 생성
        region = win32gui.CreateRoundRectRgn(0, 0, 180, 70, 20, 20)
        # 윈도우에 리전 적용
        win32gui.SetWindowRgn(self.hwnd, region, True)

    def update_data_thread(self):
        while True:
            # 실시간 데이터 업데이트 (임의의 작업)
            self.blue_percentage = (self.blue_percentage + 1) % 101
            self.red_percentage = 100 - self.blue_percentage
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
            red_text = f"{100 - self.blue_percentage}%"
            # 파란색 부분에 파란 팀 텍스트 출력
            blue_rect = (0, 0, blue_width, blue_height)
            win32gui.FillRect(hdc, blue_rect, win32gui.CreateSolidBrush(win32api.RGB(0, 0, 255)))
            win32gui.SetBkColor(hdc, win32api.RGB(0, 0, 255))
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
            win32gui.FillRect(hdc, red_rect, win32gui.CreateSolidBrush(win32api.RGB(255, 0, 0)))
            win32gui.SetBkColor(hdc, win32api.RGB(255, 0, 0))
            win32gui.SetTextColor(hdc, win32api.RGB(255, 255, 255))
            win32gui.DrawText(hdc, red_text, -1, red_rect,
                            win32con.DT_CENTER | win32con.DT_VCENTER | win32con.DT_SINGLELINE)

            win32gui.EndPaint(hwnd, ps)
            return 0
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        elif msg == win32con.WM_USER + 1:  # 사용자 정의 메시지
            self.update_ui()  # UI 업데이트
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


def start_overlay_window():
    overlay_window = OverlayWindow()
    overlay_window.run()


def main():
    # Tkinter 윈도우 생성
    root = tk.Tk()
    root.title("Overlay Window Controller")

    # 시작하기 버튼 생성
    start_button = tk.Button(root, text="시작하기", command=start_overlay_window)
    start_button.pack()

    # Tkinter 이벤트 루프 시작
    root.mainloop()


if __name__ == "__main__":
    main()

