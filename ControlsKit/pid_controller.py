from leg_logger import logger
import math
from math_utils import saturate
import time_sources
import scipy

class PidController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.max_movement_rate = 1e6

        # NOTE: it is important that these three variables are floating point to avoid truncation
        self.prev_error = 0.0
        self.prev_desired_pos = 0.0
        self.integral_error_accumulator = 0.0
        
        self.peak_detector=HystereticPeakDetector(0.0, -1.0,
        1.0, math.pi/20)

    def update(self, desired_pos, measured_pos):
        
        # bound the desired position
        desired_pos = self.boundDesiredPosition(desired_pos)

        error = desired_pos - measured_pos
        delta_time = time_sources.global_time.getDelta()

        self.peak_detector.update(error)
        
        if self.peak_detector.hasConverged():
            if self.peak_detector.isUnstable():
                warningstring=("PidController: Maximum error for the"+
                        " desired point has increased for %d seconds,"+
                        " but is within converged range.  Might be unstable." %
                        self.peak_detector.getResolveTime() )
                logger.warning(warningstring,
                        desired_pos=desired_pos,
                        measured_pos=measured_pos,
                        error=error, 
                        bad_value=error)
            elif self.peak_detector.isLimitCycle():
                warningstring=("PidController: Maximum error for the"+
                        " desired point has increased once or more for %d seconds,"+
                        " but is within converged range.  Might be unstable." %
                        self.peak_detector.getResolveTime() )
                logger.warning(warningstring,
                        desired_pos=desired_pos,
                        measured_pos=measured_pos,
                        error=error,
                        bad_value=error)
        else:
            if self.peak_detector.isUnstable():
                errorstring=("PidController: Maximum error for the desired point"+ 
                        "has increased for %d seconds.  System potentially unstable." %
                        self.peak_detector.getResolveTime() )
                logger.error(errorstring,
                        desired_pos=desired_pos,
                        measured_pos=measured_pos,
                        error=error,
                        bad_value=error)
                raise ValueError(errorstring)
            elif self.peak_detector.isLimitCycle():
                errorstring=("PidController: Controller has not converged"+ 
                "over %d seconds.  System potentially in a limit cycle." %
                self.peak_detector.getResolveTime() )
                logger.error(errorstring,
                        desired_pos=desired_pos,
                        measured_pos=measured_pos,
                        error=error,
                        bad_value=error)
                raise ValueError(errorstring)
        
        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = (error - self.prev_error) / delta_time

        self.prev_error = error
        self.prev_desired_pos = desired_pos
        
        actuator_command = self.kp * error + self.integral_error_accumulator + self.kd * derivative_error
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
            logger.error("PidController.isErrorInBounds: error out of soft bounds.",
                        error=error,
                        measured_pos=measured_pos)
            raise ValueError("Error signal points to a position out of soft bounds.")
        return error
    
    def boundDesiredPosition(self,desired_pos):
        #caps desired position to soft movement range
        if math.isnan(desired_pos):
            logger.error("PidController.boundDesiredPosition: NaN where aN expected!",
                        desired_pos=desired_pos,
                        bad_value="desired_pos")
            raise ValueError("PidController: desired_pos cannot be NaN.")
        
        command_min=-20
        command_max=20
        
        if desired_pos<command_min or desired_pos>command_max:
            logger.error("PidController.boundDesiredPosition:"+
                        " desired position out of bounds!",
                        desired_pos=desired_pos,
                        command_min=command_min,
                        command_max=command_max,
                        bad_value="desired_pos")
            raise ValueError("PidController.boundDesiredPosition:"+
                    " desired position out of soft bounds")
        
        bounded_pos=saturate(desired_pos,command_min,command_max)
        return bounded_pos
    
    def boundActuatorCommand(self, actuator_command, measured_pos):
        #prevent the controller from commanding an unsafely fast actuator move
        if ( abs(actuator_command - measured_pos)/
                time_sources.global_time.getDelta() > self.max_movement_rate):
            raise ValueError("PidController: Actuator command would cause"+
            "joint to move at an unsafe rate.")
        return actuator_command

