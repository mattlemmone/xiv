#include <iostream>
#include "SignatureScanner.h"
#include "Signatures.h"

bool SignatureScanner::compare_data(BYTE* pbData, BYTE* pattern, const char* XsAndQuestionMarks)
{
	for (; *XsAndQuestionMarks; ++XsAndQuestionMarks, ++pbData, ++pattern)
	{
		if (*XsAndQuestionMarks == 'x' && *pbData != *pattern)
		{
			return FALSE;
		}
	}
	return (*XsAndQuestionMarks) == NULL;
}

BYTE* SignatureScanner::find_pattern(HANDLE hproc, MODULEENTRY32 module, BYTE* sig, char* mask) {
	MEMORY_BASIC_INFORMATION meminfo = { 0 };
	BYTE* page_buffer = NULL;
	BYTE* MAX_ADDRESS = module.modBaseAddr + module.modBaseSize;
	BYTE* start = module.modBaseAddr;

	while (VirtualQueryEx(hproc, start, &meminfo, sizeof(meminfo)))
	{
		if (start >= MAX_ADDRESS)
			break;

		size_t step_size = meminfo.RegionSize;
		if (step_size > 0x2000000) {
			start += step_size;
			continue;
		}
		page_buffer = new BYTE[step_size];

		// Page is allocated in memory and has RW priv.
		bool can_read = meminfo.Protect & (PAGE_READWRITE | PAGE_READONLY | PAGE_EXECUTE_READ);
		if ((meminfo.State == MEM_COMMIT) && can_read) {
			if (!ReadProcessMemory(hproc, start, page_buffer, step_size, NULL))
				break;

			// Scan page buffer for signature
			for (size_t i = 0; i < step_size; i++) {
				// Found signature
				if (compare_data((BYTE*)(page_buffer + i), sig, mask)) {
					delete page_buffer;
					return start + i;
				}
			}
		}

		delete page_buffer;
		start += step_size;
	}

	delete page_buffer;
	return NULL;
}

