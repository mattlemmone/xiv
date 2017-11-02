import logging
import time
from script_manager import BaseScript

from player import Player

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Script(BaseScript):
    script_active = True

    @staticmethod
    def run():
        player = Player()

        while True:
            logger.debug('Player hp: %d', player.parameters.current_hp)
            time.sleep(1)
