#include <string>
#include <Windows.h>
#include <tlhelp32.h>
#include <Psapi.h>

#pragma once
class FFXIV {

public:

	// Get singleton
	static FFXIV *instance();

	// Setters
	void set_handle(HANDLE handle);
	void set_pid(DWORD pid);
	void set_hwnd(HWND hwnd);
	void set_module(MODULEENTRY32 module);

	// Getters
	BYTE* const& get_base_address();
	MODULEENTRY32 const& get_module();
	HANDLE const& get_handle();
	DWORD const& get_pid();
	HWND const& get_hwnd();

	// Other
	const std::string process_name = "ffxiv_d11.exe";
	const std::string window_name = "FINAL FANTASY XIV";

private:

	// Singleton
	static FFXIV *p_instance;

	// Process specific
	unsigned long long base_address;
	HANDLE handle;
	DWORD pid;
	HWND hwnd;
	MODULEENTRY32 module;
};