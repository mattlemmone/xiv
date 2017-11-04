import logging

from lib.input import KeyboardInput
from core.player import Player

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SkillRotation(object):
    def __init__(self, skill_num_list):
        self.skill_num_list = skill_num_list
        self.executable = 0

    def execute(self):
        player = Player()

        for _ in self.skill_num_list:
            skill_num = self.skill_num_list[self.executable] - 1
            skill = player.skills[skill_num]

            is_buff = skill.type == 0
            has_enough_tp = player.parameters.tp >= skill.tp_cost
            action_exists = skill.class_id != 0

            # It resets to 0 in memory after hitting 100 lol
            is_ready = not 0 < skill.ready_percent < 100

            if not action_exists:
                logger.debug(
                    'action #%d is missing from hotkeys, skipping', skill_num + 1
                )
                self._next_skill()

            if (has_enough_tp or is_buff) and skill.in_range and is_ready:
                KeyboardInput.key_press(str(skill_num + 1))
                self._next_skill()

            elif is_buff and not is_ready:
                self._next_skill()

    def _next_skill(self):
        self.executable += 1
        self.executable %= len(self.skill_num_list)
