from munch import Munch

"""
Each group (Munch) of offsets should be distinguished by their base address.
If two items do not share a base pointer, they do not belong in the same group.
"""

entity_base_offsets = Munch(
    # Misc
    name=0x30,
    distance=0x8D,
    level=0x16E0,
    is_fighting=0x3A9,

    # Position
    x=0xA0,
    z=0xA0 + 4,
    y=0xA0 + 8,
    heading=0xA0 + 16,

    # Parameters without TP
    current_hp=0x16A8,
    max_hp=0x16A8 + 4,
    current_mp=0x16A8 + 8,
    max_mp=0x16A8 + 12,
)

player_parameter_offsets = Munch(
    current_hp=0x00,
    max_hp=0x00 + 4,
    current_mp=0x00 + 8,
    max_mp=0x00 + 12,
    tp=0x00 + 16,
)

player_skill_offsets = Munch(
    class_id=0x3C,
    type=0x3C + 4,
    skill_id=0x3C + 12,
    ready_percent=0x3C + 20,
    tp_cost=0x3C + 28,
    in_range=0x3C + 36
)

client_offsets = Munch(
    jump_grav_start=0x8A4,
    jump_dir_1=0x870,
    jump_dir_2=0x870 + 8,
)

entity_size = 0x2930
skill_size = 0x28
