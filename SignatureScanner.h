#pragma once
#include <Windows.h>
#include <tlhelp32.h>

#define SAFE_MIN_ADDRESS 0x000001A18E870000

class SignatureScanner {
public:
	BYTE* SignatureScanner::find_pattern(HANDLE hproc, MODULEENTRY32 module, BYTE* sig, char* mask);
private:
	bool compare_data(BYTE* pbData, BYTE* pattern, const char* XsAndQuestionMarks);
};