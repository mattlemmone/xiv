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
		PROCESS_ALL_ACCESS,
		FALSE, // inherit process handle
		pid
	);

	if (process == INVALID_HANDLE_VALUE || !process) {
		printf("Failed to open PID %d, error code %d", pid, GetLastError());
		return NULL;
	}
	return process;
}

MODULEENTRY32 get_module(DWORD pid, std::string process_name)
{

	MODULEENTRY32 ModuleEntry32;
	ModuleEntry32.dwSize = sizeof(MODULEENTRY32);
	HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, pid);


	if (hSnapshot == INVALID_HANDLE_VALUE || !(Module32First(hSnapshot, &ModuleEntry32))) {
		CloseHandle(hSnapshot);
		return ModuleEntry32;
	}


	do {
		if (!_tccmp(ModuleEntry32.szModule, process_name.c_str()))
		{
			return ModuleEntry32;
			break;
		}
	} while (Module32Next(hSnapshot, &ModuleEntry32));

	CloseHandle(hSnapshot);
	return ModuleEntry32;
}
