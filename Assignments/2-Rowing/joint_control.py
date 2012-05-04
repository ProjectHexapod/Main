from math import pi


class JointController:
    def __init__(self, joint):
        self.joint = joint

    	self.prev_error = 0
        self.prev_time = 0
        self.iterm = 0
        self.valve_pos = 0

        # set weights
        self.kp = 0.20
        self.ki = 0.20
        self.kd = 0.20

    # sim_time: current system time in seconds
    # target_angle: target angle for joint in degrees 
    # 
    # uses globals: prev_error: the error in degrees at the time the function is called
    #               prev_time: system time when the function was last called
    def updateJoint(self, sim_time, target_angle):
        cur_error = bound(target_angle - self.joint.getAngle())
	        
        dtime = sim_time - self.prev_time

        #if no time has passed since last function call return last valve_pos
        if dtime == 0 or self.prev_time < 0:
            return self.valve_pos

        #calculate PID terms
        pterm = cur_error * self.kp
        self.iterm += cur_error * dtime * self.ki
        #print self.iterm
        dterm = (cur_error - self.prev_error)/dtime * self.kd

        #self.valve_pos = pterm + self.iterm + dterm
        self.valve_pos = pterm

        self.prev_error = cur_error
        self.prev_time = sim_time

        #print self.valve_pos

        self.joint.setLengthRate(self.valve_pos)

def bound(a):
    a %= 2*pi
    if a > pi:
        a -= 2*pi
    if a < -pi:
        a += 2*pi
    return a
