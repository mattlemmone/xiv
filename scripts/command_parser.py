import logging
import time
import yaml

from core.client import Client
from core.movement_engine import MovementEngine
from core.player import Player
from core.script_manager import BaseScript
from core.structs import Position

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


YAML_FILE = 'checkpoints.yaml'


# All scripts must inherit from BaseScript
class Script(BaseScript):
    # True by default, even without this next line.
    script_active = True

    # 'run' is the entry point of the script
    @staticmethod
    def run():
        logger.debug('script started')

        client = Client()

        while True:
            last_cmd = client.last_cmd + ''
            if '/save' in last_cmd:
                name = last_cmd[6:]
                save_location(name)
            elif '/load' in last_cmd:
                name = last_cmd[6:]
                load_location(name)
            time.sleep(1 / 1000)


def save_location(name):
    position = Player().position
    with open(YAML_FILE, 'a+') as file:
        yaml_data = yaml.load(file)
        if not yaml_data:
            yaml_data = {
                'fake_map_name': []
            }

        yaml_data['fake_map_name'].append({
            'name': name,
            'x': position.x,
            'y': position.y,
            'z': position.z
        })

    with open(YAML_FILE, 'w') as file:
        logger.debug('saved %s', name)
        yaml.dump(yaml_data, file, default_flow_style=False)


def load_location(name):
    with open(YAML_FILE, 'r') as file:
        yaml_data = yaml.load(file)['fake_map_name']

        location = next(
            coord for coord in yaml_data
            if coord['name'] == name
        )

        if location:
            next_pos = Position(
                location['x'],
                location['y'],
                location['z']
            )

            MovementEngine.teleport_to(next_pos)
