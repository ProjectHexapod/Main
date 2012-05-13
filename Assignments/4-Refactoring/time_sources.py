class TimeSource:
    def __init__(self, initial_time=0.0, initial_delta=0.0):
        self.time = initial_time
        self.delta = initial_delta
    
    def update(self, time):
        self.delta = time - self.time
        self.time = time
    
    def getTime(self):
        return self.time
    def getDelta(self):
        return self.delta

global_time = TimeSource()
