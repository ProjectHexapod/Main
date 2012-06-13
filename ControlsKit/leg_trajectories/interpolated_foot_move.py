from ControlsKit import time_sources
from scipy import interpolate

#note that at least 4 points must be specified
class InterpolatedFootMove:
    """This is a smooth trajectory through given points in space and time. 
    """
    #way_points format: array([[t0,x0,y0,z0],[t1,x1,y1,z1],...])
    def __init__(self, leg_controller, way_points):
        self.leg = leg_controller
        
        self.done = False
        
        self.time_array = way_points[0]
        self.spatial_array = way_points[1:,:]
        
        start_error = self.spatial_array[:,0] - self.leg.getFootPos()
        
        #adjust all values to be relative to actual start position
        for i in range (0,way_points.shape[1]):
            self.spatial_array[:,i] -= start_error
        
        self.f = interpolate.interp1d(self.time_array, self.spatial_array,kind='cubic')
        self.target_foot_pos = self.f(0)
        
        self.stop_watch = time_sources.StopWatch(active=True, time_source=time_sources.global_time)
        
    def isDone(self):
        print "self.done = ", self.done
        print "self.stop_watch.isActive() = ", self.stop_watch.isActive()
        return self.done and not self.stop_watch.isActive()
    
    def update(self):
        print "time up ", self.stop_watch.getTime() >= self.time_array[self.time_array.size-1]
        if not self.done and self.stop_watch.getTime() >= self.time_array[self.time_array.size-1]:
            self.done = True
            self.stop_watch.stop()
        if not self.isDone():
            self.target_foot_pos = self.f(self.stop_watch.getTime())
            print "time = ", self.stop_watch.getTime()
            print "time^3 = ", self.stop_watch.getTime()**3
            print "target_foot_pos =", self.target_foot_pos
            return self.leg.jointAnglesFromFootPos(self.target_foot_pos)
