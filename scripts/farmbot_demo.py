import logging
import time

from core.entity import get_entity_list
from core.movement_engine import MovementEngine
from core.player import Player
from core.script_manager import BaseScript
from core.skill_rotation import SkillRotation

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
        player = Player()
        REST_AT_HPP = 50

        while True:
            c_hp = player.parameters.current_hp
            m_hp = player.parameters.max_hp
            hpp = float(c_hp) / m_hp * 100

            while hpp <= REST_AT_HPP:
                pass

            enemy = get_nearest_enemy()
            go_to_enemy(enemy)
            fight_enemy(enemy)

            # Wait before continuing
            time.sleep(2)


def get_nearest_enemy():
    """
    Would make sense to have more filters like is_claimed, etc
    for actual usage.
    """
    player = Player()

    # Exclude mobs this much higher/lower than you
    MAX_LVL = 1
    MIN_LVL = 2

    # Gets all entities loaded in memory, <= 63
    entity_list = get_entity_list()

    min_dist = float('inf')
    nearest_enemy = None

    for entity in entity_list:
        # Skip dead ones
        if not entity.parameters.current_hp:
            continue

        # if entity.level < player.level - MIN_LVL:
        #     continue

        if entity.level > player.level + MAX_LVL:
            continue

        distance = MovementEngine.get_2d_distance(
            player.position, entity.position
        )

        if distance < min_dist:
            nearest_enemy = entity
            min_dist = distance

    assert nearest_enemy, 'Found no enemies :"('
    logger.info(
        'Nearest enemy: Lvl. %d %s, Address: %s',
        nearest_enemy.level,
        nearest_enemy.name,
        hex(nearest_enemy.address)
    )
    return nearest_enemy


def go_to_enemy(enemy):
    player = Player()

    # Set target, face it, run to it
    player.set_target(enemy.address)

    MovementEngine.run_to(enemy.position, tolerance=8)


def fight_enemy(enemy):
    player = Player()
    my_rotation = SkillRotation([4, 1, 2, 3])

    while player.target:
        logger.debug(
            '%s @ %d/%d hp',
            enemy.name,
            enemy.parameters.current_hp,
            enemy.parameters.max_hp
        )

        my_rotation.execute()
        time.sleep(1)
