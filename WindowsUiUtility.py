import cv2
import win32gui
import numpy as np
from SwRuneFarmerProject.MouseLibrary import mouse
from ctypes import windll
from PIL import ImageGrab

_windowsList = []
_topList = []
_windowXCoordinateOffset = 0
_windowYCoordinateOffset = 0

# Make program aware of DPI scaling
user32 = windll.user32
user32.SetProcessDPIAware()


def enum_win(hwnd, result):
    win_text = win32gui.GetWindowText(hwnd)
    _windowsList.append((hwnd, win_text))


def GetWindowHandleByWindowTitle(searchedWindowTitle):
    win32gui.EnumWindows(enum_win, _topList)
    for (hwnd, win_text) in _windowsList:
        if searchedWindowTitle in win_text:
            return hwnd


def GetScreenShotFromWindow(windowHwnd):
    position = win32gui.GetWindowRect(windowHwnd)
    __setWindowCoordinateOffset(position)
    # Take screenshot
    screenshot = ImageGrab.grab(position)
    screenshot = np.array(screenshot)
    return cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)


def __setWindowCoordinateOffset(windowPosition):
    global _windowXCoordinateOffset
    _windowXCoordinateOffset = windowPosition[0]
    global _windowYCoordinateOffset
    _windowYCoordinateOffset = windowPosition[1]


def SetCursorPosition(x, y):
    try:
        mouse.move(x + _windowXCoordinateOffset, y + _windowYCoordinateOffset)
    except Exception as e:
        print(e.__doc__)
        print("Error in SetCursorPosition(", x, ", ", y, ")")


def DoLeftClick():
    mouse.click()
