#pragma once
#include <Windows.h>
#include <tlhelp32.h>
#include <Psapi.h>
#include <tchar.h>

HWND get_hwnd(std::string window_name);
DWORD get_pid(HWND hwnd);
HANDLE get_process_handle(DWORD pid);
MODULEENTRY32 get_module(DWORD pid, std::string process_name);


