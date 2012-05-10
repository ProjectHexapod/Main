class PidController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def update(self, delta_time, desired_pos, measured_pos):
        return 0.0
