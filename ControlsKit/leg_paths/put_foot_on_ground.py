from ControlsKit import time_sources, leg_logger
from ControlsKit.math_utils import Z

class PutFootOnGround:
    def __init__(self, leg_model, limb_controller, velocity, accel_duration=0.1):
        leg_logger.logger.info("New trajectory.", traj_name="PutFootOnGround",
                    velocity=velocity, accel_duration=accel_duration)
        
        self.model = leg_model
        self.controller = limb_controller
        self.vel = velocity
        self.accel_duration = accel_duration
        
        self.done = self.model.isFootOnGround()
        self.target_foot_pos = self.model.getFootPos()
        self.stop_watch = time_sources.StopWatch(active=False)
        if not self.done:
            self.stop_watch.smoothStart(self.accel_duration)
    
        self.sw = time_sources.StopWatch()
        self.sw.smoothStart(self.accel_duration)

    def isDone(self):
        return self.done and not self.stop_watch.isActive()

    def update(self):
        if not self.done and self.model.isFootOnGround():
            self.done = True
            self.stop_watch.smoothStop(self.accel_duration)
        if not self.isDone():
            self.target_foot_pos[Z] -= self.vel * self.stop_watch.getDelta()
        return self.model.jointAnglesFromFootPos(self.target_foot_pos)
