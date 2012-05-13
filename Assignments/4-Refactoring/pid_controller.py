class PidController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.prev_error = 0.0
        self.prev_response = 0.0
        self.integral_error_accumulator = 0.0

    def update(self, delta_time, desired_pos, measured_pos):
        error = desired_pos - measured_pos

        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = (error - self.prev_error) / delta_time

        self.prev_error = error
        self.prev_response = self.kp * error + self.integral_error_accumulator + self.kd * derivative_error
        return self.prev_response

