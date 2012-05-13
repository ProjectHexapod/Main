from math_utils import *
import time_sources


class PutFootOnGround:
    def __init__(self, legController, velocity):
        self.leg = legController
        self.vel = velocity
        
        self.target_foot_pos = self.leg.getFootPos()
        self.done = False

    def isDone(self):
        return self.done

    def update(self):
        if not self.isDone():
            if self.leg.isFootOnGround():
                self.done = True
            else:
                self.target_foot_pos[Z] -= self.vel * time_sources.global_time.getDelta()
        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)


class TrapezoidalFootMove:
    def __init__(self, leg_controller, final_foot_pos, velocity, acceleration):
        self.leg = leg_controller
        self.target_foot_pos = self.leg.getFootPos()
        self.final_foot_pos = final_foot_pos
        self.vel = velocity
        self.acc = acceleration
        
        # Unit vector pointing towards the destination
        self.dir = normalize(self.final_foot_pos - self.target_foot_pos)
        
        self.done = False

    def isDone(self):
        return self.done

    def update(self):
        if not self.done:
            # Have we passed the destination?
            if not arraysAreEqual(normalize(self.final_foot_pos - self.target_foot_pos),
                              self.dir):
                self.done = True
                self.target_foot_pos = self.final_foot_pos
            else:
                self.target_foot_pos += self.dir * self.vel * time_sources.global_time.getDelta()
        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)
