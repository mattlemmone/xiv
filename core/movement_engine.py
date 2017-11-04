from ctypes.wintypes import c_float
import logging
import math

from core.player import Player
from core.pointers import multi_level_pointers
from core.offsets import entity_base_offsets
from core.structs import Position
from lib.input import KeyboardInput
from lib.memory import write_address

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MovementEngine(object):

    @staticmethod
    def run_to(destination, tolerance=3, key_up=True):
        """
        Primitively runs a straight line (x,y)
        """
        _validate_position(destination)
        position = Player().position

        MovementEngine._rotate(position, destination)
        MovementEngine._run(position, destination, tolerance, key_up)

        logger.debug('arrived')

    @staticmethod
    def run_waypoints(waypoints):
        """
        Primitively runs a straight line (x,y)
        """
        waypoints = list(waypoints)
        last_idx = len(waypoints) - 1
        for idx, waypoint in enumerate(waypoints):
            # Don't lift key up unless last waypoint reached
            MovementEngine.run_to(
                waypoint, tolerance=2, key_up=idx==last_idx
            )

    @staticmethod
    def teleport_to(destination):
        _validate_position(destination)
        pass

    @staticmethod
    def radians_to_heading(radians):
        if -math.pi <= radians <= math.pi/2.0:
            return round(radians + math.pi/2.0, 2)
        return round(radians - (3/2.0 * math.pi), 2)

    @staticmethod
    def heading_to_radians(heading):
        if -math.pi/2 <= heading <= math.pi:
            return round(heading - math.pi/2.0, 2)
        return round(heading + (3/2.0 * math.pi), 2)

    @staticmethod
    def invert_heading(heading):
        if -math.pi <= heading <= 0:
            return round(heading + math.pi, 2)
        return round(heading - math.pi, 2)

    @staticmethod
    def _rotate(position, destination, threshold=0.04):
        logger.debug('rotating')
        radian_diff = -math.atan2(
            destination.y - position.y,
            destination.x - position.x
        )

        next_heading = MovementEngine.radians_to_heading(radian_diff)
        next_heading = round(next_heading, 2)

        logger.debug('converted %f (%d degrees) to %f', radian_diff, math.degrees(radian_diff), next_heading)
        logger.debug('next heading: %f', next_heading)

        # Avoid needless rotate
        if abs(next_heading - position.heading) <= threshold:
            return

        # Write new heading to memory
        heading_address = multi_level_pointers.entity_base.address
        heading_address += entity_base_offsets.heading
        data = c_float(next_heading)
        write_address(heading_address, data)
        KeyboardInput.key_press('a', delay=50)

    @staticmethod
    def _run(position, destination, tolerance, key_up):
        logger.debug('running')
        KeyboardInput.key_down('w')

        distance = float('inf')
        while abs(distance) > tolerance:
            distance = MovementEngine.get_2d_distance(position, destination)
        if key_up:
            KeyboardInput.key_up('w')

    @staticmethod
    def get_2d_distance(start, end):
        distance = math.sqrt((end.x - start.x)**2 + (end.y - start.y)**2)
        return distance


def _validate_position(position):
        assert isinstance(position, Position)
        assert position.x
        assert position.y
        assert position.z


