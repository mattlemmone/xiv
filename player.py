from ctypes.wintypes import create_string_buffer
from ctypes.wintypes import c_float
from ctypes.wintypes import c_uint
from munch import Munch

from memory import RegistryEntry
from offsets import entity_base_offsets
from offsets import player_parameter_offsets
from pointers import base_pointers
from singleton import Singleton
from structs import Parameters
from structs import Position

from entity import Entity


class Player(Entity):
    __metaclass__ = Singleton

    def _update_registry_map(self):
        # Must be called here as pointers are likely already resolved
        self.REGISTRY_MAP = Munch(
            # Parameters
            current_health=self._build_registry_dict(
                'parameters', 'current_health', 'parameters current_health'
            ),
            max_health=self._build_registry_dict(
                'parameters', 'max_health', 'parameters max_health'
            ),
            current_mana=self._build_registry_dict(
                'parameters', 'current_mana', 'parameters current_mana'
            ),
            max_mana=self._build_registry_dict(
                'parameters', 'max_mana', 'parameters max_mana'
            ),
            tp=self._build_registry_dict('parameters', 'tp', 'parameters tp'),

            # Player Base
            name=self._build_registry_dict(
                'base', 'name', data_type=self.NAME_BUFFER
            ),
            x=self._build_registry_dict('base', 'x', 'position x', c_float()),
            y=self._build_registry_dict('base', 'y', 'position y', c_float()),
            z=self._build_registry_dict('base', 'z', 'position z', c_float()),
        )

    def _build_registry_dict(
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

        if offset_group == 'parameters':
            ADDRESS = base_pointers.player_parameters.address
            OFFSETS = player_parameter_offsets
        else:
            ADDRESS = base_pointers.entity_base.address
            OFFSETS = entity_base_offsets

        return Munch(
            address=ADDRESS, offset=OFFSETS[offset_name],
            type=data_type, attribute_path=attribute_path_str.split()
        )



