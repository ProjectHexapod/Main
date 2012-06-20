from ControlsKit import time_sources

class Pause:
    def __init__(self, leg_model, limb_controller, duration):
        self.model = leg_model
        self.controller = limb_controller
        self.initial_angles = self.model.getJointAngles()
        self.duration = duration
        self.sw = time_sources.StopWatch();
        self.done = False
    
    def isDone(self):
        return self.done
    
    def update(self):
        self.done = self.sw.getTime() >= self.duration
        return self.initial_angles
