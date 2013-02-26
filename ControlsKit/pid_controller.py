#from UI import logger
import math
from math_utils import saturate
import time_sources
from hysteretic_peak_detector import HystereticPeakDetector
from filters import LowPassFilter

class PIDController:
    def __init__(self, kp=0, ki=0, kd=0, kff=None, kfa=None, derivative_corner=10):
        """
        kp = proportional gain term
        ki = integral gain term
        kd = derivative gain term
        kff= feed forward velocity term.  Applies signal relative to dervative of the target
        derivative_corner = corner frequency of derivative filter.
        Our real world signals are too noisy to use without significant filtering
        kfa= feed forward acceleration term.  Applies signal relative to the difference in
        rate of change of the target and desired.
        """
        self.updateGainConstants(kp, ki, kd, kff, kfa)
        
        self.max_movement_rate = 1e6

        # NOTE: it is important that these three variables are floating point to avoid truncation
        self.prev_error = 0.0
        self.prev_desired_pos = 0.0
        self.integral_error_accumulator = 0.0
        
        self.peak_detector=HystereticPeakDetector(0.0, -1.0,
        1.0, math.pi/20)

        self.d_lowpass = LowPassFilter( gain=1.0, corner_frequency=derivative_corner )

    def updateGainConstants(self, kp, ki, kd, kff = None, kfa=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        if kff != None:
            self.kff = kff
        else:
            self.kff = 0.0
        if kfa != None:
            self.kfa = kfa
        else:
            self.kfa = 0.0

    def update(self, desired_pos, measured_pos):
        delta_time = time_sources.global_time.getDelta()
        
        # bound the desired position
        desired_pos = self.boundDesiredPosition(desired_pos)

        desired_vel = (desired_pos - self.prev_desired_pos)/delta_time

        error = desired_pos - measured_pos

        self.peak_detector.update(error)
        
        if self.peak_detector.hasConverged():
            if self.peak_detector.isUnstable():
                warningstring=("LimbController: Maximum error for the"+
                        " desired point has increased for %d seconds,"+
                        " but is within converged range.  Might be unstable." %
                        self.peak_detector.getResolveTime() )
                #logger.warning(warningstring,
                #        desired_pos=desired_pos,
                #        measured_pos=measured_pos,
                #        error=error, 
                #        bad_value=error)
            elif self.peak_detector.isLimitCycle():
                warningstring=("LimbController: Maximum error for the"+
                        " desired point has increased once or more for %d seconds,"+
                        " but is within converged range.  Might be unstable." %
                        self.peak_detector.getResolveTime() )
                #logger.warning(warningstring,
                #        desired_pos=desired_pos,
                #        measured_pos=measured_pos,
                #        error=error,
                #        bad_value=error)
        else:
            if self.peak_detector.isUnstable():
                errorstring=("LimbController: Maximum error for the desired point"+ 
                        "has increased for %d seconds.  System potentially unstable." %
                        self.peak_detector.getResolveTime() )
                #logger.error(errorstring,
                #        desired_pos=desired_pos,
                #        measured_pos=measured_pos,
                #        error=error,
                #        bad_value=error)
                raise ValueError(errorstring)
            elif self.peak_detector.isLimitCycle():
                errorstring=("LimbController: Controller has not converged"+ 
                "over %d seconds.  System potentially in a limit cycle." %
                self.peak_detector.getResolveTime() )
                #logger.error(errorstring,
                #        desired_pos=desired_pos,
                #        measured_pos=measured_pos,
                #        error=error,
                #        bad_value=error)
                raise ValueError(errorstring)
        
        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = self.d_lowpass.update((error - self.prev_error) / delta_time)

        velocity_error = desired_vel - derivative_error

        self.prev_error = error
        self.prev_desired_pos = desired_pos
        
        actuator_command = self.kp * error + self.integral_error_accumulator + self.kd * derivative_error + self.kff*desired_vel + self.kfa*velocity_error
        actuator_command = self.boundActuatorCommand(actuator_command, measured_pos)
        
        return actuator_command

    def isErrorInBounds(self, error, measured_pos):
        """tests whether or not the error signal is within reasonable range
        not checking for NaN, since both desired and measured position
        are tested for that
        """
        
        #makes sure the error is bounded by a single leg rotation
        error = error%(2*math.pi)
        error_min = -math.pi/2
        error_max = math.pi/2
        
        #is error within available soft range?
        if error>(measured_pos-error_min) or error>(error_max-measured_pos):
            #logger.error("LimbController.isErrorInBounds: error out of soft bounds.",
            #            error=error,
            #            measured_pos=measured_pos)
            raise ValueError("Error signal points to a position out of soft bounds.")
        return error
    
    def boundDesiredPosition(self,desired_pos):
        #caps desired position to soft movement range
        if math.isnan(desired_pos):
            #logger.error("LimbController.boundDesiredPosition: NaN where aN expected!",
            #            desired_pos=desired_pos,
            #            bad_value="desired_pos")
            raise ValueError("LimbController: desired_pos cannot be NaN.")
        
        command_min=-20
        command_max=20
        
        if desired_pos<command_min or desired_pos>command_max:
            #logger.error("LimbController.boundDesiredPosition:"+
            #            " desired position out of bounds!",
            #            desired_pos=desired_pos,
            #            command_min=command_min,
            #            command_max=command_max,
            #            bad_value="desired_pos")
            raise ValueError("LimbController.boundDesiredPosition:"+
                    " desired position out of soft bounds")
        
        bounded_pos=saturate(desired_pos,command_min,command_max)
        return bounded_pos
    
    def boundActuatorCommand(self, actuator_command, measured_pos):
        #prevent the controller from commanding an unsafely fast actuator move
        if ( abs(actuator_command - measured_pos)/
                time_sources.global_time.getDelta() > self.max_movement_rate):
            raise ValueError("LimbController: Actuator command would cause"+
            "joint to move at an unsafe rate.")
        return actuator_command
