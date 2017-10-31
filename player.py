from structs import Parameters
from structs import Position
from singleton import Singleton
from offsets import player_base_offsets
from offsets import player_parameter_offsets
from memory import RegistryEntry
from ctypes.wintypes import c_uint
from munch import Munch
from pointers import all_pointers

REGISTRY_MAP = Munch()


class Player(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.name = None
        self.target_distance = None
        self.parameters = Parameters
        self.position = Position

        self._register()

    def _register(self):
        _update_registry_map()
        for attribute in REGISTRY_MAP:
            self._create_registry_entry(attribute)

    def _create_registry_entry(self, attribute):
        mapping = REGISTRY_MAP.get(attribute)
        attribute_path = mapping.attribute_path
        data_type = mapping.type
        address = mapping.address
        offset = mapping.offset
        assert(address)

        RegistryEntry(
            reference=self, attribute_path=attribute_path,
            address=address, offset=offset, data_type=data_type
        ).register()


def _update_registry_map():
    # Must be called here as pointers are likely already resolved
    PARAM_ADDRESS = all_pointers.player_parameters.address
    PARAM_OFFSETS = player_parameter_offsets

    global REGISTRY_MAP
    REGISTRY_MAP = Munch(
        current_health=Munch(
            address=PARAM_ADDRESS, offset=PARAM_OFFSETS.current_health,
            type=c_uint(), attribute_path=['parameters', 'current_health']
        ),
        max_health=Munch(
            address=PARAM_ADDRESS, offset=PARAM_OFFSETS.max_health,
            type=c_uint(), attribute_path=['parameters', 'max_health']
        ),
        current_mana=Munch(
            address=PARAM_ADDRESS, offset=PARAM_OFFSETS.current_mana,
            type=c_uint(), attribute_path=['parameters', 'current_mana']
        ),
        max_mana=Munch(
            address=PARAM_ADDRESS, offset=PARAM_OFFSETS.max_mana,
            type=c_uint(), attribute_path=['parameters', 'max_mana']
        ),
        tp=Munch(
            address=PARAM_ADDRESS, offset=PARAM_OFFSETS.tp,
            type=c_uint(), attribute_path=['parameters', 'tp']
        ),
    )
