from core.movement_engine import MovementEngine
from core.script_manager import BaseScript
from core.structs import Position
from copy import deepcopy
from core.player import Player
import time


class Script(BaseScript):
    script_active = False

    @staticmethod
    def run():
        player = Player()
        old_position = deepcopy(player.position)

        for number in xrange(20):
            MovementEngine.teleport_to(
                Position(
                    x=73-number*20,
                    y=101-number*20,
                    z=5,
                )
            )
            time.sleep(1)

        time.sleep(5)
        MovementEngine.teleport_to(old_position)
