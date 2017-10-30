#include "FFXIV.h"

#pragma region Mutators
void FFXIV::set_module(MODULEENTRY32 module) {
	this->module = module;
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
BYTE* const& FFXIV::get_base_address() {
	return this->module.modBaseAddr;
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

MODULEENTRY32 const& FFXIV::get_module() {
	return this->module;
}
#pragma endregion
