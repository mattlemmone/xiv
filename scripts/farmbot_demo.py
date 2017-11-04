import logging
import math
import time

from core.entity import get_entity_list
from core.movement_engine import MovementEngine
from core.player import Player
from core.script_manager import BaseScript
from lib.input import KeyboardInput

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# All scripts must inherit from BaseScript
class Script(BaseScript):
    # True by default, even without this next line.
    script_active = True

    # 'run' is the entry point of the script
    @staticmethod
    def run():
        logger.debug('script started')

        while True:
            logger.debug('getting enemy')
            enemy = get_nearest_enemy()

            MovementEngine.run_to(enemy.position)
            KeyboardInput.key_press('tab')

            while enemy.parameters.current_hp:
                logger.debug('rotation')
                logger.debug(
                    '%s @ %d/%d hp',
                    enemy.name,
                    enemy.parameters.current_hp,
                    enemy.parameters.max_hp
                )
                do_rotation()
                time.sleep(1)


def get_nearest_enemy():
    """
    Would make sense to have more filters like is_claimed, etc
    for actual usage.
    """
    player = Player()
    entity_list = get_entity_list()

    min_dist = float('inf')
    nearest_enemy = None

    for entity in entity_list:
        if not entity.parameters.current_hp:
            continue

        distance = MovementEngine.get_2d_distance(
            player.position, entity.position
        )

        if distance < min_dist:
            nearest_enemy = entity
            min_dist = distance

    assert nearest_enemy, 'Found no enemies :"('
    logger.info('Nearest enemy: %s', nearest_enemy.name)
    return nearest_enemy


def do_rotation():
    """
    Embarassing raw key input for now
    """
    KeyboardInput.key_press('2')
    time.sleep(.05)
    KeyboardInput.key_press('1')
    time.sleep(.05)
