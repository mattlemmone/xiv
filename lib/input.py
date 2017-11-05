from munch import Munch
from string import ascii_lowercase
from win32api import SendMessage
from win32con import MK_RBUTTON
from win32con import WM_KEYDOWN
from win32con import WM_KEYUP
from win32con import WM_MOUSEMOVE
from win32con import WM_RBUTTONDOWN
from win32con import WM_RBUTTONUP
import time

from lib import application

KEY_MAP = Munch(
    tab=0x09
)

# Map 0-9
for num in xrange(10):
    KEY_MAP[str(num)] = 0x30 + num

# Map a-z
for idx, char in enumerate(ascii_lowercase):
    KEY_MAP[char] = 0x41 + idx

# F1 - F24
for num in xrange(25):
    KEY_MAP['f%d' % (num + 1)] = 0x70 + num


class MouseInput(object):
    @staticmethod
    def click():
        hwnd = _get_hwnd()
        SendMessage(hwnd, WM_RBUTTONDOWN, MK_RBUTTON, 0)
        x, y = 200, 200
        for _ in xrange(10):
            lparam = y << 16 | x
            x += 200
            y += 200
            SendMessage(hwnd, WM_MOUSEMOVE, MK_RBUTTON, lparam)
        SendMessage(hwnd, WM_RBUTTONUP, MK_RBUTTON, 0)


class KeyboardInput(object):
    @staticmethod
    def key_press(key, delay=300):
        key_code = KEY_MAP.get(key.lower())
        hwnd = _get_hwnd()

        SendMessage(hwnd,  WM_KEYDOWN, key_code,  0)
        time.sleep(delay / 1000)
        SendMessage(hwnd,  WM_KEYUP, key_code, 0)

    @staticmethod
    def key_down(key):
        key_code = KEY_MAP.get(key.lower())
        hwnd = _get_hwnd()
        SendMessage(hwnd,  WM_KEYDOWN, key_code,  0)

    @staticmethod
    def key_up(key):
        key_code = KEY_MAP.get(key.lower())
        hwnd = _get_hwnd()
        SendMessage(hwnd,  WM_KEYUP, key_code,  0)


def _get_hwnd():
    hwnd = application.hwnd
    assert hwnd, 'HWND not found'
    return hwnd
