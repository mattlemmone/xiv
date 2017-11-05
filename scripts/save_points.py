import logging
import yaml

from core.entity import get_entity_list
from core.movement_engine import MovementEngine
from core.player import Player
from core.script_manager import BaseScript

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


FILE_OUTPUT = 'checkpoints.yaml'


# All scripts must inherit from BaseScript
class Script(BaseScript):
    # True by default, even without this next line.
    script_active = False

    # 'run' is the entry point of the script
    @staticmethod
    def run():
        logger.debug('script started')
        player = Player()

        save_location(player.position)


def save_location(position):
    with open(FILE_OUTPUT, 'w') as outfile:
        output = {
            'mapname123': [{
                'name': 'test',
                'x': position.x,
                'y': position.y,
                'z': position.z
            },{
                'name': 'test2',
                'x': position.x + 5,
                'y': position.y + 5,
                'z': position.z + 5
            }]
        }

        yaml.dump(output, outfile, default_flow_style=False)


