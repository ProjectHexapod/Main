from ControlsKit import time_sources
from ControlsKit.math_utils import normalize, norm, arraysAreEqual
#from UI import logger


class TrapezoidalFootMove:
    """
    This is a trapezoidal speed ramp, where speed is derivative foot position WRT time. 
    """
    def __init__(self, leg_model, limb_controller, final_foot_pos, max_velocity, acceleration):
        #logger.info("New trajectory.", traj_name="TrapezoidalFootMove",
        #            final_foot_pos=final_foot_pos, max_velocity=max_velocity,
        #            acceleration=acceleration)
        
        self.model = leg_model
        self.controller = limb_controller
        # We want to start from the last commanded foot position,
        # not the last actual foot position.  However, this is not always
        # possible, since a position command may not have been given before this
        # point.
        last_target_ang_array = self.controller.getDesiredPosAngle()
        # If positions have been commanded to the controller
        if last_target_ang_array != None:
            # Base the starting position off that command
            self.target_foot_pos = self.model.footPosFromLegState(\
                (last_target_ang_array, 0.0))
        else:
            # Base the starting position on the position of the model
            self.target_foot_pos = self.model.getFootPos()
        self.final_foot_pos = final_foot_pos
        self.max_vel = max_velocity
        self.vel = 0.0
        self.acc = acceleration
        
        self.start_on_ground = self.model.isFootOnGround()
        
        # Unit vector pointing towards the destination
        self.dir = self.getNormalizedRemaining()
        self.done = False

    def isDone(self):
        return self.done

    def getNormalizedRemaining(self):
        """Returns a normalized vector that points toward the current goal point.
        """
        return normalize(self.final_foot_pos - self.target_foot_pos)

    def update(self):
        #if not self.isDone() and (self.start_on_ground or not self.model.isFootOnGround()):
        if not self.isDone():
            delta = time_sources.global_time.getDelta()
            # if the remaining distance <= the time it would take to slow
            # down times the average speed during such a deceleration (ie
            # the distance it would take to stop)
            
            # rearranged multiplies to avoid confusing order of operations
            # readability issues
            remaining_vector = self.final_foot_pos - self.target_foot_pos
            if norm(remaining_vector) <= .5 * self.vel ** 2 / self.acc:
                self.vel -= self.acc * delta
            else:
                self.vel += self.acc * delta
                self.vel = min(self.vel, self.max_vel)
            self.target_foot_pos += self.dir * self.vel * delta
            if norm(self.final_foot_pos - self.target_foot_pos) < 0.02:
                self.done = True
        else:
            self.done = True
            

        return self.model.jointAnglesFromFootPos(self.target_foot_pos, 0)
