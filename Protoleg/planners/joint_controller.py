import sys
sys.path.append('..')
import math
from ControlsKit import time_sources
from ControlsKit.filters import LowPassFilter
from Utilities.ActuatorCharacteristics import ActuatorMathHelper

gpm2cmps = 1/15850.4

class PistonController:
    """
    Tries to control a valve to match a linear rate.
    """
    def __init__(self, act_char, dead_pos, dead_neg):
        # Valve Tuning
        # Positive and Negative extents of the deadband
        self.dead_pos = dead_pos
        self.dead_neg = dead_neg
        # Piston attributes
        self.act_char = act_char
    def update( self, target_rate, measured_rate=0.0 ):
        """
        TODO: We should put a control loop in here too,
        but for now pure feedforward
        """
        # First calculate desired flow
        if target_rate > 0:
            target_flow = target_rate*self.act_char.getExtensionCrossSectionM2()
        else:
            target_flow = target_rate*self.act_char.getRetractionCrossSectionM2()
        # Then get that flow as a proportion of the valve max flow
        normalized_flow = target_flow / (6.0*gpm2cmps)
        # Then shift and scale based on the deadbands
        if normalized_flow > 0:
            valve_command = (1-self.dead_pos)*normalized_flow + self.dead_pos
        elif normalized_flow < 0:
            valve_command = (1-self.dead_neg)*normalized_flow - self.dead_neg
        else:
            valve_command = 0.0
        if valve_command > 1.0 or valve_command < -1.0:
            print 'PistonController WARNING: someone requested a ridiculous flow rate: %f'%valve_command
            valve_command = valve_command/abs(valve_command)
        return valve_command 

class JointController:
    """
    Produces a linear rate trying to control an angle.
    Requires a description of a joint in the form of an ActuatorMathHelper
    """
    def __init__(self, act_math, kp=0, ki=0, kd=0, kff=None, kfa=None, derivative_corner=10):
        """
        act_math is the ActuatorMathHelper that contains the description of the joint
            and actuator
        kp = proportional gain term
        ki = integral gain term
        kd = derivative gain term
        kff= feed forward velocity term.  Applies signal relative to dervative of the target
        derivative_corner = corner frequency of derivative filter.
        Our real world signals are too noisy to use without significant filtering
        kfa= feed forward acceleration term.  Applies signal relative to the difference in
        rate of change of the target and desired.
        """
        self.act_math = act_math
        self.updateGainConstants(kp, ki, kd, kff, kfa)
        
        # NOTE: it is important that these three variables are floating point to avoid truncation
        self.prev_error = 0.0
        self.prev_desired_ang = 0.0
        self.integral_error_accumulator = 0.0

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

    def update(self, desired_ang, measured_ang):
        delta_time = time_sources.global_time.getDelta()
        
        desired_vel = (desired_ang - self.prev_desired_ang)/delta_time

        error = desired_ang - measured_ang

        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = self.d_lowpass.update((error - self.prev_error) / delta_time)

        velocity_error = desired_vel - derivative_error

        self.prev_error = error
        self.prev_desired_ang = desired_ang
        
        # Calculate a desired angle rate
        target_ang_rate = self.kp * error + self.integral_error_accumulator + self.kd * derivative_error + self.kff*desired_vel + self.kfa*velocity_error
        # Use joint geometry to determine a target piston length rate
        self.act_math.setAngle( measured_ang )
        self.act_math.setAngleRate( target_ang_rate )
        target_length_rate = self.act_math.getLengthRate()

        return target_length_rate

