import sys
sys.path.append('..')
from ConfigParser import ConfigParser
from ControlsKit.limb_controller import LimbController
from math_utils import *
from filters import HighPassFilter
import math
from leg_logger import logger
from os import path

class LegModel:
    def __init__(self, config_file="../ControlsKit/leg_model.conf", section="LegModel"):
        c = ConfigParser()
        if not path.exists(path.abspath(config_file)):
            print 'Config file %s not found!'%config_file
            raise IOError
        c.read(config_file)
        
        # Link lengths
        self.YAW_LEN = c.getfloat(section, "yaw_len")
        self.THIGH_LEN = c.getfloat(section, "thigh_len")
        self.CALF_LEN = c.getfloat(section, "calf_len")

        # Actuator soft bounds
        soft_stops_section='SoftStops'
        self.SOFT_MINS=array(
                [c.getfloat(soft_stops_section,'yaw_stop_low'),
                c.getfloat(soft_stops_section,'pitch_stop_low'),
                c.getfloat(soft_stops_section,'knee_stop_low')])
        self.SOFT_MAXES=array(
                [c.getfloat(soft_stops_section,'yaw_stop_high'),
                c.getfloat(soft_stops_section,'pitch_stop_high'),
                c.getfloat(soft_stops_section,'knee_stop_high') ])

        # State
        vel_corner = 100.0  # rad/s
        self.jv_filter = HighPassFilter(vel_corner, vel_corner)  # band limited differentiator
        self.setSensorReadings(0.0, 0.0, 0.0, 0.0)

        # Events
        self.SHOCK_DEPTH_THRESHOLD_LOW = c.getfloat(section, "shock_depth_threshold_low")
        self.SHOCK_DEPTH_THRESHOLD_HIGH = c.getfloat(section, "shock_depth_threshold_high")
        self.foot_on_ground = False

#MOVE ME TO PLANNER
        # Joint control
        self.length_rate_commands = array([0.0, 0.0, 0.0])
            # TODO: replace these soft min and soft max values with more reasonable ones once they're known
        self.controller=LimbController([c.getfloat(section, "yaw_p"),  # proportional terms
                        c.getfloat(section, "hp_p"),
                        c.getfloat(section, "kp_p")],
        
                        [c.getfloat(section, "yaw_i"),  # integral terms
                        c.getfloat(section, "hp_i"),
                        c.getfloat(section, "kp_i")],
        
                        [c.getfloat(section, "yaw_d"),  # differential terms
                        c.getfloat(section, "hp_d"),
                        c.getfloat(section, "kp_d")] )


    # Store sensor readings
    def setSensorReadings(self, yaw, hip_pitch, knee_pitch, shock_depth):
        self.joint_angles = array([yaw, hip_pitch, knee_pitch])
        
        #throw errors if measured joint angles are NaN, out of bounds, etc
        for angle, soft_min, soft_max in zip(self.joint_angles, self.SOFT_MINS, self.SOFT_MAXES):
            if math.isnan(angle):
                logger.error("LegModel.setSensorReadings: NaN where aN expected!",
                            angle=angle,
                            angle_index=self.joint_angles.searchsorted(angle),
                            yaw=yaw,
                            hip_pitch=hip_pitch,
                            knee_pitch=knee_pitch,
                            shock_depth=shock_depth,
                            bad_value="angle")
                raise ValueError("LegModel: Measured angle cannot be NaN.")
                
            if (soft_min > angle) or (angle > soft_max):
                logger.error("LegModel: Measured position outside of soft range!",
                        angle=angle,
                        angle_index=self.joint_angles.searchsorted(angle),
                        yaw=yaw,
                        hip_pitch=hip_pitch,
                        knee_pitch=knee_pitch,
                        shock_depth=shock_depth,
                        soft_min=soft_min,
                        soft_max=soft_max,
                        bad_value="angle")
                print soft_min
                print soft_max
                print angle
                raise ValueError("LegModel: Measured angle out of soft range!")
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

#MOVE ME TO PLANNERS
    # Joint control
    def setDesiredJointAngles(self, desired_joint_angles):
        self.desired_joint_angles = desired_joint_angles
        logger.info("LegModel.setDesiredJointAngles()",
                    hip_yaw_command=desired_joint_angles[YAW],
                    hip_pitch_command=desired_joint_angles[HP],
                    knee_pitch_command=desired_joint_angles[KP])
    def updateLengthRateCommands(self):
        self.length_rate_commands = self.controller.update(
                self.desired_joint_angles, self.getJointAngles())
    def getLengthRateCommands(self):
        return self.length_rate_commands

