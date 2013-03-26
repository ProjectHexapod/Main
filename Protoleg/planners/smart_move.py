from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove
from ControlsKit.math_utils import array, Z
from ControlsKit.time_sources import global_time
from  joint_controller import PistonController, JointController
from Utilities.ActuatorCharacteristics import *

# Convenience multipliers...
deg2rad    = pi/180
psi2pascal = 6894.76
inch2meter = 2.54e-2
pound2kilo = 0.455
gpm2cmps = 1/15850.4

class Gait(object):
    def __init__( self ):
        self.model = LegModel()
        self.controller = LimbController()

        self.path = None
        self.index = 0
        self.points = []
        #self.points.append( (0.4,  0, -0.45, 0.2) )
        self.points.append( (1.8, -1.00, -0.75, 0.20) )
        self.points.append( (1.8, -1.00, -1.68, 0.20) )
        self.points.append( (1.8,  1.00, -1.68, 0.20) )
        self.points.append( (1.8,  1.00, -0.75, 0.20) )

        # Describe the actuator placements at each joint
        YAW_ACT    = ActuatorMathHelper(
                bore_diameter          = inch2meter*2.5,
                rod_diameter           = inch2meter*1.125,
                act_retracted_len      = inch2meter*14.25,
                act_extended_len       = inch2meter*18.25,
                pivot1_dist_from_joint = inch2meter*16.18,
                pivot2                 = (inch2meter*2.32,inch2meter*3.3),
                ang_offset             = deg2rad*-30.0,
                system_pressure        = psi2pascal*2300,
                axis                   = ( 0, 0, -1 ) )

        PITCH_ACT  = ActuatorMathHelper(
                bore_diameter          = inch2meter*3.0,
                rod_diameter           = inch2meter*1.5,
                act_retracted_len      = inch2meter*20.25,
                act_extended_len       = inch2meter*30.25,
                pivot1_dist_from_joint = inch2meter*8.96,
                pivot2                 = (inch2meter*27.55,inch2meter*8.03),
                ang_offset             = deg2rad*-84.0,
                system_pressure        = psi2pascal*2300,
                axis                   = ( 0, -1, 0 ) )

        KNEE_ACT   = ActuatorMathHelper(
                bore_diameter          = inch2meter*2.5,
                rod_diameter           = inch2meter*1.25,
                act_retracted_len      = inch2meter*22.25,
                act_extended_len       = inch2meter*34.25,
                pivot1_dist_from_joint = inch2meter*28.0,
                pivot2                 = (inch2meter*4.3,inch2meter*6.17),
                ang_offset             = deg2rad*61.84,
                system_pressure        = psi2pascal*2300,
                axis                   = ( 0, -1, 0 ) )
        self.act_helpers = [YAW_ACT, PITCH_ACT, KNEE_ACT]
       
        yaw_joint  = JointController(YAW_ACT,
                kp=1.0,
                ki=0.0,
                kd=0.0,
                kff=1.0,
                kfa=0.0,
                derivative_corner=10)
        pitch_joint  = JointController(PITCH_ACT,
                kp=3.5,
                ki=0.0,
                kd=0.0,
                kff=1.0,
                kfa=0.0,
                derivative_corner=10)
        knee_joint  = JointController(KNEE_ACT,
                kp=3.5,
                ki=0.0,
                kd=0.0,
                kff=1.0,
                kfa=0.0,
                derivative_corner=10)

        self.joint_controllers = [yaw_joint, pitch_joint, knee_joint]

        yaw_pist   = PistonController(YAW_ACT  , 0.26, 0.26)
        pitch_pist = PistonController(PITCH_ACT, 0.27, 0.27)
        knee_pist  = PistonController(KNEE_ACT , 0.22, 0.20)

        self.pist_helpers = [yaw_pist, pitch_pist, knee_pist]

    def update( self, time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
        # Update model
        time_sources.global_time.updateTime(time)
        self.model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
        self.model.updateFootOnGround()

        # Init path. Do this after the first update.
        if self.path is None:
            self.path = Pause(self.model, controller, 1.0)
        
        if self.path.isDone():
            self.path = TrapezoidalFootMove(self.model, controller,
                    array(self.points[self.index][0:3]),
                                           self.points[self.index][3], 0.3)
            self.index = (self.index+1)%len(self.points)

        # Evaluate path and joint control
        present_angles = self.model.getJointAngles()
        target_angles  = self.path.update()
        controller.update(present_angles, target_angles)

        ang_rates = [self.joint_controllers[i].update(target_angles[i], present_angles[i]) for i in range(3)]
        commands  = [self.pist_helpers[i].update(ang_rates[i]) for i in range(3)]

        return commands

gait = Gait()
update = gait.update
controller = gait.controller

