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


# Don't use this function unless you're running a test. Production code expects
# TimeSources to be monotonically increasing.
def resetTimeSourceForTestingPurposes(ts):
    ts.time = ts.initial_time
    ts.delta = ts.initial_delta
