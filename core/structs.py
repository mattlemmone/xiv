class Parameters(object):
    def __init__(self):
        self.current_hp = None
        self.max_hp = None
        self.current_mp = None
        self.max_mp = None
        self.tp = None


class Position(object):
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z
        self.heading = None

    def __repr__(self):
        return str(self.__dict__)


class Skill(object):
    def __init__(self):
        self.class_id = None
        self.type = None
        self.skill_id = None
        self.ready_percent = None
        self.tp_cost = None
        self.in_range = None




