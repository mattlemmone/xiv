import logging

from lib.memory import MemoryWatch
from core.registry_entries import build_registry_entry

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Registerable(object):
    registry_tuple = []

    def __init__(self):
        self.register()

    def unregister(self):
        MemoryWatch.unregister_by_address(self.address)

    def register(self):
        """
        Registers every attribute found in registry_tuple.
        """
        for entry in self.registry_tuple:
            registry_entry = build_registry_entry(self, entry)
            MemoryWatch.register(registry_entry)

