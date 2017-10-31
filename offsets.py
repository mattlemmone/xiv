from munch import Munch

player_base_offsets = Munch(
    # Misc
    name=0x30,
    distance=0x8D,

    # Position
    x=0xA0,
    z=0xA4,
    y=0xA8,
    heading=0xB0,
)

player_parameter_offsets = Munch(
    current_health=0x00,
    max_health=0x04,
    current_mana=0x08,
    max_mana=0x0C,
    tp=0x10,
)
