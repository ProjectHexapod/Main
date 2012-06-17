from ControlsKit import time_sources
from ConfigParser import ConfigParser
from os import path

class FindJointStop:
    def __init__(self, leg_model, limb_controller, joint_idx, direction, velocity=0.05, accel_duration=0.1):
        self.model = leg_model
        self.controller = limb_controller
        self.joint = joint_idx
        self.vel = direction * velocity
        
        self.target_angles = self.model.getJointAngles()
        self.sw = time_sources.StopWatch()
        self.sw.smoothStart(accel_duration)
        
        self.moving = False
        self.done = False
                
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
    
    def isDone(self):
        return self.done
        
    def update(self):
        if self.moving and not self.model.isMoving():
            self.done = True
        if not self.done:
            self.moving = self.model.isMoving()
            self.target_angles[self.joint] += self.sw.getDelta() * self.vel
            
        return self.target_angles
