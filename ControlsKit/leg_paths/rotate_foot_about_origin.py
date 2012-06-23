from ControlsKit import time_sources, leg_logger
from ControlsKit.math_utils import normalize, norm, arraysAreEqual
from numpy import arctan

class RotateFootAboutOrigin:
    """This is a trapezoidal speed ramp, where speed is derivative foot position WRT time. 
    """
    def __init__(self, body_model, leg_index, leg_model, limb_controller, final_angle, max_velocity, acceleration):
        leg_logger.logger.info("New path.", path_name="RotateFootAboutOrigin",
                    angle=angle, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.body_model = body_model
        self.leg_index = leg_index
        self.model = leg_model
        self.controller = limb_controller
        self.target_foot_pos = self.model.getFootPos()
        self.final_angle = final_angle
        self.max_vel = max_velocity
        self.vel = 0.0
        self.acc = acceleration
        
        
        
        # Unit vector tangent to the circle
        
        
        # Unit vector pointing towards the destination
        self.dir = self.getNormalizedRemaining()
        self.done = False
     
        self.sw = time_sources.StopWatch()
        self.sw.smoothStart(1)#self.accel_duration)
        # FIXME:the above line should have accel_duration reinstated.

    def isDone(self):
        return self.done

    def getNormalizedTangent(self):
        """Returns a normalized vector that points toward the current goal point.
        """
        return normalize(self.final_angle - arctan(self.target_foot_pos[0]/self.target_foot_pos[1]))

    def update(self):
        if not self.isDone():
            delta = time_sources.global_time.getDelta()
            # if the remaining distance <= the time it would take to slow
            # down times the average speed during such a deceleration (ie
            # the distance it would take to stop)
            
            remaining_vector = self.final_angle - self.target_foot_pos
            if norm(remaining_vector) <= .5 * self.vel**2 / self.acc:
                self.vel -= self.acc * delta
            else:
                self.vel += self.acc * delta
                self.vel = min(self.vel, self.max_vel)
            self.target_foot_pos += self.dir * self.vel * delta
            
            if not arraysAreEqual(self.getNormalizedRemaining(), self.dir):
                self.done = True
                self.target_foot_pos = self.final_foot_pos

        return self.model.jointAnglesFromFootPos(self.target_foot_pos)
