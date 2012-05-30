from math_utils import *
from scipy.linalg import norm
from scipy import interpolate
import time_sources
from leg_logger import logger
from time_sources import global_time

#note that at least 4 points must be specified
class InterpolatedFootMove:
    """This is a smooth trajectory through given points in space and time. 
    """
    #way_points format: array([[t0,x0,y0,z0],[t1,x1,y1,z1],...])
    def __init__(self, leg_controller, way_points):
        self.leg = leg_controller
        
        self.done = False
        
        """
        #make sure start position is within a reasonable distance of actual start position
        if scipy.spatial.distance.pdist([start_pos, way_points[0,1:]], 'euclidean') > 0.1:
            self.done = True
            
        #append actual start position to beginning of way_points
        way_points = vstack((start_pos, way_points))
        """
        
        self.time_array = way_points[0]
        self.spatial_array = way_points[1:,:]
        
        start_error = self.spatial_array[:,0] - self.leg.getFootPos()
        
        #adjust all values to be relative to actual start position
        for i in range (0,way_points.shape[1]):
            self.spatial_array[:,i] -= start_error
        
        self.f = interpolate.interp1d(self.time_array, self.spatial_array,kind='cubic')
        self.target_foot_pos = self.f(0)
        
        self.stop_watch = time_sources.StopWatch(active=True, time_source=global_time)
        
    def isDone(self):
        #print "self.done = ", self.done
        #print "self.stop_watch.isActive() = ", self.stop_watch.isActive()
        #print "self.stop_watch.slope, curvature = ", self.stop_watch.slope, self.stop_watch.curvature
        return self.done and not self.stop_watch.isActive()
    
    def update(self):
        #print "time up ", self.stop_watch.getTime() >= self.time_array[self.time_array.size-1]
        if not self.done and self.stop_watch.getTime() >= self.time_array[self.time_array.size-1]:
        #    print "setting done"
            self.done = True
            self.stop_watch.stop()
        if not self.isDone():
            self.target_foot_pos = self.f(self.stop_watch.getTime())
        #    print "time = ", self.stop_watch.getTime()
        #    print "time^3 = ", self.stop_watch.getTime()**3
            print "target_foot_pos =", self.target_foot_pos
            return self.leg.jointAnglesFromFootPos(self.target_foot_pos)

class PutFootOnGround:
    def __init__(self, leg_controller, velocity, accel_duration=0.1):
        logger.info("New trajectory.", traj_name="PutFootOnGround",
                    velocity=velocity, accel_duration=accel_duration)
        
        self.leg = leg_controller
        self.vel = velocity
        self.accel_duration = accel_duration
        
        self.done = self.leg.isFootOnGround()
        self.target_foot_pos = self.leg.getFootPos()
        self.stop_watch = time_sources.StopWatch(active=False)
        if not self.done:
            self.stop_watch.smoothStart(self.accel_duration)

    def isDone(self):
        return self.done and not self.stop_watch.isActive()

    def update(self):
        if not self.done and self.leg.isFootOnGround():
            self.done = True
            self.stop_watch.smoothStop(self.accel_duration)
        if not self.isDone():
            self.target_foot_pos[Z] -= self.vel * self.stop_watch.getDelta()
        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)


class TrapezoidalFootMove:
    """This is a trapezoidal speed ramp, where speed is derivative foot position WRT time.
    """
    def __init__(self, leg_controller, final_foot_pos, max_velocity, acceleration):
        logger.info("New trajectory.", traj_name="TrapezoidalFootMove",
                    final_foot_pos=final_foot_pos, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.leg = leg_controller
        self.target_foot_pos = self.leg.getFootPos()
        self.final_foot_pos = final_foot_pos
        self.max_vel = max_velocity
        self.vel = 0.0
        self.acc = acceleration
        
        # Unit vector pointing towards the destination
        self.dir = self.getNormalizedRemaining()
        self.done = False

    def isDone(self):
        return self.done

    def getNormalizedRemaining(self):
        """Returns a normalized vector that points toward the current goal point.
        """
        return normalize(self.final_foot_pos - self.target_foot_pos)

    def update(self):
        if not self.isDone():
            delta = time_sources.global_time.getDelta()
            # if the remaining distance <= the time it would take to slow
            # down times the average speed during such a deceleration (ie
            # the distance it would take to stop)
            
            # rearranged multiplies to avoid confusing order of operations
            # readability issues
            remaining_vector = self.final_foot_pos - self.target_foot_pos
            if norm(remaining_vector) <= .5 * self.vel**2 / self.acc:
                self.vel -= self.acc * delta
            else:
                self.vel += self.acc * delta
                self.vel = min(self.vel, self.max_vel)
            self.target_foot_pos += self.dir * self.vel * delta
            
            if not arraysAreEqual(self.getNormalizedRemaining(), self.dir):
                self.done = True
                self.target_foot_pos = self.final_foot_pos

        return self.leg.jointAnglesFromFootPos(self.target_foot_pos)

class TrapezoidalJointMove:
    """This is a trapezoidal speed ramp, where speed is derivative foot position WRT time.
        This class expects max velocity for end effector, not for angular velocity.
    """
    def __init__(self, leg_controller, final_angles, max_velocity, acceleration):

        final_foot_pos = leg_controller.footPosFromLegState([final_angles,0])
        self.foot_move = TrapezoidalFootMove(leg_controller, final_foot_pos, max_velocity, acceleration)

        logger.info("New trajectory.", traj_name="TrapezoidalJointMove",
                    final_foot_pos=final_foot_pos, final_angles=final_angles, max_velocity=max_velocity,
                    acceleration=acceleration)
        
    def isDone(self):
        return self.foot_move.isDone()

    def update(self):
        return self.foot_move.update()
    
class Pause:
    def __init__(self, leg_controller, duration):
        self.leg = leg_controller
        self.initial_angles = self.leg.getJointAngles()
        self.duration = duration
        self.sw = time_sources.StopWatch();
        self.done = False
        
    def isDone(self):
        return self.done
    
    def update(self):
        self.done = self.sw.getTime() >= self.duration
        return self.initial_angles

class MoveJoint:
    def __init__(self, leg_controller, joint_idx, duration, direction, velocity=0.1, accel_duration=0.1):
        assert abs(direction) == 1
        
        self.leg = leg_controller
        self.joint = joint_idx
        self.duration = duration
        self.vel = direction * velocity
        self.accel_duration = accel_duration
        
        self.target_angles = self.leg.getJointAngles()
        self.stopping = False
        
        self.sw = time_sources.StopWatch()
        self.sw.smoothStart(self.accel_duration)
        
    def isDone(self):
        return not self.sw.isActive()
    
    def update(self):
        if not self.isDone():
            self.target_angles[self.joint] += self.sw.getDelta() * self.vel
            if not self.stopping and self.sw.getTime() >= self.duration:
                self.sw.smoothStop(self.accel_duration)
                self.stopping = True
        return self.target_angles

class FindJointStop:
    def __init__(self, leg_controller, joint_idx, direction, velocity=0.05, accel_duration=0.1):
        self.leg = leg_controller
        self.joint = joint_idx
        self.vel = direction * velocity
        
        self.target_angles = self.leg.getJointAngles()
        self.sw = time_sources.StopWatch()
        self.sw.smoothStart(accel_duration)
        
        self.moving = False
        self.done = False
    
    def isDone(self):
        return self.done
        
    def update(self):
        if self.moving and not self.leg.isMoving():
            self.done = True
        if not self.done:
            self.moving = self.leg.isMoving()
            self.target_angles[self.joint] += self.sw.getDelta() * self.vel
            
        return self.target_angles

    
