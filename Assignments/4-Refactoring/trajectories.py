from math_utils import *
from scipy.linalg import norm
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
        if not self.done and self.leg.isFootOnGround():
            self.done = True
            self.stop_watch.smoothStop(self.accel_duration)
        if not self.isDone():
            self.target_foot_pos[Z] -= self.vel * self.stop_watch.getDelta()
        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)


class TrapezoidalFootMove:
    """This is a trapezoidal speed ramp, where speed is derivative foot position WRT time.
    """
    def __init__(self, leg_controller, final_foot_pos, max_velocity, acceleration):
        self.leg = leg_controller
        self.target_foot_pos = self.leg.getFootPos()
        self.final_foot_pos = final_foot_pos
        self.max_vel = max_velocity
        self.vel = 0
        self.acc = acceleration
        
        # Unit vector pointing towards the destination
        self.dir = self.getNormalizedRemaining()
        #self.stop_watch = time_sources.TimeSource()
        self.done = False

    def isDone(self):
        return self.done# and not self.stop_watch.isActive()

    def getNormalizedRemaining(self):
        """Returns a normalized vector that points toward the current goal point.
        """
        return normalize(self.final_foot_pos - self.target_foot_pos)

    def update(self):
        remaining_vector = self.final_foot_pos - self.target_foot_pos
        if not self.isDone():
            if not arraysAreEqual(self.getNormalizedRemaining(), self.dir):
	        self.done = True
                self.target_foot_pos = self.final_foot_pos
            else:
                delta = time_sources.global_time.getDelta()
                # if the remaining distance <= the time it would take to slow down times the average speed during such a deceleration (ie the distance it would take to stop)
                # rearranged multiplies to avoid confusing order of operations readability issues
                if norm(remaining_vector) <= .5 * self.vel * self.vel / self.acc:
                    self.vel -= self.acc * delta
                else:
                    self.vel += self.acc * delta
                    self.vel = min(self.vel, self.max_vel)
                self.target_foot_pos += self.dir * self.vel * delta
        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)
