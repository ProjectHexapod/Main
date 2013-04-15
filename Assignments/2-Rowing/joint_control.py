#TODO add PID override function
#TODO add on-the-fly PID tuning

from math import pi


class JointController:


    def __init__(self, joint):
        self.prev_error = 0  # error in radians at the time the function is called
        self.prev_time = 0  # system time when the function was last called
        self.iterm = 0
        self.valve_pos = 0
        self.outMin = -200   # minimum allowable flow rate
        self.outMax = 200    # maximum allowable flow rate
        self.joint = joint   # make joint into a global variable

        # set weights
        self.kp = 1
        self.ki = 1
        self.kd = 1

    # sys_time: current system time in seconds
    # target_angle: target angle for joint in degrees 


    def updateJoint(self, target_angle, sys_time):
        #check that target angle is within bounds
        if abs(target_angle) > 2 * pi:
            raise ValueError("Invalid target angle") 

        cur_error = target_angle - self.joint.getAngle()

        dtime = sys_time - self.prev_time

        #if no time has passed since last function call return last valve_pos
        if dtime == 0:
            return self.valve_pos

        #calculate P term
        pterm = cur_error * self.kp
        
        # calculate I term
        self.iterm += cur_error * dtime * self.ki
        # clamp iterm at maximum/minimum output
        # this prevents integral windup
        if self.iterm > self.outMax: 
            self.iterm = self.outMax
        elif self.iterm < self.outMin:
            self.iterm = self.outMin

        # calculate D term
        dterm = (cur_error - self.prev_error) / dtime * self.kd

        # calculate valve position output
        self.valve_pos = pterm + self.iterm + dterm

        # clamp outpout at maximum/minimum output
        if self.valve_pos > self.outMax: 
            self.valve_pos = self.outMax
        elif self.valve_pos < self.outMin:
            self.valve_pos = self.outMin

        self.prev_error = cur_error
        self.prev_time = sys_time

        # update the joint with the calculated flow rate
        self.outputFlowRate()

        return cur_error

    # update the joint with the calculated flow rate
    def outputFlowRate(self):
        self.joint.setLengthRate(self.valve_pos)
