#include "FFXIV.h"

FFXIV *FFXIV::p_instance = NULL;

FFXIV* FFXIV::instance() {
	if (!p_instance)
		p_instance = new FFXIV;
	return p_instance;
}

#pragma region Mutators
void FFXIV::set_base_address(DWORD64 base_address) {
	this->base_address = base_address;
}

void FFXIV::set_handle(HANDLE handle) {
	this->handle = handle;
}

void FFXIV::set_pid(DWORD pid) {
	this->pid = pid;
}

void FFXIV::set_hwnd(HWND hwnd) {
	this->hwnd = hwnd;
}
#pragma endregion

#pragma region Accessors
unsigned long long const& FFXIV::get_base_address() {
	return this->base_address;
}

HANDLE const& FFXIV::get_handle() {
	return this->handle;
}

DWORD const& FFXIV::get_pid() {
	return this->pid;
}

HWND const& FFXIV::get_hwnd() {
	return this->hwnd;
}
#pragma endregion
