from math_utils import *
from filters import HighPassFilter
from pid_controller import PidController


class LegController:
    def __init__(self):
        # Link lengths
        self.YAW_LEN = 0.211
        self.THIGH_LEN = 1.372
        self.CALF_LEN = 1.283

        # State
        vel_corner = 100.0  # rad/s
        self.jv_filter = HighPassFilter(vel_corner, vel_corner)  # band limited differentiator
        self.setLegState(0.0, 0.0, 0.0, 0.0)
        self.joint_velocities = array([0.0, 0.0, 0.0])

        # Events
        self.SHOCK_DEPTH_THRESHOLD_LOW = 0.01
        self.SHOCK_DEPTH_THRESHOLD_HIGH = 0.02
        self.foot_on_ground = False

        # Joint control
        self.length_rate_commands = array([0.0, 0.0, 0.0])
        self.controllers = [
            # TODO: replace these soft min and soft max values with more reasonable ones once they're known
            PidController(0.5, 0.0, 0.0, -100, 100),  # Yaw joint
            PidController(0.5, 0.0, 0.0, -100, 100),  # Hip pitch joint
            PidController(0.5, 0.0, 0.0, -100, 100)   # Knee pitch joint
        ]


    # Store sensor readings
    def setLegState(self, yaw, hip_pitch, knee_pitch, shock_depth):
        self.joint_angles = array([yaw, hip_pitch, knee_pitch])
        self.shock_depth = shock_depth
        self.joint_velocities = self.jv_filter.update(self.joint_angles)
        

    # Access state
    def getJointAngles(self):
        return self.joint_angles
    def getJointVelocities(self):
        return self.joint_velocities
    def getShockDepth(self):
        return self.shock_depth
    def getLegState(self):
        return [self.getJointAngles(), self.getShockDepth()]

    # Kinematics
    def getFootPos(self):
        return self.footPosFromLegState(self.getLegState())
    def footPosFromLegState(self, leg_state):
        pos = array([self.CALF_LEN - leg_state[1], 0.0, 0.0])
        pos = rotateY(pos, leg_state[0][KP])
        pos[X] += self.THIGH_LEN
        pos = rotateY(pos, leg_state[0][HP])
        pos[X] += self.YAW_LEN
        return rotateZ(pos, -leg_state[0][YAW])
    def jointAnglesFromFootPos(self, pos, shock_depth=-9e9):
        if shock_depth == -9e9:
            shock_depth = self.getShockDepth()
            
        # Yaw is independent of the other two joints
        yaw = -atan2(pos[Y], pos[X])
        # Choose the solution that keeps the leg outside of the body
        if yaw > pi_2:
            yaw -= pi
        elif yaw < -pi_2:
            yaw += pi
        
        # Now treat the other two joints like a 2-DOF leg in the X-Z plane
        pos = rotateZ(pos, yaw)
        pos[X] -= self.YAW_LEN
        
        # What is the included angle between the foot and the +X axis?
        foot_pitch = -atan2(pos[Z], pos[X])
        
        aL, aC, aT = solveTriangle(norm(pos),
                                   self.CALF_LEN - shock_depth,
                                   self.THIGH_LEN)
        hip_pitch = foot_pitch - aC
        knee_pitch = pi - aL
        return array([yaw, hip_pitch, knee_pitch])

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
                self.desired_joint_angles[i],
                self.getJointAngles()[i])
    def getLengthRateCommands(self):
        return self.length_rate_commands

