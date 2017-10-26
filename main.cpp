// XIV.cpp : Defines the entry point for the console application.
//

#include <iostream>

#include "Memory.h"
#include "Process.h"
#include "FFXIV.h"

void initialize_ffxiv_data() {
	/*
		Updates ffxiv singleton with process information.
	*/
	FFXIV *ffxiv = FFXIV::instance();

	// Get data
	HWND hwnd = get_hwnd("FINAL FANTASY XIV");
	DWORD pid = get_pid(hwnd);
	HANDLE handle = get_process_handle(pid);
	DWORD64 base_address = get_base_address(handle);

	// Update instance
	ffxiv->set_hwnd(hwnd);
	ffxiv->set_pid(pid);
	ffxiv->set_handle(handle);
	ffxiv->set_base_address(base_address);
}

int main()
{	
	FFXIV *ffxiv = FFXIV::instance();
	initialize_ffxiv_data();
	
	//send_key_press(xiv_process.hwnd);
	//send_key_press(xiv_process.hwnd);
	//send_key_press(xiv_process.hwnd);
	//send_key_press(xiv_process.hwnd);

	DWORD64 health_address = 0x2451FDA56F8;
	uint8_t	health = 0;
	HANDLE xiv_handle = ffxiv->get_handle();

	while (true) {
		health = read_memory<uint8_t>(xiv_handle, health_address);
		std::cout << unsigned(health);
		Sleep(300);
		system("cls");
	}
	return 0;
}
