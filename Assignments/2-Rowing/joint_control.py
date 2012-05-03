from math import pi


class JointController:
    def __init__(self):
    	self.prev_error = 0
        self.prev_time = -1
        self.iterm = 0
        self.valve_pos = 0

        # set weights
        self.kp = 1
        self.ki = 1
        self.kd = 1

    # target_angle: target angle for joint in degrees 
    # joint:
    # robot:
    # sys_time: current system time in seconds
    # 
    # uses globals: prev_error: the error in degrees at the time the function is called
    #               prev_time: system time when the function was last called
    def updateJoint(self, target_angle, joint, robot, sys_time):
        # YOUR ASSIGNMENT: 
        # 
        # Given the target angle on the joint, command a sane linear velocity
        # to make the joint hit the target angle.
        # You should think about not introducing sudden movements in to the system
        # 
        # All lengths are in meters, all angles in radians
        #
        # Robot link lengths are in:
        # robot.YAW_L  
        # robot.THIGH_L
        # robot.CALF_L
        # Joint angles are positive in the direction of cylinder expansions.
        # Looking from above, positive hip yaw swings the leg clockwise
        # Positive hip pitch and knee pitch curl the leg under the robot

        ### YOUR CODE GOES HERE ###

	        
        cur_error = target_angle - joint.getAngle()
	        
        dtime = sys_time - self.prev_time

        #if no time has passed since last function call return last valve_pos
        if dtime == 0 or self.prev_time < 0:
            return self.valve_pos

        #calculate PID terms
        pterm = cur_error * self.kp
        self.iterm += cur_error * dtime * self.ki
        dterm = (cur_error - self.prev_error)/dtime * self.kd

        self.valve_pos = pterm + self.iterm + dterm

        self.prev_error = cur_error
        self.prev_time = sys_time

        return self.valve_pos
