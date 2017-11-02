from ctypes.wintypes import c_float
from ctypes.wintypes import c_uint
from ctypes.wintypes import c_ulonglong
from munch import Munch

from entity import Entity
from memory import MemoryWatch
from memory import RegistryEntry
from offsets import entity_base_offsets
from offsets import player_parameter_offsets
from pointers import base_pointers
from pointers import single_level_pointers
from singleton import Singleton


class Player(Entity):
    __metaclass__ = Singleton

    def __init__(self):
        self._target_address = None
        self.target_entity = None
        super(Player, self).__init__(address=None)

    @property
    def target_address(self):
        return self._target_address

    @target_address.setter
    def target_address(self, new_target_address):
        # Target unchanged
        if new_target_address == self._target_address:
            return

        # Target changed
        if self.target_entity:
            MemoryWatch.unregister_by_ref(self.target_entity)
        if new_target_address:
            self.target_entity = Entity(new_target_address)
        self._target_address = new_target_address

    def _update_registry_map(self):
        # Must be called here as pointers are likely already resolved
        # For the player, everything will be built on multiple pointer addresses.
        # Mostly on the base, but additional features will be added in, hence
        # subclassing.
        self.REGISTRY_MAP = Munch(
            # Parameters
            current_hp=self._build_registry_entry(
                'player params', 'current_hp', 'parameters current_hp'
            ),
            max_hp=self._build_registry_entry(
                'player params', 'max_hp', 'parameters max_hp'
            ),
            current_mp=self._build_registry_entry(
                'player params', 'current_mp', 'parameters current_mp'
            ),
            max_mp=self._build_registry_entry(
                'player params', 'max_mp', 'parameters max_mp'
            ),
            tp=self._build_registry_entry('player params', 'tp', 'parameters tp'),

            # Player Base
            name=self._build_registry_entry(
                'player base', 'name', data_type=self.NAME_BUFFER
            ),
            x=self._build_registry_entry('player base', 'x', 'position x', c_float()),
            y=self._build_registry_entry('player base', 'y', 'position y', c_float()),
            z=self._build_registry_entry('player base', 'z', 'position z', c_float()),

            # Misc
            target_address=self._build_registry_entry(
                'player target address', None, 'target_address', c_ulonglong()
            )
        )

    def _build_registry_entry(
        self, description, offset_name,
        attribute_path_str=None, data_type=c_uint()
    ):
        """
        description -> determines which address and offsets are used.
        offset_name -> must match property name in corresponding OFFSETS.
            If no offset, assume it's a pointer.
        attribute_path_str -> how the value is to be assigned to the class.
            e.g. Player.position.x: 'position x'
        data_type -> specified wintype necessary for reading correct amount of bytes
        """
        if not attribute_path_str:
            attribute_path_str = offset_name

        # Assume this is a pointer
        if not offset_name:
            offset = 0

        if 'params' in description:
            pointer = base_pointers.player_parameters
            offset = player_parameter_offsets[offset_name]
        elif 'base' in description:
            pointer = base_pointers.entity_base
            offset = entity_base_offsets[offset_name]
        elif 'target address' in description:
            pointer = single_level_pointers.player_target
        else:
            print 'error on %s %s' % (description, attribute_path_str)
        return RegistryEntry(
            reference=self, description=description, attribute_path=attribute_path_str.split(),
            address=pointer.address, offset=offset,
            data_type=data_type, is_lvl1_ptr=bool(not offset_name)
        )
