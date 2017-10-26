#include <Windows.h>

#pragma once
HWND get_hwnd(LPCSTR window_name);
DWORD get_pid(HWND hwnd);
HANDLE get_process_handle(DWORD pid);
DWORD64 get_base_address(HANDLE process_handle);
