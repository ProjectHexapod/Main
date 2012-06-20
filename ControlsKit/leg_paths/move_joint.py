from ControlsKit import time_sources

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
