from copy import deepcopy
import logging
import time

from core.entity import get_entity_list
from core.movement_engine import MovementEngine
from core.player import Player
from core.script_manager import BaseScript

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# All scripts must inherit from BaseScript
class Script(BaseScript):
    # True by default, even without this next line.
    script_active = True

    # 'run' is the entry point of the script
    @staticmethod
    def run():
        logger.debug('going to say hi to err1')
        player = Player()
        entity_list = get_entity_list()

        original_coords = deepcopy(player.position)
        for entity in entity_list:
            MovementEngine.teleport_to(entity.position)
            time.sleep(0.75)
        MovementEngine.teleport_to(original_coords)
        logger.debug('homie im hon')
