import math

class PidController:
    def __init__(self, kp, ki, kd, soft_min, soft_max):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.soft_min = soft_min
        self.soft_max = soft_max

        self.prev_error = 0.0
        self.prev_response = 0.0
        self.integral_error_accumulator = 0.0

    def update(self, delta_time, desired_pos, measured_pos):
        if delta_time == 0:  # if no time has elapsed the error hasn't changed
            return self.prev_response
        if math.isnan(delta_time):
            raise ValueError("PidController: delta_time cannot be NaN.")
        if math.isnan(desired_pos):
            raise ValueError("PidController: desired_pos cannot be NaN.")
        if math.isnan(measured_pos):
            raise ValueError("PidController: measured_pos cannot be NaN.")

        if self.soft_min > measured_pos or measured_pos > self.soft_max:
            raise ValueError("PidController: Measured position out of soft range!")

        # cap the desired position to the soft range
        desired_pos = max(min(desired_pos, self.soft_max), self.soft_min)

        error = desired_pos - measured_pos

        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = (error - self.prev_error) / delta_time

        self.prev_error = error
        self.prev_response = self.kp * error + self.integral_error_accumulator + self.kd * derivative_error
        return self.prev_response

