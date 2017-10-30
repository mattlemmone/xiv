#pragma once
#include <Windows.h>
#include <string>
#include "Structs.h"

class Player {
public:
	Player(BYTE* address);

	std::string name;
	float distance;

	// Position
	Position position;
	float heading;

	// Parameters
	Parameters parameters;
};