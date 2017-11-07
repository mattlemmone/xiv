from munch import Munch


class MemoryPointer(object):
    def __init__(self, offsets):
        # Resolved by MemoryWatch.find_all_multi_level_pointers iff offsets is a list
        self.address = None
        self.offsets = offsets


# Base pointers will be resolved and stored ONCE per run.
multi_level_pointers = Munch(
    entity_base=MemoryPointer([0x01802E50]),
    player_parameters=MemoryPointer(
        [0x01807FB8, 0x30, 0x58, 0x18, 0x20]
    ),
    player_skills=MemoryPointer([0x01807FB8, 0x30, 0x58, 0x30, 0x20]),
)

# noticed enemies have an offset that represent their distance from me...
# idea: search for address of player base in memory, find out what up
single_level_pointers = Munch(
    player_target=MemoryPointer([0x1801A10]),
    player_speed=MemoryPointer([0x1805768]),
    last_cmd=MemoryPointer([0x17E6822])
)
