#pragma once
#include <Windows.h>
#include <string>
#include <vector>
#include "Singleton.h"
#include "FFXIV.h"

struct MemoryRegistryEntry {
	MemoryRegistryEntry(void* variable, BYTE* address, DWORD read_size = 0, bool is_string = false) {
		this->variable = variable;
		this->address = address;
		this->read_size = read_size;
		this->is_string = is_string;
	}
	void* variable;
	BYTE* address;
	DWORD read_size;
	bool is_string;
};

class MemoryRegistry : public Singleton<MemoryRegistry> {
public:
	void add(void* variable, BYTE* address, DWORD read_size = 0, bool is_string = false);
	void scan();
	~MemoryRegistry();
private:
	const int POLL_RATE = 500;
	std::vector<MemoryRegistryEntry*> registry;
};

std::string read_address_string(HANDLE process_handle, BYTE* address, DWORD read_size);

// Templated functions must be defined in the header
template<typename T>
T read_address(HANDLE process_handle, BYTE* address) {
	T val;
	DWORD size = sizeof(T);
	ReadProcessMemory(process_handle, (LPCVOID) address, (LPVOID)&val, size, NULL);
	return val;
}


//template<typename T>
//void write_memory(HANDLE proc, LPVOID adr, T val) {
//	WriteProcessMemory(proc, adr, &val, sizeof(T), NULL);
//}
//
template <typename T>
T read_address_pointers(HANDLE process_handle, BYTE* base_address, const std::vector<DWORD> &offsets) {
	// Read initial address
	BYTE* address = base_address + offsets[0];
	T val = read_address<BYTE*>(process_handle, address);

	// Read the chain of pointers
	for (size_t i = 1; i < offsets.size(); ++i) {
		if (i < offsets.size() - 1)
			val = read_address<BYTE*>(process_handle, val + offsets[i]);
		else
			val = read_address<T>(process_handle, val + offsets[i]);
	}
	
	return val;
}

//template<typename T>
//DWORD protectMemory(HANDLE proc, unsigned long long adr, unsigned long long adr_size, DWORD prot) {
//	DWORD oldProt;
//	VirtualProtectEx(proc, (LPVOID)adr, adr_size, prot, &oldProt);
//	return oldProt;
//}