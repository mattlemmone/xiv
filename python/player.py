from structs import Parameters
from structs import Position
from singleton import Singleton
from offsets import player_offsets
from memory import MemoryWatch


class Player(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.name = None
        self.target_distance = None
        self.parameters = Parameters()
        self.position = Position()

    def register(self):
        """
        (nested) itr for adding to memwatch registry
        """
        pass
