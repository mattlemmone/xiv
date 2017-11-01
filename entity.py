from ctypes.wintypes import create_string_buffer
from ctypes.wintypes import c_float
from ctypes.wintypes import c_uint
from munch import Munch

from memory import RegistryEntry
from offsets import entity_base_offsets
from pointers import base_pointers
from structs import Parameters
from structs import Position

MAX_NAME_LENGTH = 32


class Entity(object):

    def __init__(self):

        self.REGISTRY_MAP = Munch()
        self.NAME_BUFFER = create_string_buffer('_' * MAX_NAME_LENGTH)

        self.name = None
        self.parameters = Parameters
        self.position = Position

        self._register()

    def _register(self):
        self._update_registry_map()
        for attribute in self.REGISTRY_MAP:
            self._create_registry_entry(attribute)

    def _create_registry_entry(self, attribute):
        """
        Forwards data from registry map to create and register a new RegistryEntry
        """
        registry_entry = self.REGISTRY_MAP.get(attribute)
        assert(registry_entry.address)

        registry_entry.register()

    def _update_registry_map(self):
        # Must be called here as pointers are likely already resolved
        # For the entity, everything will be built on the base address.
        self.REGISTRY_MAP = Munch(
            current_hp=self._build_registry_entry(
                'base', 'current_hp', 'parameters current_hp'
            ),
            max_hp=self._build_registry_entry(
                'base', 'max_hp', 'parameters max_hp'
            ),
            current_mp=self._build_registry_entry(
                'base', 'current_mp', 'parameters current_mp'
            ),
            max_mp=self._build_registry_entry(
                'base', 'max_mp', 'parameters max_mp'
            ),

            name=self._build_registry_entry(
                'base', 'name', data_type=self.NAME_BUFFER
            ),
            x=self._build_registry_entry('base', 'x', 'position x', c_float()),
            y=self._build_registry_entry('base', 'y', 'position y', c_float()),
            z=self._build_registry_entry('base', 'z', 'position z', c_float()),
        )

    def _build_registry_entry(
        self, offset_group, offset_name,
        attribute_path_str=None, data_type=c_uint()
    ):
        """
        offset_group -> determines which address and offsets are used.
        offset_name -> must match property name in corresponding OFFSETS.
        attribute_path_str -> how the value is to be assigned to the class.
            e.g. Player.position.x: 'position x'
        data_type -> specified wintype necessary for reading correct amount of bytes
        """

        if not attribute_path_str:
            attribute_path_str = offset_name

        ADDRESS = base_pointers.entity_base.address
        OFFSETS = entity_base_offsets

        return RegistryEntry(
            reference=self, attribute_path=attribute_path_str.split(),
            address=ADDRESS, offset=OFFSETS[offset_name],
            data_type=data_type
        )


