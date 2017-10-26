#include <Windows.h>

#pragma once

// Templated functions must be defined in the header
template<typename T>
T read_memory(HANDLE process_handle, DWORD64 address) {
	T val;
	ReadProcessMemory(process_handle, (LPCVOID)address, (LPVOID)&val, sizeof(val), NULL);
	return val;
}
template<typename T>

void write_memory(HANDLE proc, LPVOID adr, T val) {
	WriteProcessMemory(proc, adr, &val, sizeof(T), NULL);
}