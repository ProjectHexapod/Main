import math
from math_utils import saturate
import time_sources

class PidController:
    def __init__(self, kp, ki, kd, soft_min, soft_max):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.soft_min = soft_min
        self.soft_max = soft_max

        self.prev_error = 0.0
        self.integral_error_accumulator = 0.0

    def update(self, desired_pos, measured_pos):
        if math.isnan(desired_pos):
            raise ValueError("PidController: desired_pos cannot be NaN.")
        if math.isnan(measured_pos):
            raise ValueError("PidController: measured_pos cannot be NaN.")

        if self.soft_min > measured_pos or measured_pos > self.soft_max:
            raise ValueError("PidController: Measured position out of soft range!")

        # cap the desired position to the soft range
        desired_pos = saturate(desired_pos, self.soft_min, self.soft_max)

        error = desired_pos - measured_pos

        delta_time = time_sources.global_time.getDelta()
        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = (error - self.prev_error) / delta_time

        self.prev_error = error
        return self.kp * error + self.integral_error_accumulator + self.kd * derivative_error

