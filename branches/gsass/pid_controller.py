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
        
        self.max_movement_rate = 100
        
        #Counters/timers and maximum error tracker to check on dynamic stability
        #of the PID controller 
        self.max_error = 0.0
        self.rising_error_time = 0.0
        
        self.max_error_growth_time = 1e9
        self.max_limit_cycle = 1e9

        # NOTE: it is important that these three variables are floating point to avoid truncation
        self.prev_error = 0.0
        self.prev_desired_pos = 0.0
        self.integral_error_accumulator = 0.0
        
        #hysteretic limits for rising/falling edge detection
        self.hyst_low_limit = 0.0
        self.hyst_high_limit = 0.0
        
        self.peak_detector=HystereticPeakDetector(0.0, self.hyst_low_limit,
        self.hyst_high_limit, math.pi/20)

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
        
        #if the requested position changes, reset variables
        #otherwise, update them with new data from this timestep
        if desired_pos==self.prev_desired_pos:
            if abs(error) > self.max_error:
                self.max_error=abs(error)
                #if the error rises, add to the rising error count
                self.rising_error_time+=delta_time
        else:
            self.max_error=abs(error)
            self.rising_error_time=0.0
        if self.rising_error_time >= self.max_error_growth_time:
            raise ValueError("PidController: Maximum error for the desired point"+ 
            "has increased for %d seconds.  System potentially unstable." %
            self.rising_error_time)
        
        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = (error - self.prev_error) / delta_time

        self.prev_error = error
        self.prev_desired_pos = desired_pos
        
        actuator_command = self.kp * error + self.integral_error_accumulator + self.kd * derivative_error
        actuator_command=self.boundActuatorCommand(actuator_command, measured_pos, delta_time)
        
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
            logger.error("PidController.isErrorInBounds: error out of soft bounds.",
                          error=error,
                          measured_pos=measured_pos)
            raise ValueError("Error signal points to a position out of soft bounds.")
        #is error within defined (symmetric) bounds for per-
        if error < -self.max_error or error > self.max_error:
            logger.error("PidController.isErrorInBounds: error out of error bounds.",
                          error=error,
                          max_error = self.max_error,
                          measured_pos=measured_pos)
            raise ValueError("Error signal is outside safe per-timestep bounds.")
        return error
    
    def boundDesiredPosition(self,desired_pos):
		#caps desired position to soft movement range
        bounded_pos=saturate(desired_pos,self.soft_min,self.soft_max)
        return bounded_pos
    
    def boundActuatorCommand(self, actuator_command, measured_pos, delta_time):
        #bound actuator command to available range of command which don't
        #move the actuator outside of available soft range
        soft_min_command=self.soft_min - measured_pos
        soft_max_command=self.soft_max - measured_pos
        actuator_command=saturate(actuator_command,soft_min_command,soft_max_command)
        if abs(actuator_command - measured_pos)/delta_time > self.max_movement_rate:
			raise ValueError("PidController: Actuator command would cause"+
			"joint to move at unsafe rate.")
        return actuator_command

class HystereticPeakDetector:
	def __init__(self, start_value, hyst_low_limit, hyst_high_limit, resolved_threshold):
		#Class Attributes describing the current low/high peaks
		self.peak=start_value
		self.trough=start_value
		
		self.peaks=[]
		self.troughs=[]
		
		self.historylength=100
		
		#Class Attributes to determine when a state transition has happened
		self.hyst_high_limit=hyst_high_limit
		self.hyst_low_limit=hyst_low_limit
		
		#Class Attribute to determine when
		self.resolved_threshold=resolved_threshold
		self.resolved=0
		self.resolvetime=0.0
		
		self.state=0
		
		self.prev_pos=0.0
		
	def reset(self):
		#resets peaks and troughs, while maintaining state for current position
		self.peaks=[]
		self.troughs=[]
		self.peak=self.prev_pos
		self.trough=self.prev_pos
		self.resolved=0
		self.state=0
		
	def update(self, measured_pos, delta_time):
		init_state=0
		rising_edge_state=1
		falling_edge_state=2
		
		if self.state==init_state:
			##INIT STATE - for startup only
			if measured_pos-self.trough>self.hyst_high_limit:
				self.state=rising_edge_state
			elif measured_pos-self.peak<self.hyst_low_limit:
				self.state=falling_edge_state
		elif self.state==rising_edge_state:
			##RISING EDGE STATE
			self.peak=max(self.peak, measured_pos)
			if measured_pos-self.peak<self.hyst_low_limit:
				self.state=falling_edge_state
				self.peaks.append(self.peak)
				#reset trough so it can accumulate properly in next state
				self.trough=measured_pos
		elif self.state==falling_edge_state:
			##FALLING EDGE STATE
			self.trough=min(self.trough, measured_pos)
			if measured_pos-self.trough>self.hyst_high_limit:
				self.state=rising_edge_state
				self.troughs.append(self.trough)
				#reset peak so it can accumulate properly in next state
				self.peak=measured_pos
		
		#truncate peak/trough history
			for i in [self.peaks, self.troughs]:
				if len(i)>self.historylength:
					i.pop(0)
		
		self.resolvetime+=delta_time			
		self.prev_pos=measured_pos
				
	def getPeaks(self):
		return self.peaks
	
	def getTroughs(self):
		return self.troughs
		
	def getState(self):
		return self.state
