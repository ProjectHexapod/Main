class TimeSource:
    def __init__(self, initial_time=0.0, initial_delta=0.0):
        self.initial_time = initial_time
        self.initial_delta = initial_delta
        self.reset()
    
    def reset(self):
        self.time = self.initial_time
        self.delta = self.initial_delta
    def updateTime(self, time):
        self.delta = time - self.time
        self.time = time
    def updateDelta(self, delta):
        self.delta = delta
        self.time += delta
    
    def getTime(self):
        return self.time
    def getDelta(self):
        return self.delta

global_time = TimeSource()
