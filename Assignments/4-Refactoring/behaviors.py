from math_utils import *

class PutFootOnGround:
    def __init__(self, legController, velocity):
        self.leg = legController
        self.vel = velocity
        
        self.foot_pos = self.leg.getFootPos()

    def isDone(self):
        return self.leg.isFootOnGround()

    def update(self, time, delta_time):
        if not self.isDone():
            self.foot_pos[Z] -= self.vel * delta_time
        return self.leg.jointAnglesFromFootPos(self.foot_pos)


class TrapezoidalFootMove:
    def __init__(self, leg_controller, target_foot_pos, velocity, acceleration):
        self.leg = leg_controller
        self.targetFootPos = target_foot_pos
        self.velocity = velocity
        self.acceleration = aceleration

    def isDone(self):
        return False

    def update(self, time):
        return self.leg.getJointAngles()
