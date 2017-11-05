from copy import deepcopy
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


def record_waypoints(step=500, duration=10000):
    """
    Records a waypoint every step (ms) for duration (ms)
    """
    waypoints = []
    player = Player()

    start_time = time.time()
    while time.time() - start_time < duration / 1000:
        logger.debug('recording waypoint... %r', player.position)
        waypoints.append(deepcopy(player.position))

        time.sleep(step / 1000.0)

    logger.debug('stop moving!')
    time.sleep(2)

    return waypoints
