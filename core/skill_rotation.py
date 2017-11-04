import logging

from lib.input import KeyboardInput
from core.player import Player

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SkillRotation(object):
    def __init__(self, skill_num_list):
        self.skill_num_list = skill_num_list

    def execute(self):
        player = Player()

        for skill_num in self.skill_num_list:
            skill = player.skills[skill_num - 1]
            has_enough_tp = player.parameters.tp >= skill.tp_cost
            action_exists = skill.class_id != 0

            # It resets to 0 in memory after hitting 100 lol
            is_ready = 0 < skill.ready_percent < 100

            if not action_exists:
                logger.debug(
                    'action #%d is missing from hotkeys, skipping', skill_num
                    )

            if has_enough_tp and skill.in_range and is_ready:
                KeyboardInput.key_press(str(skill_num))
