from ControlsKit import time_sources, leg_logger
from ControlsKit.math_utils import normalize, norm, arraysAreEqual


class TrapezoidalJointMove:
    """This is a trapezoidal speed ramp, where speed is derivative foot position WRT time.
        This class expects max velocity for angular velocity.
    """
    def __init__(self, leg_model, limb_controller, final_angles, max_velocity, acceleration):
        logger.info("New path.", path_name="TrapezoidalFootMove",
                    final_angles=final_angles, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.leg = leg_model
        self.controller = limb_controller
        self.target_angles = self.leg.getJointAngles()
        self.final_angles = final_angles
        self.max_vel = max_velocity
        self.vel = 0.0
        self.acc = acceleration
        
        # Set PID gains for this path
        config_file="../ControlsKit/leg_model.conf"
        section="LegModel"
        c = ConfigParser()
        if not path.exists(path.abspath(config_file)):
            print 'Config file %s not found!'%config_file
            raise IOError
        c.read(config_file)
        self.controller.updateGainConstants([c.getfloat(section, "yaw_p"),  # proportional terms
                        c.getfloat(section, "hp_p"),
                        c.getfloat(section, "kp_p")],
        
                        [c.getfloat(section, "yaw_i"),  # integral terms
                        c.getfloat(section, "hp_i"),
                        c.getfloat(section, "kp_i")],
        
                        [c.getfloat(section, "yaw_d"),  # differential terms
                        c.getfloat(section, "hp_d"),
                        c.getfloat(section, "kp_d")] )
        
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
