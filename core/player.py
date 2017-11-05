import logging

from ctypes.wintypes import c_float
from ctypes.wintypes import c_uint
from ctypes.wintypes import c_ulonglong
from ctypes.wintypes import c_ubyte
from munch import Munch

from core.entity import Entity
from core.offsets import entity_base_offsets
from core.offsets import player_parameter_offsets
from core.offsets import player_skill_offsets
from core.offsets import skill_size
from core.pointers import multi_level_pointers
from core.pointers import single_level_pointers
from core.structs import Skill
from lib import client
from lib.memory import MemoryWatch
from lib.memory import RegistryEntry
from lib.memory import write_address
from lib.singleton import Singleton

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

NUM_SKILLS = 10


class Player(Entity):
    __metaclass__ = Singleton

    def __init__(self):
        self._target_address = None
        self.target = None
        self.skills = [Skill() for i in xrange(NUM_SKILLS)]

        super(Player, self).__init__(
            address=multi_level_pointers.entity_base.address
        )

    @staticmethod
    def set_target(target_address):
        writable_address = single_level_pointers.player_target.address
        data = c_ulonglong(target_address)
        write_address(writable_address, data)

    @property
    def target_address(self):
        return self._target_address

    @target_address.setter
    def target_address(self, new_target_address):
        # Target unchanged
        if new_target_address == self._target_address:
            return

        # Target changed
        if self.target and self._target_address:
            # Unregister existing target
            if self.address != self._target_address:
                MemoryWatch.unregister_by_address(self._target_address)
                self.target = None

        # Create new entity
        if new_target_address:
            self.target = Entity(new_target_address)
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
            level=self._build_registry_entry(
                'player base', 'level', data_type=c_ubyte()
            ),
            x=self._build_registry_entry('player base', 'x', 'position x', c_float()),
            y=self._build_registry_entry('player base', 'y', 'position y', c_float()),
            z=self._build_registry_entry('player base', 'z', 'position z', c_float()),
            heading=self._build_registry_entry('player base', 'heading', 'position heading', c_float()),

            # Misc
            target_address=self._build_registry_entry(
                'player target address', None, 'target_address', c_ulonglong()
            )
        )

        # Skills
        attributes = [a for a in vars(Skill()) if not a.startswith('_')]

        for skill_idx in xrange(NUM_SKILLS):
            for skill_attribute in attributes:
                key = 'player skill %d %s' % (skill_idx, skill_attribute)
                self.REGISTRY_MAP.update({
                    key:
                    self._build_registry_entry(
                        description=key,
                        offset_name=skill_attribute,
                        attribute_path_str='skills %d %s' % (skill_idx, skill_attribute),
                        data_type=c_uint(),
                        multiple=skill_idx
                    )
                })

    def _build_registry_entry(
        self, description, offset_name,
        attribute_path_str=None, data_type=c_uint(),
        multiple=None
    ):
        """
        description -> determines which address and offsets are used.
        offset_name -> must match property name in corresponding OFFSETS.
            If no offset, assume it's a pointer.
        attribute_path_str -> how the value is to be assigned to the class.
            e.g. Player.position.x: 'position x'
        data_type -> specified wintype necessary for reading correct amount of bytes
        multiple -> used to reference list indices
        """
        if not attribute_path_str:
            attribute_path_str = offset_name

        # Assume this is a pointer
        if not offset_name:
            offset = 0

        if 'params' in description:
            pointer = multi_level_pointers.player_parameters
            offset = player_parameter_offsets[offset_name]
        elif 'base' in description:
            pointer = multi_level_pointers.entity_base
            offset = entity_base_offsets[offset_name]
        elif 'target address' in description:
            pointer = single_level_pointers.player_target
        elif 'skill' in description:
            pointer = multi_level_pointers.player_skills
            offset = player_skill_offsets[offset_name]
            offset += skill_size * multiple
        else:
            print 'error on %s %s' % (description, attribute_path_str)
        return RegistryEntry(
            reference=self, description=description, attribute_path=attribute_path_str.split(),
            address=pointer.address, offset=offset,
            data_type=data_type
        )
