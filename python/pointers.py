from munch import Munch


class MemoryPointer(object):
    def __init__(self, offsets):
        self.offsets = offsets

        # Set by find_all_pointers
        self.address = None


all_pointers = Munch(
    player_base=MemoryPointer([0x01802E50]),
    player_parameters=MemoryPointer(
        [0x01807FB8, 0x30, 0x58, 0x18, 0x20, 0x00]
    ),
)
