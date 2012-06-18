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
        gains = zip(self.model.DEFAULT_YAW_PID, self.model.DEFAULT_HP_PID, self.model.DEFAULT_KP_PID)
        self.controller.updateGainConstants(gains[0], gains[1], gains[2])
    
    def isDone(self):
        return self.done
        
    def update(self):
        if self.moving and not self.model.isMoving():
            self.done = True
        if not self.done:
            self.moving = self.model.isMoving()
            self.target_angles[self.joint] += self.sw.getDelta() * self.vel
            
        return self.target_angles
