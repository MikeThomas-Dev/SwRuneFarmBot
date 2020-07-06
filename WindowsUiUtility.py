import time
import cv2
import win32gui
import win32api
import win32con
import numpy as np
from ctypes import windll
from PIL import ImageGrab

windowsList = []
topList = []

# Make program aware of DPI scaling
user32 = windll.user32
user32.SetProcessDPIAware()


def enum_win(hwnd, result):
    win_text = win32gui.GetWindowText(hwnd)
    windowsList.append((hwnd, win_text))


def GetWindowHandleByWindowTitle(searchedWindowTitle):
    win32gui.EnumWindows(enum_win, topList)
    for (hwnd, win_text) in windowsList:
        if searchedWindowTitle in win_text:
            return hwnd


def GetScreenShotFromWindow(windowHwnd):
    position = win32gui.GetWindowRect(windowHwnd)
    # Take screenshot
    screenshot = ImageGrab.grab(position)
    screenshot = np.array(screenshot)
    return cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)


def SetCursorPosition(x, y):
    try:
        win32api.SetCursorPos((x, y))
    except:
        print("Error in SetCursorPosition(", x, ", ", y, ")")


def DoLeftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
