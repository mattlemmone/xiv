#include <Windows.h>
#include <tlhelp32.h>
#include <tchar.h>

#pragma once
HWND get_hwnd(std::string window_name);
DWORD get_pid(HWND hwnd);
HANDLE get_process_handle(DWORD pid);
unsigned long long get_base_address(DWORD pid, std::string process_name);