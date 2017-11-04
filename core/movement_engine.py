import logging
import math

from core.player import Player
from core.structs import Position
from lib.input import KeyboardInput
from lib.input import MouseInput

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MovementEngine(object):

    @staticmethod
    def run_to(destination, rotate=False, tolerance=2):
        """
        Primitively runs a straight line (x,y)
        """
        _validate_position(destination)
        position = Player().position

        if rotate:
            MovementEngine._rotate(position, destination)
        MovementEngine._run(position, destination, tolerance)

        logger.debug('arrived')

    @staticmethod
    def run_waypoints(waypoints):
        """
        Primitively runs a straight line (x,y)
        """
        for idx, waypoint in enumerate(waypoints):
            MovementEngine.run_to(waypoint, 1)

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
    def _rotate(position, destination):
        logger.debug('rotating')
        radian_diff = -math.atan2(
            destination.y - position.y,
            destination.x - position.x
        )

        next_heading = MovementEngine.radians_to_heading(radian_diff)
        next_heading = round(next_heading, 2)

        logger.debug('converted %f (%d degrees) to %f', radian_diff, math.degrees(radian_diff), next_heading)
        logger.debug('next heading: %f', next_heading)

        # Dont rotate if unnecessary - too awkward
        if abs(position.heading - next_heading) <= 0.02:
            return

        key = 'd'
        if next_heading > position.heading:
            if 0 <= position.heading <= 3.14:
                key = 'a'
        else:
            if -3.14 <= position.heading <= 0:
                key = 'a'

        KeyboardInput.key_down(key)

        while abs(position.heading - next_heading) > 0.02:
            pass
        KeyboardInput.key_up(key)

    @staticmethod
    def _run(position, destination, tolerance):
        logger.debug('running')
        KeyboardInput.key_down('w')

        distance = float('inf')
        while abs(distance) > tolerance:
            distance = MovementEngine.get_2d_distance(position, destination)
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


