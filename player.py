from ctypes.wintypes import c_float
from ctypes.wintypes import c_uint
from ctypes.wintypes import c_ulonglong
from munch import Munch

from memory import RegistryEntry
from offsets import entity_base_offsets
from offsets import player_parameter_offsets
from pointers import base_pointers
from singleton import Singleton

from entity import Entity


class Player(Entity):
    __metaclass__ = Singleton

    def __init__(self):
        self.target = None
        super(Player, self).__init__()

    def _update_registry_map(self):
        # Must be called here as pointers are likely already resolved
        # For the player, everything will be built on multiple pointer addresses.
        # Mostly on the base, but additional features will be added in, hence
        # subclassing.
        self.REGISTRY_MAP = Munch(
            # Parameters
            current_hp=self._build_registry_entry(
                'parameters', 'current_hp', 'parameters current_hp'
            ),
            max_hp=self._build_registry_entry(
                'parameters', 'max_hp', 'parameters max_hp'
            ),
            current_mp=self._build_registry_entry(
                'parameters', 'current_mp', 'parameters current_mp'
            ),
            max_mp=self._build_registry_entry(
                'parameters', 'max_mp', 'parameters max_mp'
            ),
            tp=self._build_registry_entry('parameters', 'tp', 'parameters tp'),

            # Player Base
            name=self._build_registry_entry(
                'base', 'name', data_type=self.NAME_BUFFER
            ),
            x=self._build_registry_entry('base', 'x', 'position x', c_float()),
            y=self._build_registry_entry('base', 'y', 'position y', c_float()),
            z=self._build_registry_entry('base', 'z', 'position z', c_float()),

            # Misc
            # target=self._build_registry_entry(
            #     'target', None, 'target', c_ulonglong()
            # )
        )

    def _build_registry_entry(
        self, offset_group, offset_name,
        attribute_path_str=None, data_type=c_uint()
    ):
        """
        offset_group -> determines which address and offsets are used.
        offset_name -> must match property name in corresponding OFFSETS.
            If no offset, assume it's a pointer.
        attribute_path_str -> how the value is to be assigned to the class.
            e.g. Player.position.x: 'position x'
        data_type -> specified wintype necessary for reading correct amount of bytes
        """
        if not attribute_path_str:
            attribute_path_str = offset_name

        if offset_group == 'parameters':
            ADDRESS = base_pointers.player_parameters.address
            OFFSETS = player_parameter_offsets
        elif offset_group == 'base':
            ADDRESS = base_pointers.entity_base.address
            OFFSETS = entity_base_offsets

        # Assume we are reading a pointer
        if not offset_name:
            pass

        return RegistryEntry(
            reference=self, attribute_path=attribute_path_str.split(),
            address=ADDRESS, offset=OFFSETS[offset_name],
            data_type=data_type
        )




