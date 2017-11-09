from copy import deepcopy
from ctypes.wintypes import c_float
from ctypes.wintypes import c_ubyte
from ctypes.wintypes import c_uint
from ctypes.wintypes import c_ulonglong
from ctypes.wintypes import create_string_buffer
from munch import Munch

from core.offsets import client_offsets
from core.offsets import entity_base_offsets
from core.offsets import player_parameter_offsets
from core.offsets import player_skill_offsets
from core.offsets import skill_size
from core.pointers import multi_level_pointers
from core.pointers import single_level_pointers
from core.structs import Skill

NUM_SKILLS = 10

MAX_CMD_LENGTH = 64
CMD_BUFFER = create_string_buffer('_' * MAX_CMD_LENGTH)

MAX_NAME_LENGTH = 32
NAME_BUFFER = create_string_buffer('_' * MAX_NAME_LENGTH)


class RegistryEntry(object):
    def __init__(
        self, reference, attribute_path, address, data_type,
    ):
        assert address, 'Address must exist in order to create RegistryEntry'
        self.reference = reference
        self.attribute_path = attribute_path
        self.data_type = data_type
        self.address = address


POINTERS = Munch(
    client=Munch(
        last_cmd=single_level_pointers.last_cmd,
        hacks=multi_level_pointers.entity_base,
    ),
    entity=Munch(
        base=None
    ),
    player=Munch(
        base=multi_level_pointers.entity_base,
        parameters=multi_level_pointers.player_parameters,
        skills=multi_level_pointers.player_skills,
        target_address=single_level_pointers.player_target
    )
)

OFFSETS = Munch(
    client=Munch(
        hacks=client_offsets
    ),
    entity=Munch(
        base=entity_base_offsets
    ),
    player=Munch(
        base=entity_base_offsets,
        parameters=player_parameter_offsets,
        skills=player_skill_offsets
    )
)

client_entries = [
    ('last_cmd', CMD_BUFFER),
    ('hacks player_speed', c_float()),
    ('hacks jump_grav_start', c_float()),
    ('hacks jump_dir_1', c_float()),
    ('hacks jump_dir_2', c_float()),
]

entity_entries = [
    # Parameters
    ('parameters current_hp', c_uint()),
    ('parameters current_mp', c_uint()),
    ('parameters max_hp', c_uint()),
    ('parameters max_mp', c_uint()),

    # Entity Base
    ('level', c_ubyte()),
    ('name', NAME_BUFFER),

    # Position
    ('position heading', c_float()),
    ('position x', c_float()),
    ('position y', c_float()),
    ('position z', c_float()),
]


player_entries = deepcopy(entity_entries)
player_entries += [
    ('parameters tp', c_uint()),
    ('target_address', c_ulonglong())
]

# Skills
attributes = [
    attr for attr in vars(Skill())
    if not attr.startswith('_')
]

for skill_idx in xrange(NUM_SKILLS):
    for skill_attribute in attributes:
        skill_entry = (
            'skills %d %s' % (skill_idx, skill_attribute), c_uint(),
        )

        player_entries.append(skill_entry)


def build_registry_entry(
    reference, attr_type_tuple,
):
    """
    Builds a registry entry from above tuples.
    tuple[0] -> attribute path
    tuple[1] -> data type
    """
    category = reference.__class__.__name__.lower()
    attribute_path = attr_type_tuple[0].split()
    data_type = attr_type_tuple[1]

    pointer = POINTERS[category]
    offset = OFFSETS.get(category, 0)

    if category == 'client':
        pointer = pointer[attribute_path[0]]
        offset = 0

        if len(attribute_path) == 2:
            # Client hacks are based on player base addr
            if attribute_path[0] == 'hacks':
                offset = OFFSETS.client.hacks.get(attribute_path[1], 0)
            if attribute_path[1] == 'player_speed':
                pointer = single_level_pointers.player_speed
    else:
        # Entity or Player
        if category == 'entity':
            POINTERS.entity.base = reference

        if 'target_address' in attribute_path:
            pointer = pointer['target_address']
            offset = 0
        elif len(attribute_path) == 1:
            pointer = pointer['base']
            offset = offset['base'][attribute_path[0]]
        elif len(attribute_path) == 2:
            pointer = pointer.get(attribute_path[0], pointer['base'])
            offset = offset.get(attribute_path[0], offset['base'])
            offset = offset[attribute_path[1]]
        elif 'skills' in attribute_path:
            pointer = pointer[attribute_path[0]]
            offset = offset[attribute_path[0]][attribute_path[2]]
            offset += skill_size * int(attribute_path[1])

    return RegistryEntry(
        reference=reference, attribute_path=attribute_path,
        address=pointer.address + offset,
        data_type=data_type
    )
