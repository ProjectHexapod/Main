from ControlsKit import time_sources, leg_logger
from ControlsKit.math_utils import normalize, norm, arraysAreEqual, rotateZ, array
from numpy import arctan, sign, pi

class RotateFootAboutOrigin:
    """This is a trapezoidal speed ramp, where speed is derivative foot position WRT time. 
    """
    def __init__(self, body_model, leg_index, leg_model, limb_controller, delta_angle, max_velocity, acceleration):
        leg_logger.logger.info("New path.", path_name="RotateFootAboutOrigin",
                    delta_angle=delta_angle, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.body_model = body_model
        self.leg_index = leg_index
        self.leg_model = leg_model
        self.controller = limb_controller
        self.target_foot_pos = self.leg_model.getFootPos()
        self.delta_angle = delta_angle
        self.remaining_angle = self.delta_angle
        self.max_vel = max_velocity
        self.vel = 0.0
        self.acc = acceleration
        self.body_coord = body_model.transformLeg2Body(self.leg_index, self.target_foot_pos)
        self.init_angle = arctan(self.body_coord[0]/self.body_coord[1])
        
        # Unit vector tangent to the circle
        self.tan = self.getNormalizedTangent()
        
        # Unit vector pointing towards the destination
        self.dir = sign(self.init_angle + self.delta_angle - arctan(self.body_coord[0]/self.body_coord[1]))
        self.done = False
     
        self.sw = time_sources.StopWatch()
        self.sw.smoothStart(1)#self.accel_duration)
        # FIXME:the above line should have accel_duration reinstated.

    def isDone(self):
        return self.done
    
    def getNormalizedTangent(self):
        """Returns a normalized tangent vector
        """
        body_tan = normalize(rotateZ(self.body_coord, pi/2))
        return rotateZ(body_tan,self.body_model.getHipOffset(self.leg_index)[2])

    def update(self):
        if not self.isDone():
            delta = time_sources.global_time.getDelta()
            # if the remaining distance <= the time it would take to slow
            # down times the average speed during such a deceleration (ie
            # the distance it would take to stop)
            
            self.body_coord = self.body_model.transformLeg2Body(self.leg_index, self.target_foot_pos)
            self.tan = self.getNormalizedTangent()

            self.remaining_angle = self.init_angle + self.delta_angle - arctan(self.body_coord[0]/self.body_coord[1])
            
            if self.remaining_angle*norm([self.body_coord[0],self.body_coord[1],0]) <= .5 * self.vel**2 / self.acc:
                self.vel -= self.acc * delta
            else:
                self.vel += self.acc * delta
                self.vel = min(self.vel, self.max_vel)
            self.target_foot_pos += sign(self.remaining_angle) * self.tan * self.vel * delta
            
            if not sign(self.remaining_angle) == self.dir:
                self.done = True
                #self.target_foot_pos = self.final_foot_pos

        return self.leg_model.jointAnglesFromFootPos(self.target_foot_pos)
