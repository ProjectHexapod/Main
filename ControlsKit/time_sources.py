from leg_logger import logger

class TimeSource:
    def __init__(self, initial_time=0.0, initial_delta=0.0):
        self.initial_time = initial_time
        self.initial_delta = initial_delta
        
        self.time = self.initial_time
        self.delta = self.initial_delta
    
    def updateTime(self, time):
        if time <= self.time:
            logger.error("TimeSource.updateTime: Reversed time error!",
                         initial_time=self.initial_time,
                         initial_delta=self.initial_delta,
                         current_time=self.time,
                         bad_value=time)
            raise ValueError("TimeSource.updateTime(): time must be increasing")
        self.delta = time - self.time
        self.time = time
    def updateDelta(self, delta):
        if delta <= 0:
            logger.error("TimeSource.updateDelta: Reversed time error!",
                         initial_time=self.initial_time,
                         initial_delta=self.initial_delta,
                         current_time=self.time,
                         bad_value=delta)
            raise ValueError("TimeSource.updateDelta(): time must be increasing")
        self.delta = delta
        self.time += delta
    
    def getTime(self):
        return self.time
    def getDelta(self):
        return self.delta

global_time = TimeSource()

class StopWatch:
    '''
    A StopWatch re-references a parent_time_source (usually global_time) so
    that it starts counting at t = 0 even if parent_time_source.getTime() != 0
    when StopWatch.getTime() is first called. A StopWatch gets its time updates
    from the parent_time_source.
    '''
    def __init__(self, active=True, time_source=global_time):
        self.ts = time_source
        self.parent_time_1 = 0.0
        
        self.sync_with_parent = True
        self.time = 0.0
        self.delta = 0.0
        
        self.curvature = 0.0
        if active:
            self.slope = 1.0
        else:
            self.slope = 0.0
    
    def isActive(self):
        return self.slope != 0.0 or self.curvature != 0.0
    def start(self):
        self.curvature = 0.0
        self.slope = 1.0
        self.sync_with_parent = True
    def stop(self):
        self.curvature = 0.0
        self.slope = 0.0
    def smoothStart(self, transition_duration):
        self.sync_with_parent = True
        self.curvature = 1.0 / transition_duration
    def smoothStop(self, transition_duration):
        self.curvature = -1.0 / transition_duration
    
    def getTime(self):
        self.update()
        return self.time
    def getDelta(self):
        self.update()
        return self.delta
    
    # Both getTime() and getDelta() call update(), so it's generally not
    # necessary to call update() directly.
    def update(self):
        parent_time = self.ts.getTime()
        if self.sync_with_parent:
            self.sync_with_parent = False
            self.parent_time_1 = parent_time
            self.delta = 0.0
            return
        
        # If our data is stale, update it
        if self.parent_time_1 != parent_time:
            parent_delta = parent_time - self.parent_time_1
            if self.curvature != 0.0:  # If we are smooth starting/stopping
                self.slope += self.curvature * parent_delta  # Update the slope
                if self.slope >= 1.0:  # smoothStart() end condition
                    self.slope = 1.0
                    self.curvature = 0.0
                elif self.slope <= 0.0:  # smoothStop end condition
                    self.slope = 0.0
                    self.curvature = 0.0
            if self.slope == 0.0:
                self.delta = 0.0
                return
            
            self.delta = self.slope * parent_delta
            self.time += self.delta
            self.parent_time_1 = parent_time
    

# Don't use this function unless you're running a test. Production code expects
# TimeSources to be monotonically increasing.
def resetTimeSourceForTestingPurposes(ts):
    ts.time = ts.initial_time
    ts.delta = ts.initial_delta
