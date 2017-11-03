import logging
import time

from core.player import Player
from core.movement_engine import MovementEngine
from core.script_manager import BaseScript

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# All scripts must inherit from BaseScript
class Script(BaseScript):
    # True by default, even without this next line.
    script_active = False

    # 'run' is the entry point of the script
    @staticmethod
    def run():
        logger.debug('script started')
        waypoints = record_waypoints()

        # Use the movement system to run to each waypoint backwards!
        MovementEngine.run_waypoints(reversed(waypoints))


def record_waypoints(step=1000, duration=4000):
    """
    Records a waypoint every step (ms) for duration (ms)
    """
    waypoints = []
    counter = 0
    player = Player()

    while counter < duration:
        logger.debug('recording waypoint... %r', player.position)
        waypoints.append(player.position.copy())

        counter += step
        time.sleep(step / 1000)

    logger.debug('stop moving!')
    time.sleep(2)

    return waypoints
