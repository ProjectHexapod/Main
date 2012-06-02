from ConfigParser import ConfigParser
from math_utils import *
from filters import HighPassFilter
from pid_controller import PidController
import math
from leg_logger import logger

class LegController:
    def __init__(self, config_file="leg_controller.conf", section="LegController"):
        c = ConfigParser()
        c.read(config_file)
        
        # Link lengths
        self.YAW_LEN = c.getfloat(section, "yaw_len")
        self.THIGH_LEN = c.getfloat(section, "thigh_len")
        self.CALF_LEN = c.getfloat(section, "calf_len")

        # Actuator soft bounds
        self.SOFT_MIN = c.getfloat(section, "joint_stop_low")
        self.SOFT_MAX = c.getfloat(section, "joint_stop_high")

        # State
        vel_corner = 100.0  # rad/s
        self.jv_filter = HighPassFilter(vel_corner, vel_corner)  # band limited differentiator
        self.setSensorReadings(0.0, 0.0, 0.0, 0.0)

        # Events
        self.SHOCK_DEPTH_THRESHOLD_LOW = c.getfloat(section, "shock_depth_threshold_low")
        self.SHOCK_DEPTH_THRESHOLD_HIGH = c.getfloat(section, "shock_depth_threshold_high")
        self.foot_on_ground = False

        # Joint control
        self.length_rate_commands = array([0.0, 0.0, 0.0])
        self.controllers = [
            # TODO: replace these soft min and soft max values with more reasonable ones once they're known
            PidController(c.getfloat(section, "yaw_p"),  # Yaw joint
                          c.getfloat(section, "yaw_i"),
                          c.getfloat(section, "yaw_d")),

            PidController(c.getfloat(section, "hp_p"),  # Hip pitch joint
                          c.getfloat(section, "hp_i"),
                          c.getfloat(section, "hp_d")),

            PidController(c.getfloat(section, "kp_p"),  # Knee pitch joint
                          c.getfloat(section, "kp_i"),
                          c.getfloat(section, "kp_d")),
        ]


    # Store sensor readings
    def setSensorReadings(self, yaw, hip_pitch, knee_pitch, shock_depth):
        self.joint_angles = array([yaw, hip_pitch, knee_pitch])
        
        #throw errors if measured joint angles are NaN, out of bounds, etc
        for angle in self.joint_angles:
            if math.isnan(angle):
                logger.error("LegController.setSensorReadings: NaN where aN expected!",
                            angle=angle,
                            angle_index=self.joint_angles.searchsorted(angle),
                            yaw=yaw,
                            hip_pitch=hip_pitch,
                            knee_pitch=knee_pitch,
                            shock_depth=shock_depth,
                            bad_value="angle")
                raise ValueError("LegController: Measured angle cannot be NaN.")
                
            if self.SOFT_MIN > angle or angle > self.SOFT_MAX:
                logger.error("LegController: Measured position outside of soft range!",
                        angle=angle,
                        angle_index=self.joint_angles.searchsorted(angle),
                        yaw=yaw,
                        hip_pitch=hip_pitch,
                        knee_pitch=knee_pitch,
                        shock_depth=shock_depth,
                        soft_min=self.SOFT_MIN,
                        soft_max=self.SOFT_MAX,
                        bad_value="angle")
                raise ValueError("LegController: Measured angle out of soft range!")
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
    
    def isMoving(self, tolerance=0.001):
        return (abs(self.joint_velocities) >= tolerance).any()

    # Joint control
    def setDesiredJointAngles(self, desired_joint_angles):
        self.desired_joint_angles = desired_joint_angles
        logger.info("LegController.setDesiredJointAngles()",
                    hip_yaw_command=desired_joint_angles[YAW],
                    hip_pitch_command=desired_joint_angles[HP],
                    knee_pitch_command=desired_joint_angles[KP])
    def updateLengthRateCommands(self):
        for i in range(LEG_DOF):
            self.length_rate_commands[i] = self.controllers[i].update(
                self.desired_joint_angles[i],
                self.getJointAngles()[i])
    def getLengthRateCommands(self):
        return self.length_rate_commands

