import logging
import time

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
        player = Player()

        while True:
            logger.debug('Player data: %r', player)
            time.sleep(1)
