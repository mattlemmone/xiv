from ctypes.wintypes import c_uint
from ctypes.wintypes import c_ulonglong
from ctypes.wintypes import create_string_buffer
from munch import Munch
import logging
import time

from core.entity import Entity
from core.offsets import entity_size
from core.pointers import multi_level_pointers
from core.pointers import single_level_pointers
from core.registerable import Registerable
from lib.memory import MemoryWatch
from lib.memory import read_address
from lib.memory import RegistryEntry
from lib.memory import write_address
from lib.singleton import Singleton

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ENTITY_LIST_SIZE = 64

MAX_CMD_LENGTH = 64
CMD_BUFFER = create_string_buffer('_' * MAX_CMD_LENGTH)

NULL_MSG_LENGTH = 1
NULL_BUFFER = create_string_buffer('_' * NULL_MSG_LENGTH)


class Client(Registerable):
    __metaclass__ = Singleton

    def __init__(self):
        # MemoryWatch's reference to this class is aka the address
        self.address = 'client'
        self.entity_address_list = []
        self._last_cmd = ''

        super(Client, self).__init__()

    @property
    def last_cmd(self):
        # Write '' to memory
        if self._last_cmd:
            writable_address = single_level_pointers.last_cmd.address
            data = NULL_BUFFER
            write_address(writable_address, data)
        ret = self._last_cmd
        self._last_cmd = ''
        return ret

    @last_cmd.setter
    def last_cmd(self, incoming_last_cmd):
        if incoming_last_cmd != '_':
            self._last_cmd = incoming_last_cmd

    def _update_registry_map(self):
        self.REGISTRY_MAP = Munch(
            last_cmd=self._build_registry_entry(
                'last_cmd', data_type=CMD_BUFFER
            ),
        )

    def _build_registry_entry(
        self, offset_name, data_type=c_uint(),
    ):
        attribute_path_str = offset_name
        description = 'client %s' % offset_name
        address = single_level_pointers.last_cmd.address
        offset = 0

        return RegistryEntry(
            reference=self, description=description,
            attribute_path=attribute_path_str.split(),
            address=address, offset=offset, data_type=data_type
        )

    def get_entity_list(self):
        player_address = multi_level_pointers.entity_base.address
        entity_ptr_value = read_address(player_address, c_ulonglong())
        assert entity_ptr_value, 'Player base not found...?!'

        # Start with a fresh list
        self._clear_entities_from_memory()

        # Start at first non-self entity
        entity_address = player_address + entity_size
        entity_list = []

        for _ in xrange(ENTITY_LIST_SIZE):
            new_entity = Entity(entity_address)
            entity_list.append(new_entity)
            entity_address += entity_size

        self.entity_address_list = [e.address for e in entity_list]

        # Pause for MemoryWatch to gather data
        time.sleep(.05)

        return entity_list

    def _clear_entities_from_memory(self):
        for address in self.entity_address_list:
            MemoryWatch.unregister_by_address(address)
