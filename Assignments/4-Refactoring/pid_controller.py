from leg_logger import logger
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
        
        self.max_error = 100

        # NOTE: it is important that these three variables are floating point to avoid truncation
        self.prev_error = 0.0
        self.integral_error_accumulator = 0.0

    def update(self, desired_pos, measured_pos):
        if math.isnan(desired_pos):
            logger.error("PidController.update: NaN where aN expected!",
                         desired_pos=desired_pos,
                         measured_pos=measured_pos,
                         soft_min=self.soft_min,
                         soft_max=self.soft_max,
                         bad_value="desired_pos")
            raise ValueError("PidController: desired_pos cannot be NaN.")
        if math.isnan(measured_pos):
            logger.error("PidController.update: NaN where aN expected!",
                         desired_pos=desired_pos,
                         measured_pos=measured_pos,
                         soft_min=self.soft_min,
                         soft_max=self.soft_max,
                         bad_value="measured_pos")
            raise ValueError("PidController: measured_pos cannot be NaN.")

        if self.soft_min > measured_pos or measured_pos > self.soft_max:
            logger.error("PidController.update: Measured position outside of soft range!",
                         desired_pos=desired_pos,
                         measured_pos=measured_pos,
                         soft_min=self.soft_min,
                         soft_max=self.soft_max,
                         bad_value=measured_pos)
            raise ValueError("PidController: Measured position out of soft range!")

        # bound the desired position
        desired_pos = self.boundDesiredPosition(desired_pos)

        error = desired_pos - measured_pos

        delta_time = time_sources.global_time.getDelta()
        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = (error - self.prev_error) / delta_time

        self.prev_error = error
        
        actuator_command = self.kp * error + self.integral_error_accumulator + self.kd * derivative_error
        actuator_command=self.boundActuatorCommand(actuator_command, measured_pos)
        
        return actuator_command

    def isErrorInBounds(self, error, measured_pos):
        """tests whether or not the error signal is within reasonable range
        not checking for NaN, since both desired and measured position
        are tested for that
        """
        
        #makes sure the error is bounded by a single leg rotation
        error = error%(2*math.pi)
        
        #is error within available soft range?
        if error>(measured_pos-self.soft_min) or error>(self.soft_max-measured_pos):
            logging.error("PidController.isErrorInBounds: error out of soft bounds.",
                          error=error,
                          measured_pos=measured_pos)
            raise ValueError("Error signal points to a position out of soft bounds.")
        #is error within defined (symmetric) bounds for per-
        if error < -self.max_error or error > self.max_error:
            logging.error("PidController.isErrorInBounds: error out of error bounds.",
                          error=error,
                          max_error = self.max_error,
                          measured_pos=measured_pos)
            raise ValueError("Error signal is outside safe per-timestep bounds.")
        return error
    
    def boundDesiredPosition(self,desired_pos):
		#caps desired position to soft movement range
        bounded_pos=saturate(desired_pos,self.soft_min,self.soft_max)
        return bounded_pos
    
    def boundActuatorCommand(self,actuator_command, measured_pos):
        #bound actuator command to available range of command which don't
        #move the actuator outside of available soft range
        soft_min_command=self.soft_min - measured_pos
        soft_max_command=self.soft_max - measured_pos
        return saturate(actuator_command,soft_min_command,soft_max_command)
