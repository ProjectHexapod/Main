from math_utils import *
from pid_controller import PidController


class LegController:
    def __init__(self):
        # Link lengths
        self.YAW_LEN = 0.211
        self.THIGH_LEN = 1.372
        self.CALF_LEN = 1.283

        # State
        self.time = 0.0
        self.delta_time = 0.0
        self.setLegState(0.0, 0.0, 0.0, 0.0)

        # Events
        self.SHOCK_DEPTH_THRESHOLD_LOW = 0.01
        self.SHOCK_DEPTH_THRESHOLD_HIGH = 0.02
        self.foot_on_ground = False

        # Joint control
        self.length_rate_commands = array([0.0, 0.0, 0.0])
        self.controllers = [
            PidController(1.0, 1.0, 1.0),  # Yaw joint
            PidController(1.0, 1.0, 1.0),  # Hip pitch joint
            PidController(1.0, 1.0, 1.0)   # Knee pitch joint
        ]


    # Store sensor readings
    def setTime(self, time):
        self.delta_time = time - self.time
        self.time = time
    def setLegState(self, yaw, hip_pitch, knee_pitch, shock_depth):
        self.joint_angles = array([yaw, hip_pitch, knee_pitch])
        self.shock_depth = shock_depth

    # Access state
    def getTime(self):
        return self.time
    def getDeltaTime(self):
        return self.delta_time
    def getJointAngles(self):
        return self.joint_angles
    def getShockDepth(self):
        return self.shock_depth
    def getLegState(self):
        return [self.getJointAngles(), self.getShockDepth()]

    # Kinematics
    def getFootPos(self):
        return footPosFromJointAngles(self.getLegState())
    def footPosFromLegState(self, leg_state):
        pos = array([self.CALF_LEN - leg_state[1], 0.0, 0.0])
        pos = rotateY(pos, leg_state[0][KP])
        pos[X] += self.THIGH_LEN
        pos = rotateY(pos, leg_state[0][HP])
        pos[X] += self.YAW_LEN
        return rotateZ(pos, -leg_state[0][YAW])
    def jointAnglesFromFootPos(self, pos, shock_depth):
        hip_yaw_target = -atan2(pos[Y], pos[X])
        pos = rotateZ(pos, -hip_yaw_target)
        pos[X] -= self.YAW_LEN
        pitch = -atan2(pos[Z], pos[X])
        pos = rotateY(pos, -pitch)
        aL, aC, aT = solveTriangle(pos[X], self.CALF_LEN + shock_depth, self.THIGH_LEN)
        hip_pitch_target = pitch - aC
        knee_target = pi - aL
        return array([hip_yaw_target, hip_pitch_target, knee_target])

    # Touch-down detection
    def isFootOnGround(self):
        return self.foot_on_ground
    def updateFootOnGround(self):
        sd = self.getShockDepth()
        if sd < self.SHOCK_DEPTH_THRESHOLD_LOW:
            self.foot_on_ground = False
        elif sd > self.SHOCK_DEPTH_THRESHOLD_HIGH:
            self.foot_on_ground = True

    # Joint control
    def setDesiredJointAngles(self, desired_joint_angles):
        self.desired_joint_angles = desired_joint_angles
    def updateLengthRateCommands(self):
        for i in range(LEG_DOF):
            self.length_rate_commands[i] = self.controllers[i].update(
                self.getDeltaTime(),
                self.desired_joint_angles[i],
                self.getJointAngles()[i])
    def getLengthRateCommands(self):
        return self.length_rate_commands

