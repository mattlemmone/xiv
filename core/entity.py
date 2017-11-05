from ctypes.wintypes import c_float
from ctypes.wintypes import c_uint
from ctypes.wintypes import c_ulonglong
from ctypes.wintypes import c_ubyte
from ctypes.wintypes import create_string_buffer
from munch import Munch
import logging
import time

from core.offsets import entity_base_offsets
from core.offsets import entity_size
from core.pointers import multi_level_pointers
from core.registerable import Registerable
from core.structs import Parameters
from core.structs import Position
from lib.memory import MemoryWatch
from lib.memory import RegistryEntry
from lib.memory import read_address

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MAX_NAME_LENGTH = 32
ENTITY_LIST_SIZE = 64
entity_address_list = []


class Entity(Registerable):

    def __init__(self, address):
        self.NAME_BUFFER = create_string_buffer('_' * MAX_NAME_LENGTH)

        self.name = None
        self.level = None
        self.address = address
        self.parameters = Parameters()
        self.position = Position()

        super(Entity, self).__init__()

    def __repr__(self):
        return str({
            'name': self.name,
            'level': self.level,
            'address': hex(self.address),
            'parameters': self.parameters,
            'position': self.position,
        })

    def _update_registry_map(self):
        # Must be called here as pointers are likely already resolved
        # For the entity, everything will be built on the base address.
        self.REGISTRY_MAP = Munch(
            current_hp=self._build_registry_entry(
                'entity base', 'current_hp', 'parameters current_hp'
            ),
            max_hp=self._build_registry_entry(
                'entity base', 'max_hp', 'parameters max_hp'
            ),
            current_mp=self._build_registry_entry(
                'entity base', 'current_mp', 'parameters current_mp'
            ),
            max_mp=self._build_registry_entry(
                'entity base', 'max_mp', 'parameters max_mp'
            ),

            name=self._build_registry_entry(
                'entity base', 'name', data_type=self.NAME_BUFFER
            ),
            level=self._build_registry_entry(
                'entity base', 'level', 'level', data_type=c_ubyte()
            ),
            x=self._build_registry_entry('entity base', 'x', 'position x', c_float()),
            y=self._build_registry_entry('entity base', 'y', 'position y', c_float()),
            z=self._build_registry_entry('entity base', 'z', 'position z', c_float()),
        )

    def _build_registry_entry(
        self, description, offset_name,
        attribute_path_str=None, data_type=c_uint()
    ):
        """
        description -> determines which address and offsets are used.
        offset_name -> must match property name in corresponding OFFSETS.
        attribute_path_str -> how the value is to be assigned to the class.
            e.g. Player.position.x: 'position x'
        data_type -> specified wintype necessary for reading correct amount of bytes
        """

        if not attribute_path_str:
            attribute_path_str = offset_name

        address = self.address
        offset = entity_base_offsets[offset_name]

        return RegistryEntry(
            reference=self, description=description, attribute_path=attribute_path_str.split(),
            address=address, offset=offset, data_type=data_type
        )


def get_entity_list():
    player_address = multi_level_pointers.entity_base.address
    entity_ptr_value = read_address(player_address, c_ulonglong())
    assert entity_ptr_value, 'Player base not found...?!'

    # Start with a fresh list
    clear_entities_from_memory()

    # Start at first non-self entity
    entity_address = player_address + entity_size
    entity_list = []

    for _ in xrange(ENTITY_LIST_SIZE):
        new_entity = Entity(entity_address)
        entity_list.append(new_entity)
        entity_address += entity_size

    global entity_address_list
    entity_address_list = [e.address for e in entity_list]

    # Pause for MemoryWatch to gather data
    time.sleep(.05)

    return entity_list


def clear_entities_from_memory():
    global entity_address_list
    for address in entity_address_list:
        MemoryWatch.unregister_by_address(address)
