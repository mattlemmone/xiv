import logging
from ctypes.wintypes import c_ulonglong

from core.entity import Entity
from core.pointers import multi_level_pointers
from core.pointers import single_level_pointers
from core.structs import Skill
from lib.memory import MemoryWatch
from lib.memory import write_address
from lib.singleton import Singleton
from core.registry_entries import player_entries
from core.registry_entries import NUM_SKILLS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Player(Entity):
    __metaclass__ = Singleton
    registry_tuple = player_entries

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


