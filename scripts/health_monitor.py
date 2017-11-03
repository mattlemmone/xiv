import logging
import time

from core.player import Player
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
        player = Player()

        # Example scenario
        while True:
            time.sleep(1)
            if player.parameters.current_hp == 0:
                last_target = player.target_entity.name
                logger.warning(
                    'U fuckin died m8! Last target was %s', last_target
                )
                return
