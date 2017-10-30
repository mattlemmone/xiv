#pragma once
#include <Windows.h>
#include <vector>

template<typename T>
struct Pointer {
	Pointer(std::vector<DWORD> offsets) {
		this->offsets = offsets;
	}

	std::vector<DWORD> offsets;
	BYTE* address;
};


static Pointer<BYTE*>* player_base = new Pointer<BYTE*>(
	{ 0x01802E50}
);