class HystereticPeakDetector:
    def __init__(self, start_value, hyst_low_limit, hyst_high_limit, convergence_level):
        self.historylength=100
        
        #Class Attributes to determine when a state transition has happened
        if not (hyst_low_limit < hyst_high_limit):
            raise ValueError("HystereticPeakDetector: Can't instantiate with"+
                    " a hysteretic low bound greater than the hyst. high bound!")
        self.hyst_high_limit=hyst_high_limit
        self.hyst_low_limit=hyst_low_limit
        
        self.NO_EDGE_DETECTED=0
        self.RISING_EDGE=1
        self.FALLING_EDGE=2
        
        #Class Attribute to determine when
        self.convergence_level=convergence_level
        
        self.prev_pos=start_value
        
        self.reset()
                    
    def reset(self):
        #resets peaks and troughs, while maintaining state for current position
        self.peaks=[]
        self.troughs=[]
        self.peak=self.prev_pos
        self.trough=self.prev_pos
        self.edgetype=0
        self.resolve_time=0.0
        
        #Dictionary of flags for different potential system states
        self.flags={"unstable":False,
                    "limit_cycle":False,
                    "converging":False,
                    "converged":False}

    def isUnstable(self):
        return self.flags["unstable"]
    
    def isLimitCycle(self):
        return self.flags["limit_cycle"]
    
    def isConverging(self):
        return self.flags["converging"]
    
    def hasConverged(self):
        return self.flags["converged"]
        
    def update(self, current_pos):
        
        if self.edgetype==self.NO_EDGE_DETECTED:
            ##INIT STATE - for startup only
            if current_pos-self.trough>self.hyst_high_limit:
                self.edgetype=self.RISING_EDGE
            elif current_pos-self.peak<self.hyst_low_limit:
                self.edgetype=self.FALLING_EDGE
        elif self.edgetype==self.RISING_EDGE:
            ##RISING EDGE STATE
            self.peak=max(self.peak, current_pos)
            if current_pos-self.peak<self.hyst_low_limit:
                self.edgetype=self.FALLING_EDGE
                self.peaks.append(self.peak)
                #reset trough so it can accumulate properly in next state
                self.trough=current_pos
        elif self.edgetype==self.FALLING_EDGE:
            ##FALLING EDGE STATE
            self.trough=min(self.trough, current_pos)
            if current_pos-self.trough>self.hyst_high_limit:
                self.edgetype=self.RISING_EDGE
                self.troughs.append(self.trough)
                #reset peak so it can accumulate properly in next state
                self.peak=current_pos
        
        #truncate peak/trough history
            for i in [self.peaks, self.troughs]:
                if len(i)>self.historylength:
                    i.pop(0)
        
        self.resolve_time+=time_sources.global_time.getDelta()			
        self.prev_pos=current_pos
        
        #check for resolution, instability, limit cycles
        self.updateStates()
    
    def updateStates(self):
        peak_deltas = scipy.diff(self.peaks)
        trough_deltas = scipy.diff(self.troughs)
        
        peak_envelope = self.envelopeFromArray(self.peaks)
        trough_envelope = self.envelopeFromArray([-trough for trough in self.troughs])
        
        peak_envelope_deltas= scipy.diff(peak_envelope)
        trough_envelope_deltas= scipy.diff(trough_envelope)
        envelope_detected=(len(peak_envelope_deltas) > 0 and
                            len(trough_envelope_deltas) > 0)
        
        [unstable, limit_cycle, converging, converged]=[True, True, True, True]
        
        if len(self.peaks) > 1 and len(self.troughs) > 1:
            #only unstable if error always rises
            unstable = ( (peak_deltas > 0.0).all() or 
                        (trough_deltas < 0.0).all()
                        or (envelope_detected and
                            (peak_envelope_deltas > 0.0).all() and
                            (trough_envelope_deltas > 0.0).all() ) 
                        )
            #only converging if error is always decreasing
            converging = ( ( (peak_deltas < 0.0).all() and (trough_deltas > 0.0).all() )
                        or (envelope_detected and
                            (peak_envelope_deltas < 0.0).all() and 
                            (trough_envelope_deltas < 0.0).all() ) 
                        )
            #in a limit cycle if error ever rises
            limit_cycle = not converging and not unstable
        else:
            [unstable, limit_cycle, converging] = [False, False, False]
            
        #only converged if both final peak and trough are below
        #converged threshold
        if len(self.peaks) > 0 and len(self.troughs) > 0:
            converged=( (self.peaks[-1] < self.convergence_level) and
                    (self.troughs[-1] > -self.convergence_level) )
        else:
            converged=False
        self.flags["unstable"]=unstable
        self.flags["limit_cycle"]=limit_cycle
        self.flags["converging"]=converging
        self.flags["converged"]=converged

    def envelopeFromArray(self, array):
        envelope=[]
        diffs=scipy.diff(array)
        #identifies envelope peaks via first derivative
        for index in range( 1,len(diffs) ):
            if diffs[index] <= 0 and diffs[index-1] >= 0:
                envelope.append(array[index])
        return envelope

    def getEdgeType(self):
        return self.edgetype
    
    def getResolveTime(self):
        return self.resolve_time
