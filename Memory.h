#include <Windows.h>

#pragma once

// Templated functions must be defined in the header
template<typename T>
T read_address(HANDLE process_handle, long long address) {
	T val;
	ReadProcessMemory(process_handle, (LPCVOID)address, (LPVOID)&val, sizeof(val), NULL);
	return val;
}

template<typename T>
void write_memory(HANDLE proc, LPVOID adr, T val) {
	WriteProcessMemory(proc, adr, &val, sizeof(T), NULL);
}

template <typename T>
T read_address_pointers(HANDLE process_handle, long long base_address, const std::vector<long long> &offsets) {
	// Read initial address
	long long address = base_address + offsets[0];
	T val = read_address<T>(process_handle, address);

	// Read the chain of pointers
	for (size_t i = 1; i < offsets.size(); ++i) {
		val = read_address<T>(process_handle, val);
	}
	return val;
}