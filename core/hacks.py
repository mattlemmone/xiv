from ctypes.wintypes import c_float

from core.offsets import client_offsets
from core.pointers import multi_level_pointers
from core.pointers import single_level_pointers
from lib.memory import write_address

JUMP_GRAV = -2.00
JUMP_DIR_PULL = 20


class Hacks(object):
    """
    Necessary workaround to tie setters/getters to Client
    """
    def __init__(self):
        self._jump_dir_1 = 0.0
        self._jump_dir_2 = 0.0
        self._jump_grav_start = 0.0
        self._player_speed = 6.0
        self._has_updated_jump_pull = {
            '1': False,
            '2': False
        }

    @property
    def player_speed(self):
        return self._player_speed

    @player_speed.setter
    def player_speed(self, new_speed):
        if new_speed != self._player_speed:
            writable_address = single_level_pointers.player_speed.address
            data = c_float(self.player_speed)
            write_address(writable_address, data)

    @property
    def jump_grav_start(self):
        return self._jump_grav_start

    @jump_grav_start.setter
    def jump_grav_start(self, new_grav):

        self._jump_grav_start = new_grav
        # Reset grav every time player lands
        if new_grav == 0.00:
            writable_address = multi_level_pointers.entity_base.address
            writable_address += client_offsets.jump_grav_start
            data = c_float(JUMP_GRAV)
            # write_address(writable_address, data)

    @property
    def jump_dir_1(self):
        return self._jump_dir_1

    @jump_dir_1.setter
    def jump_dir_1(self, new_dir):
        self._jump_dir_1 = self._write_jump_dir(new_dir, 1)

    @property
    def jump_dir_2(self):
        return self._jump_dir_2

    @jump_dir_2.setter
    def jump_dir_2(self, new_dir):
        self._jump_dir_2 = self._write_jump_dir(new_dir, 2)

    def _write_jump_dir(self, new_dir, jump_num):
        # Reset grav every time player lands
        jump_num = str(jump_num)
        player_jumping = self._jump_grav_start != 0
        already_updated_jump_pull = self._has_updated_jump_pull[jump_num]

        if player_jumping and not already_updated_jump_pull:
            new_dir *= JUMP_DIR_PULL
            writable_address = multi_level_pointers.entity_base.address
            writable_address += client_offsets['jump_dir_' + jump_num]
            data = c_float(new_dir)
            write_address(writable_address, data)
            self._has_updated_jump_pull[jump_num] = True
        elif not player_jumping:
            print 'reset'
            self._has_updated_jump_pull[jump_num] = False

        return new_dir
