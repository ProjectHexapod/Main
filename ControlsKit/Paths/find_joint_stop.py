from ControlsKit import time_sources


class FindJointStop:
    def __init__(self, leg_model, joint_idx, direction, velocity=0.05, accel_duration=0.1):
        self.leg = leg_model
        self.joint = joint_idx
        self.vel = direction * velocity
        
        self.target_angles = self.leg.getJointAngles()
        self.sw = time_sources.StopWatch()
        self.sw.smoothStart(accel_duration)
        
        self.moving = False
        self.done = False
    
    def isDone(self):
        return self.done
        
    def update(self):
        if self.moving and not self.leg.isMoving():
            self.done = True
        if not self.done:
            self.moving = self.leg.isMoving()
            self.target_angles[self.joint] += self.sw.getDelta() * self.vel
            
        return self.target_angles
