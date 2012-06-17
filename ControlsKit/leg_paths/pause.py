from ControlsKit import time_sources
from ConfigParser import ConfigParser
from os import path


class Pause:
    def __init__(self, leg_model, limb_controller, duration):
        self.model = leg_model
        self.controller = limb_controller
        self.initial_angles = self.model.getJointAngles()
        self.duration = duration
        self.sw = time_sources.StopWatch();
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
        self.done = self.sw.getTime() >= self.duration
        return self.initial_angles
