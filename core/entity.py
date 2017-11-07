import logging

from core.registry_entries import entity_entries
from core.structs import Parameters
from core.structs import Position
from lib.registerable import Registerable

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Entity(Registerable):
    registry_tuple = entity_entries

    def __init__(self, address):
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

