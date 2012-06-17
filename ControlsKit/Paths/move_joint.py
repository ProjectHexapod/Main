from ControlsKit import time_sources
from ConfigParser import ConfigParser
from os import path


class MoveJoint:
    def __init__(self, leg_model, limb_controller, joint_idx, duration, direction, velocity=0.1, accel_duration=0.1):
        assert abs(direction) == 1
        
        self.model = leg_model
        self.controller = limb_controller
        self.joint = joint_idx
        self.duration = duration
        self.vel = direction * velocity
        self.accel_duration = accel_duration
        
        self.target_angles = self.model.getJointAngles()
        self.stopping = False
        
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
        
        self.sw = time_sources.StopWatch()
        self.sw.smoothStart(self.accel_duration)
        
    def isDone(self):
        return not self.sw.isActive()
    
    def update(self):
        if not self.isDone():
            self.target_angles[self.joint] += self.sw.getDelta() * self.vel
            if not self.stopping and self.sw.getTime() >= self.duration:
                self.sw.smoothStop(self.accel_duration)
                self.stopping = True
        return self.target_angles
