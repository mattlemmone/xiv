from munch import Munch


class MemoryPointer(object):
    def __init__(self, offsets):
        # Resolved by MemoryWatch.find_all_base_pointers iff offsets is a list
        self.address = None

        if isinstance(offsets, list):
            self.offsets = offsets
        else:
            self.address = offsets

# Base pointers will be resolved and stored ONCE per run.
base_pointers = Munch(
    # all enemies in area are + 0x2930 from player base! about 64?
    # found by scanning hex for the 1st value in player base!
    entity_base=MemoryPointer([0x01802E50]),
    player_parameters=MemoryPointer(
        [0x01807FB8, 0x30, 0x58, 0x18, 0x20]
    )
)

# noticed enemies have an offset that represent their distance from me...
# idea: search for address of player base in memory, find out what up
single_level_pointers = Munch(
    player_target=MemoryPointer(0x1801A10),
    player_speed=MemoryPointer(0x1805768)
)
