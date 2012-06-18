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
        gains = zip(self.model.DEFAULT_YAW_PID, self.model.DEFAULT_HP_PID, self.model.DEFAULT_KP_PID)
        self.controller.updateGainConstants(gains[0], gains[1], gains[2])
        
    def isDone(self):
        return self.done
    
    def update(self):
        self.done = self.sw.getTime() >= self.duration
        return self.initial_angles
