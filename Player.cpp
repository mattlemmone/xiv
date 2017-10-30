#include "Player.h"
#include "Memory.h"
#include "FFXIV.h"
#include "Offsets.h"

Player::Player(BYTE* address) {
	MemoryRegistry* registry = MemoryRegistry::instance();
	PlayerOffsets offsets = PlayerOffsets();
	
	registry->add(&this->position.x, address + offsets.x);

	//this->name = read_address_string(handle, address + offsets.name, 0x32);
	//this->distance = read_address<float>(handle, address + offsets.distance);

	/*this->position.x = read_address<float>(handle, address + offsets.x);
	this->position.y = read_address<float>(handle, address + offsets.y);
	this->position.z = read_address<float>(handle, address + offsets.z);
	*/
	//this->parameters.current_health = read_address<unsigned int>(handle, address + offsets.current_health);
	//this->parameters.max_health = read_address<unsigned int>(handle, address + offsets.max_health);
	//this->parameters.current_mana = read_address<unsigned int>(handle, address + offsets.current_mana);
	//this->parameters.max_mana = read_address<unsigned int>(handle, address + offsets.max_mana);
	//this->parameters.tp = read_address<unsigned int>(handle, address + offsets.tp);
}
