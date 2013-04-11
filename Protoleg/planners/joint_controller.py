import sys
sys.path.append('..')
import math
from ControlsKit import time_sources
from ControlsKit.filters import LowPassFilter
from Utilities.ActuatorCharacteristics import ActuatorMathHelper

gpm2cmps = 1/15850.4

class PistonController(object):
    """
    Tries to control a valve to match a linear rate.
    """
    def __init__(self, act_char, dead_pos, dead_neg):
        # Valve Tuning
        # Positive and Negative extents of the deadband
        self.dead_pos = dead_pos
        self.dead_neg = dead_neg
        # Piston attributes
        self.act_char = act_char
    def flowFromValveCommand( self, cmd ):
        """
        Return a flow from a valve command
        -1 < cmd < 1
        """
        raise NotImplemented
    def valveCommandFromFlow( self, flow ):
        """
        Reverse of flowFromValveCommand
        """
        # Then get that flow as a proportion of the valve max flow
        normalized_flow = flow / (5.0*gpm2cmps)
        # Then shift and scale based on the deadbands
        if normalized_flow > 0:
            valve_command = (1-self.dead_pos)*normalized_flow + self.dead_pos
        elif normalized_flow < 0:
            valve_command = (1-self.dead_neg)*normalized_flow - self.dead_neg
        else:
            valve_command = 0.0
        if valve_command > 1.0 or valve_command < -1.0:
            print 'PistonController WARNING: someone requested a ridiculous flow rate: %f'%valve_command
            valve_command = valve_command/abs(valve_command)
        return valve_command 
    def flowFromLinearRate( self, target_rate ):
        if target_rate > 0:
            target_flow = target_rate*self.act_char.getExtensionCrossSectionM2()
        else:
            target_flow = target_rate*self.act_char.getRetractionCrossSectionM2()
        return target_flow
    def update( self, target_rate, measured_rate=0.0 ):
        """
        TODO: We should put a control loop in here too,
        but for now pure feedforward
        """
        target_flow = self.flowFromLinearRate(target_rate)
        valve_command = self.valveCommandFromFlow(target_flow)
        return valve_command 

class OneDClayPit(object):
    def __init__(self, min_x, max_x, n_points, name=None, init_func=None, k=0.0e-3, max_slope=None, force_monotonic=True):
        """
        min_x and max_x determine the length of the x axis.
        The x axis is then subdivided in to n_points points
        init_func must take one float and return one float.  If provided, it is used
            to initialize the pit.
        k is the fraction of the distance a point in the pit will change when
            provided with a new reading.
        max_slope is the slope beyond which adjacent points will tug at eachother
        force_monotonic forces a positive slope.
        """
        self.name = name
        self.k = k
        self.force_monotonic=force_monotonic
        self.min_x = min_x
        self.dx = (max_x - min_x)/(n_points-1)
        # Internally we express max slope as maximum change between two adjacent cells
        #   in memory.  Externally it's maximum dy/dx
        self.max_dy = max_slope*self.dx

        try:
            self.loadState()
        except IOError:
            print 'No saved state found for %s, generating new profile'%self.name
            self.mem = [0.0 for i in range(n_points)]
            if init_func != None:
                for i in range(n_points):
                    self.mem[i] = init_func(self.min_x+i*self.dx)

    def __index(self, x):
        index = (x-self.min_x)/self.dx
        remainder = index%1
        index = int(index)
        if index < 0:
            index = 0
        elif index > len(self.mem)-2:
            index = len(self.mem)-2
        return index, remainder
    def __interp(self, x):
        index, remainder = self.__index(x)
        retval = (1.0-remainder)*self.mem[index] + (remainder)*self.mem[index+1]
        return retval
    def __smoothneg( self, i ):
        if i == 0:
            return
        dy = self.mem[i] - self.mem[i-1]
        if dy > self.max_dy:
            self.mem[i-1] = self.mem[i] - self.max_dy
            self.__smoothneg(i-1)
        elif self.force_monotonic and dy < 0:
            self.mem[i-1] = self.mem[i]
            self.__smoothneg(i-1)
    def __smoothpos( self, i ):
        if i == len(self.mem)-1:
            return
        dy = self.mem[i+1] - self.mem[i]
        if dy > self.max_dy:
            self.mem[i+1] = self.mem[i] + self.max_dy
            self.__smoothpos(i+1)
        elif self.force_monotonic and dy < 0:
            self.mem[i+1] = self.mem[i]
            self.__smoothpos(i+1)
    def lookup(self, x, y=None, k=None):
        """
        Read the value of the pit at x.
        If y is supplied, push the clay in the direction of y.
        """
        retval = self.__interp(x)
        if y == None:
            return retval
        # Poke the pit
        index,remainder = self.__index(x)
        
        if k == None:
            k = self.k
        
        dy = y-self.mem[index]
        self.mem[index] += k * (1.0-remainder) * dy
        dy = y-self.mem[index+1]
        self.mem[index+1] += k * (remainder) * dy

        # Smooth out the pit in both directions
        self.__smoothneg( index )
        self.__smoothpos( index+1 )
    def printpit(self):
        s=''
        for f in self.mem:
            s += '%0.2f '%f
        print s
        print '\n\n'
    def saveState( self ):
        import pickle
        f = open(self.name, 'wb+')
        pickle.dump(self.mem, f)
        f.close()
    def loadState( self ):
        import pickle
        f = open(self.name, 'rb')
        self.mem = pickle.load(f)
        f.close()
        print 'load success:', self.name
    def dumpToFile( self, fname ):
        """
        Dump the mem to a csv
        """
        f = open(fname, 'w+')
        f.write('x, y\r\n')
        for i in range(len(self.mem)):
            x = self.min_x + self.dx*i
            y = self.mem[i]
            f.write('%1.5f, %1.5f\r\n'%(x,y))
        f.close()

