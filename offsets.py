from munch import Munch

"""
Each group (Munch) of offsets should be distinguished by their base address.
If two items do not share a base pointer, they do not belong in the same group.
"""

entity_base_offsets = Munch(
    # Misc
    name=0x30,
    distance=0x8D,

    # Position
    x=0xA0,
    z=0xA0 + 4,
    y=0xA0 + 8,
    heading=0xB0,

    # Parameters without TP
    current_health=0x16A0,
    max_health=0x16A0 + 4,
    current_mana=0x16A0 + 8,
    max_mana=0x16A0 + 12,
)

player_parameter_offsets = Munch(
    current_health=0x00,
    max_health=0x00 + 4,
    current_mana=0x00 + 8,
    max_mana=0x00 + 12,
    tp=0x00 + 16,
)
