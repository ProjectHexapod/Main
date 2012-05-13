class TimeSource:
    def __init__(self, initial_time=0.0, initial_delta=0.0):
        self.initial_time = initial_time
        self.initial_delta = initial_delta
        
        self.time = self.initial_time
        self.delta = self.initial_delta
    
    def updateTime(self, time):
        if time <= self.time:
            raise ValueError("TimeSource.updateTime(): time must be increasing")
        self.delta = time - self.time
        self.time = time
    def updateDelta(self, delta):
        if delta <= 0:
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
        
        self.active = active
        self.sync_with_parent = True
        self.time = 0.0
        self.delta = 0.0
    
    def start(self):
        self.active = True
        self.sync_with_parent = True
    def stop(self):
        self.active = False
    def isActive(self):
        return self.active
        
    
    def getTime(self):
        self.update()
        return self.time
    def getDelta(self):
        self.update()
        return self.delta
    
    # Both getTime() and getDelta() call update(), so it's generally not
    # necessary to call update() directly.
    def update(self):
        if not self.active:
            self.delta = 0.0
            return
        
        parent_time = self.ts.getTime()
        if self.sync_with_parent:
            self.sync_with_parent = False
            self.parent_time_1 = parent_time
            self.delta = 0.0
        
        # If our data is stale, update it
        if self.parent_time_1 != parent_time:
            self.delta = parent_time - self.parent_time_1
            self.time += self.delta
            self.parent_time_1 = parent_time
    

# Don't use this function unless you're running a test. Production code expects
# TimeSources to be monotonically increasing.
def resetTimeSourceForTestingPurposes(ts):
    ts.time = ts.initial_time
    ts.delta = ts.initial_delta