if __name__=='__main__':
    pit = OneDClayPit( -1.0, 1.0, 100, lambda(x):x, k=1e-3, max_slope=1.0, discontinuities_x=[0.0] )
    def printpit(pit):
        s=''
        for f in pit.mem:
            s += '%0.2f '%f
        print s
        print '\n\n'
    printpit(pit)
    for i in range(1000):
        pit.lookup(0.1, 1.0)
    printpit(pit)
    for i in range(1000):
        pit.lookup(0.1, 0.0)
    printpit(pit)
    for i in range(1000):
        pit.lookup(-0.1, 1.0)
    printpit(pit)
    for i in range(1000):
        pit.lookup(-0.1, -1.0)
    printpit(pit)

class LearningPistonController(PistonController):
    """
    Stores a history of measured rates vs. valve commands and corrects itself over time.
    """
    def __init__(self, name=None, *args, **kwargs):
        super(LearningPistonController, self).__init__(*args, **kwargs)
        pit_init = super(LearningPistonController, self).valveCommandFromFlow
        self.clay_pit_pos = OneDClayPit( min_x=1e-6, max_x = 4.0*gpm2cmps,  n_points = 64, init_func=pit_init, max_slope=1.0/(6.0*gpm2cmps), k=1.0, name=name+'_pos' )
        self.clay_pit_neg = OneDClayPit( min_x=-4.0*gpm2cmps, max_x = -1e-6, n_points = 64, init_func=pit_init, max_slope=1.0/(6.0*gpm2cmps), k=1.0, name=name+'_neg' )
        self.valve_cmd = 0.0
    def saveState(self):
        self.clay_pit_pos.saveState()
        self.clay_pit_neg.saveState()
    def update(self, target_rate, measured_rate=None):
        target_flow = self.flowFromLinearRate(target_rate)
        # Calc valve command
        if target_flow > (0.025*gpm2cmps):
            self.valve_cmd = self.clay_pit_pos.lookup(target_flow)
        elif target_flow < (-0.025*gpm2cmps):
            self.valve_cmd = self.clay_pit_neg.lookup(target_flow)
        else:
            self.valve_cmd = 0.0
        # "Learn"
        if measured_rate != None:
            measured_flow = self.flowFromLinearRate(measured_rate)
            def sign(x):
                if x<0:
                    return -1
                if x>0:
                    return 1
                return 0
            def sat(x,lim):
                return max(min(x,lim),-lim)
            if sign(measured_flow) == sign(self.valve_cmd)\
                    and abs(target_flow) > 0.025*gpm2cmps:
                flow_error = target_flow-measured_flow
                error_mult=2e-0
                err = (target_flow-measured_flow)*error_mult
                err = sat(err, 1e-2)
                if   target_flow >  0.025*gpm2cmps:
                    self.clay_pit_pos.lookup( target_flow, self.valve_cmd+err )
                elif target_flow < -0.025*gpm2cmps:
                    self.clay_pit_neg.lookup( target_flow, self.valve_cmd+err )
        return self.valve_cmd

