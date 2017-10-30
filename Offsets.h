#pragma once

struct PlayerOffsets {
	unsigned int name = 0x30;
	unsigned int distance = 0x8D;

	// Position
	unsigned int x = 0xA0;
	unsigned int z = 0xA4;
	unsigned int y = 0xA8;
	unsigned int heading = 0xB0;
	
	// Parameters
	unsigned int current_health = 0x16A8;
	unsigned int max_health = 0x16AC;
	unsigned int current_mana = 0x16B0;
	unsigned int max_mana = 0x16B4;
	unsigned int tp = 0x16B8;
	
};