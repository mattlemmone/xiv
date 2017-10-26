// XIV.cpp : Defines the entry point for the console application.
//

#include <iostream>
#include <vector>

#include "Memory.h"
#include "Process.h"
#include "FFXIV.h"

void initialize_ffxiv_data() {
	/*
		Updates ffxiv singleton with process information.
	*/
	FFXIV *ffxiv = FFXIV::instance();

	// Get data
	HWND hwnd = get_hwnd(ffxiv->window_name);
	DWORD pid = get_pid(hwnd);
	HANDLE handle = get_process_handle(pid);
	long long base_address = get_base_address(pid, ffxiv->process_name);

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

	HANDLE xiv_handle = ffxiv->get_handle();
	unsigned long long xiv_base = ffxiv->get_base_address();
	std::vector<long long> health_offsets = { 0x1828C34 };

	while (true) {
		uint8_t health = read_address_pointers<uint8_t>(xiv_handle, xiv_base, health_offsets);
		//health = read_address<uint8_t>(xiv_handle, xiv_base + 0x1828C34);
		std::cout << unsigned(health);
		Sleep(600);
		system("cls");
	}
	return 0;
}
