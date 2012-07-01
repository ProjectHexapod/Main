from ControlsKit.math_utils import array, saturate
from ControlsKit.time_sources import global_time

class FootVelocity:
    def __init__(self, leg_model,
                 max_acceleration=array([20.0, 20.0, 20.0]),
                 initial_velocity=None,
                 initial_position=None,
                 time_source=global_time):
        self.model = leg_model
        self.setMaxAcceleration(max_acceleration)
        self.ts = time_source
        
        if initial_velocity is None:
            self.vel = array([0.0, 0.0, 0.0])
        else:
            self.vel = initial_velocity
        if initial_position is None:
            self.pos = self.model.getFootPos()
        else:
            self.pos = initial_position
            
        self.setVelocity(self.vel)
    
    def setMaxAcceleration(self, max_acceleration):
        self.max_accel = max_acceleration
    def setVelocity(self, target_velocity):
        self.target_vel = target_velocity
    
    def isDone(self):
        return False
    def update(self):
        dt = self.ts.getDelta()
        for i in range(len(self.vel)):
            target_accel = (self.target_vel[i] - self.vel[i]) / dt
            self.vel[i] += saturate(target_accel, self.max_accel[i]) * dt
            self.pos[i] += self.vel[i] * dt
        return self.model.jointAnglesFromFootPos(self.pos)
