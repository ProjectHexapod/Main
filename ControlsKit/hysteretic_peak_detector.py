import time_sources
import scipy


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
