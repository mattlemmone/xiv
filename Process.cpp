#include <iostream>

#include "Process.h"

HWND get_hwnd(LPCSTR window_name) {
	HWND hwnd = FindWindowA(NULL, window_name);
	return hwnd;
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

DWORD64 get_base_address(HANDLE process_handle)
{
	// str8 ripped cuz nothing else works ;(
	DWORD newBase;

	// get the address of kernel32.dll
	HMODULE k32 = GetModuleHandle(L"kernel32.dll");

	// get the address of GetModuleHandle()
	LPVOID funcAdr = GetProcAddress(k32, "GetModuleHandleA");
	if (!funcAdr)
		funcAdr = GetProcAddress(k32, "GetModuleHandleW");

	// create the thread
	HANDLE thread = CreateRemoteThread(
		process_handle, NULL, NULL, (LPTHREAD_START_ROUTINE)funcAdr, NULL, NULL, NULL
	);

	// let the thread finish
	WaitForSingleObject(thread, INFINITE);

	// get the exit code
	GetExitCodeThread(thread, &newBase);

	// clean up the thread handle
	CloseHandle(thread);

	return newBase;
}
