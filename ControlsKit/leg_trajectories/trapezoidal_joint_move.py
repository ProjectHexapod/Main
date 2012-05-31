from ControlsKit import time_sources, logger
from ControlsKit.math_utils import normalize, norm, arraysAreEqual


class TrapezoidalJointMove:
    """This is a trapezoidal speed ramp, where speed is derivative foot position WRT time.
        This class expects max velocity for angular velocity.
    """
    def __init__(self, leg_controller, final_angles, max_velocity, acceleration):
        logger.info("New trajectory.", traj_name="TrapezoidalFootMove",
                    final_angles=final_angles, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.leg = leg_controller
        self.target_angles = self.leg.getJointAngles()
        self.final_angles = final_angles
        self.max_vel = max_velocity
        self.vel = 0.0
        self.acc = acceleration
        
        # Unit vector pointing towards the destination
        self.dir = self.getNormalizedRemaining()
        self.done = False

    def isDone(self):
        return self.done

    def getNormalizedRemaining(self):
        """Returns a normalized vector that points toward the current goal point.
        """
        return normalize(self.final_angles - self.target_angles)

    def update(self):
        if not self.isDone():
            delta = time_sources.global_time.getDelta()
            # if the remaining distance <= the time it would take to slow
            # down times the average speed during such a deceleration (ie
            # the distance it would take to stop)
            
            # rearranged multiplies to avoid confusing order of operations
            # readability issues
            remaining_vector = self.final_angles - self.target_angles
            if norm(remaining_vector) <= .5 * self.vel**2 / self.acc:
                self.vel -= self.acc * delta
            else:
                self.vel += self.acc * delta
                self.vel = min(self.vel, self.max_vel)
            self.target_angles += self.dir * self.vel * delta
            
            if not arraysAreEqual(self.getNormalizedRemaining(), self.dir):
                self.done = True
                self.target_angles = self.final_angles

        return self.target_angles
