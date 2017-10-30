#pragma once
#include "Memory.h"
#include "FFXIV.h"

struct Parameters {
	Parameters();

	unsigned int current_health;
	unsigned int max_health;
	unsigned int current_mana;
	unsigned int max_mana;
	unsigned int tp;
};

struct Position {
	Position();
	Position(float x, float y, float z);
	Position(BYTE* address);

	float x;
	float y;
	float z;
};