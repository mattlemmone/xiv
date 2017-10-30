#pragma once
#include <Windows.h>

struct Signature {

	Signature(char *pattern, char *mask, DWORD offset) {
		this->pattern = (BYTE*)pattern;
		this->mask = mask;
		this->offset = offset;
	}

	BYTE *pattern;
	char *mask;
	DWORD offset;

	bool found = false;
	byte* address;
};


static Signature *player_cords = new Signature(
    "\xD0\x8C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x62\xE7",
	"xx?????xxxxxxxxxxx",
	0xA0
);

static Signature *player_parameters = new Signature(
	"\x8B\x00\x00\x00\x00\x00\x4C\x8B\xF0\x44\x8B\x7B",
	"x?????xxxxxx",
	0x02
);

static Signature *all_signatures[] = { 
	//player_cords,
	player_parameters
}; 