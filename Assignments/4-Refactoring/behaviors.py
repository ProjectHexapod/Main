from math_utils import *
import time_sources


class PutFootOnGround:
    def __init__(self, legController, velocity, accel_duration=0.1):
        self.leg = legController
        self.vel = velocity
        self.accel_duration = accel_duration
        
        self.done = self.leg.isFootOnGround()
        self.target_foot_pos = self.leg.getFootPos()
        self.stop_watch = time_sources.StopWatch(active=False)
        if not self.done:
            self.stop_watch.smoothStart(self.accel_duration)

    def isDone(self):
        return self.done and not self.stop_watch.isActive()

    def update(self):
        if not self.done and not self.leg.isFootOnGround():
            self.done = True
            self.stop_watch.smoothStop(self.accel_duration)
        if not self.isDone():
            self.target_foot_pos[Z] -= self.vel * time_sources.global_time.getDelta()
        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)


class TrapezoidalFootMove:
    """This is a trapezoidal speed ramp, where speed is derivative foot position WRT time.
    """
    def __init__(self, leg_controller, final_foot_pos, velocity, acceleration):
        self.leg = leg_controller
        self.current_foot_pos = self.leg.getFootPos()
        self.final_foot_pos = final_foot_pos
        self.vel = velocity
        self.acc = acceleration
        
        # Unit vector pointing towards the destination
        self.dir = self.getNormalizedRemaining()
        
        self.done = False

    def isDone(self):
        return self.done

    def getNormalizedRemaining(self):
        """Returns a normalized vector that points toward the current goal point.
        """
        return normalize(self.final_foot_pos - self.current_foot_pos)

    def update(self):
        if not self.done:
            # Have we passed the destination?
            if not arraysAreEqual(self.getNormalizedRemaining(), self.dir):
                self.done = True
                self.target_foot_pos = self.final_foot_pos
            else:
                self.target_foot_pos += self.dir * self.vel * time_sources.global_time.getDelta()
        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)
