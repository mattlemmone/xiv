from munch import Munch
import logging

from lib.memory import MemoryWatch


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Registerable(object):

    def __init__(self):
        self.REGISTRY_MAP = Munch()
        self.register()

    def unregister(self):
        MemoryWatch.unregister_by_address(self.address)

    def register(self):
        """
        Registers every attribute found in REGISTRY_MAP.
        """
        self._update_registry_map()

        for attribute in self.REGISTRY_MAP:
            registry_entry = self.REGISTRY_MAP.get(attribute)
            MemoryWatch.register(registry_entry)

    def _update_registry_map():
        pass
