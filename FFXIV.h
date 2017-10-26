#include <string>
#include <Windows.h>

#pragma once
class FFXIV {

public:

	// Get singleton
	static FFXIV *instance();

	// Setters
	void set_base_address(DWORD64 base_address);
	void set_handle(HANDLE handle);
	void set_pid(DWORD pid);
	void set_hwnd(HWND hwnd);

	// Getters
	DWORD64 const& get_base_address();
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
	DWORD64 base_address;
	HANDLE handle;
	DWORD pid;
	HWND hwnd;
};