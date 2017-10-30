#include "Structs.h"

Position::Position(){}
Position::Position(float x, float y, float z) {
	this->x = x;
	this->y = y;
	this->z = z;
}

Position::Position(BYTE* address) {
	FFXIV *ffxiv = FFXIV::instance();
	HANDLE hnd = ffxiv->get_handle();
	this->x = read_address<float>(hnd, address);
	this->y = read_address<float>(hnd, address + 0x4);
	this->z = read_address<float>(hnd, address + 0x8);
}

Parameters::Parameters() {}


