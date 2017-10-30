#include "Memory.h"

std::string read_address_string(HANDLE process_handle, BYTE* address, DWORD read_size) {
	char val[64];
	ReadProcessMemory(process_handle, (LPCVOID)address, (LPVOID)&val, read_size, NULL);
	return std::string(val);
}

void* read_address_by_size(HANDLE process_handle, BYTE* address, DWORD read_size) {
	void * val;
	ReadProcessMemory(process_handle, (LPCVOID)address, (LPVOID)&val, read_size, NULL);
	return val;
}


MemoryRegistry::~MemoryRegistry() {
	for (auto entry : this->registry)
		delete entry;	
}

void MemoryRegistry::add(void* variable, BYTE* address, DWORD read_size, bool is_string){
	MemoryRegistryEntry *entry = new MemoryRegistryEntry(variable, address, read_size, is_string);
	this->registry.push_back(entry);
}

void MemoryRegistry::scan() {
	FFXIV *ffxiv = FFXIV::instance();
	HANDLE handle = ffxiv->get_handle();

	for (auto entry : this->registry) {
		void* test = read_address_by_size(handle, entry->address, 0x04);
		float crap = *(float *)&test;
		printf("");
		//entry->variable = read_address(handle, entry->address);
	}
	Sleep(this->POLL_RATE);
}

