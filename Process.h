#include <Windows.h>
#include <tlhelp32.h>
#include <Psapi.h>
#include <tchar.h>

#pragma once
HWND get_hwnd(std::string window_name);
DWORD get_pid(HWND hwnd);
HANDLE get_process_handle(DWORD pid);
MODULEENTRY32 get_module(DWORD pid, std::string process_name);


//unsigned long long find_pattern(char* module_name, char *pattern, char *mask) {
//	MODULEINFO mod_info = get_module_info(module_name);
//	unsigned long long base = (unsigned long long) mod_info.lpBaseOfDll;
//	unsigned long long size = (unsigned long long) mod_info.SizeOfImage;
//	unsigned long long pattern_length = (unsigned long long) strlen(mask);
//
//	for (unsigned long long i = 0; i < size - pattern_length; ++i) {
//		bool found = true;
//		for (unsigned long long j = 0; j < pattern_length; ++j) {
//			found &= mask[j] == '?' || pattern[j] == *(char*)(base + i + j);
//		}
//		if (found)
//			return base + i;
//	}
//
//	return 0;
//}

