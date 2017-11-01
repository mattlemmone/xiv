from ctypes import windll
from ctypes.wintypes import addressof
from ctypes.wintypes import BYTE
from ctypes.wintypes import c_char
from ctypes.wintypes import DWORD
from ctypes.wintypes import HMODULE
from ctypes.wintypes import POINTER
from ctypes.wintypes import pointer
from ctypes.wintypes import sizeof
from ctypes.wintypes import Structure
import psutil
import win32api
import win32con
import win32gui

# Module specific
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
TH32CS_SNAPMODULE = 0x00000008

CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
Module32First = windll.kernel32.Module32First
Module32Next = windll.kernel32.Module32Next
GetLastError = windll.kernel32.GetLastError
CloseHandle = windll.kernel32.CloseHandle
hModuleSnap = DWORD


class MODULEENTRY32(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('th32ModuleID', DWORD),
        ('th32ProcessID', DWORD),
        ('GlblcntUsage', DWORD),
        ('ProccntUsage', DWORD),
        ('modBaseAddr', POINTER(BYTE)),
        ('modBaseSize', DWORD),
        ('hModule', HMODULE),
        ('szModule', c_char * 256),
        ('szExePath', c_char * 260)
    ]


def get_hwnd(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    assert hwnd, 'Failed to get HWND'
    return hwnd


def get_pid(process_name):
    pid = next(
        item for item in psutil.process_iter()
        if item.name() == process_name
    ).pid
    assert pid, 'Failed to get PID'
    return pid


def get_handle(pid):
    handle = win32api.OpenProcess(
        win32con.PROCESS_ALL_ACCESS,
        False,
        pid
    )
    assert handle, 'Failed to get HANDLE'
    return handle


def get_base_address(pid):
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)
    snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid)
    next_module = Module32First(snapshot, pointer(me32))

    while next_module and me32.th32ProcessID != pid:
        print me32.th32ProcessID
        print me32.szExePath
        next_module = Module32Next(
            snapshot, pointer(me32)
        )

    CloseHandle(snapshot)

    # Convert base address from LP_c_byte to long
    return addressof(me32.modBaseAddr.contents)

