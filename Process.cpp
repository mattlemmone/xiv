#include <iostream>
#include "Process.h"

HWND get_hwnd(std::string window_name) {
	return FindWindowA(NULL, window_name.c_str());
}

DWORD get_pid(HWND hwnd) {
	DWORD pid;
	GetWindowThreadProcessId(hwnd, &pid);
	return pid;
}

HANDLE get_process_handle(DWORD pid) {
	HANDLE process = OpenProcess(
		// memory manip, read, write flags
		PROCESS_VM_READ | PROCESS_VM_WRITE,
		FALSE, // inherit process handle
		pid
	);

	if (process == INVALID_HANDLE_VALUE || !process) {
		printf("Failed to open PID %d, error code %d", pid, GetLastError());
		return NULL;
	}
	return process;
}

unsigned long long get_base_address(DWORD pid, std::string process_name)
{
	unsigned long long newBase = 0;
	HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid);

	MODULEENTRY32 ModuleEntry32;
	ModuleEntry32.dwSize = sizeof(MODULEENTRY32);

	if (hSnapshot == INVALID_HANDLE_VALUE || !(Module32First(hSnapshot, &ModuleEntry32))) {
		CloseHandle(hSnapshot);
		return newBase;
	}

	std::wstring process_name_wide = std::wstring(process_name.begin(), process_name.end());
	do {
		if (!_tccmp(ModuleEntry32.szModule, process_name_wide.c_str()))
		{
			newBase = (unsigned long long) ModuleEntry32.modBaseAddr;
			break;
		}
	} while (Module32Next(hSnapshot, &ModuleEntry32));

	CloseHandle(hSnapshot);
	return newBase;
}
