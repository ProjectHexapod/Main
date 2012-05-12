from math_utils import *

class PutFootOnGround:
    def __init__(self, legController, velocity):
        self.leg = legController
        self.vel = velocity
        
        self.target_foot_pos = self.leg.getFootPos()

    def isDone(self):
        return self.leg.isFootOnGround()

    def update(self, time, delta_time):
        if not self.isDone():
            self.target_foot_pos[Z] -= self.vel * delta_time
        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)


class TrapezoidalFootMove:
    def __init__(self, leg_controller, final_foot_pos, velocity, acceleration):
        self.leg = leg_controller
        self.initial_foot_pos = self.leg.getFootPos()
        self.final_foot_pos = final_foot_pos
        self.vel = velocity
        self.acc = acceleration
        
        self.done = False

    def isDone(self):
        return self.done

    def update(self, time, deltaTime):
        if not self.done:
            self.done = arraysAreEqual(self.final_foot_pos,
                                       self.leg.getFootPos(), 5e-3)
        return self.leg.jointAnglesFromFootPos(self.final_foot_pos)
