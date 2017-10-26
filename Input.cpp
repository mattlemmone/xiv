#include <Windows.h>
#include <iostream>

void send_key_press(HWND hwnd, DWORD delay_ms = 300) {
	PostMessage(hwnd, WM_KEYDOWN, 0x57, 0);
	Sleep(delay_ms);
	PostMessage(hwnd, WM_KEYUP, 0x57, 0);
}