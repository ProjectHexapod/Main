class PidController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.error_1 = 0.0
        self.integral_error_ki = 0.0

    def update(self, delta_time, desired_pos, measured_pos):
        error = desired_pos - measured_pos

        self.integral_error_ki += self.ki*error * delta_time
        derivative_error = (error - self.error_1) / delta_time

        self.error_1 = error

        return self.kp*error + self.integral_error_ki + self.kd*derivative_error