class JointController(object):
    """
    Produces a linear rate trying to control an angle.
    Requires a description of a joint in the form of an ActuatorMathHelper
    """
    def __init__(self, act_math, kp=0, ki=0, kd=0, kff=None, kfa=None, derivative_corner=10, backlash=0.0):
        """
        act_math is the ActuatorMathHelper that contains the description of the joint
            and actuator
        kp = proportional gain term
        ki = integral gain term
        kd = derivative gain term
        kff= feed forward velocity term.  Applies signal relative to dervative of the target
        derivative_corner = corner frequency of derivative filter.
        Our real world signals are too noisy to use without significant filtering
        kfa= feed forward acceleration term.  Applies signal relative to the difference in
        rate of change of the target and desired.
        backlash = if we are within this angle of the target, we apply no corrective signal.
        """
        self.act_math = act_math
        self.updateGainConstants(kp, ki, kd, kff, kfa)
        self.backlash = backlash
        
        # NOTE: it is important that these three variables are floating point to avoid truncation
        self.prev_error = 0.0
        self.prev_desired_ang = 0.0
        self.prev_ang = 0.0
        self.integral_error_accumulator = 0.0

        self.d_lowpass = LowPassFilter( gain=1.0, corner_frequency=derivative_corner )
        self.arate_lowpass = LowPassFilter( gain=1.0, corner_frequency=derivative_corner )

    def updateGainConstants(self, kp, ki, kd, kff = None, kfa=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        if kff != None:
            self.kff = kff
        else:
            self.kff = 0.0
        if kfa != None:
            self.kfa = kfa
        else:
            self.kfa = 0.0
    def getAngleRate( self ):
        return self.arate_lowpass.getVal()
    def getLengthRate( self ):
        self.act_math.setAngle( self.prev_ang )
        self.act_math.setAngleRate( self.arate_lowpass.getVal() )
        #self.act_math.setAngleRate( self.measured_deriv )
        present_length_rate = self.act_math.getLengthRate()
        return present_length_rate
    def getDesiredLengthRate( self ):
        self.act_math.setAngle( self.prev_ang )
        self.act_math.setAngleRate( self.desired_vel )
        desired_length_rate = self.act_math.getLengthRate()
        return desired_length_rate

    def update(self, desired_ang, measured_ang):
        delta_time = time_sources.global_time.getDelta()

        delta_ang = measured_ang - self.prev_ang
        self.prev_ang = measured_ang
        self.arate_lowpass.update( delta_ang / delta_time )

        desired_vel = (desired_ang - self.prev_desired_ang)/delta_time
        self.desired_vel = desired_vel

        error = desired_ang - measured_ang
        if abs(error) < self.backlash:
            error = 0.0
        else:
            if error < 0.0:
                error += self.backlash
            else:
                error -= self.backlash

        self.integral_error_accumulator += self.ki * error * delta_time
        derivative_error = self.d_lowpass.update((error - self.prev_error) / delta_time)

        velocity_error = desired_vel - derivative_error

        self.prev_error = error
        self.prev_desired_ang = desired_ang
        
        # Calculate a desired angle rate
        control_ang_rate = self.kp * error + self.integral_error_accumulator + self.kd * derivative_error + self.kff*desired_vel + self.kfa*velocity_error
        # Use joint geometry to determine a target piston length rate
        self.act_math.setAngle( measured_ang )
        self.act_math.setAngleRate( control_ang_rate )
        target_length_rate = self.act_math.getLengthRate()

        return target_length_rate

