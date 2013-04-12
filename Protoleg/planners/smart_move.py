from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove
from ControlsKit.math_utils import array, Z
from ControlsKit.time_sources import global_time
from  joint_controller import PistonController,LearningPistonController, JointController
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

        #self.points.append( (1.8, -1.00, -0.75, 0.40) )
        #self.points.append( (1.8, -1.00, -1.68, 0.20) )
        #self.points.append( (1.8,  1.00, -1.68, 0.40) )
        #self.points.append( (1.8,  1.00, -0.75, 0.20) )

        #self.points.append( (1.8, -1.00, -1.45, 0.40) )
        self.points.append( (1.8, -1.00, -1.68, 0.70) )
        self.points.append( (1.8,  1.00, -1.68, 0.70) )
        self.points.append( (1.8,  0.00, -1.35, 0.70) )

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
                kp=1.5,
                ki=0.0,
                kd=0.0,
                kff=1.0,
                kfa=0.0,
                derivative_corner=10,
                backlash=deg2rad*1.5)
        pitch_joint  = JointController(PITCH_ACT,
                kp=2.0,
                ki=0.0,
                kd=0.0,
                kff=1.0,
                kfa=0.0,
                derivative_corner=10,
                backlash=deg2rad*0.5)
        knee_joint  = JointController(KNEE_ACT,
                kp=2.0,
                ki=0.0,
                kd=0.0,
                kff=1.0,
                kfa=0.0,
                derivative_corner=10,
                backlash=deg2rad*0.5)

        self.joint_controllers = [yaw_joint, pitch_joint, knee_joint]

        #yaw_pist   = LearningPistonController(YAW_ACT  , 0.26, 0.28)
        yaw_pist   = LearningPistonController('YAWPIST',   YAW_ACT  , 0.37, 0.37)
        pitch_pist = LearningPistonController('PITCHPIST', PITCH_ACT, 0.32, 0.32)
        knee_pist  = LearningPistonController('KNEEPIST',  KNEE_ACT , 0.22, 0.20)

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
                    self.points[self.index][3], 0.4)
            self.index = (self.index+1)%len(self.points)

        # Evaluate path and joint control
        present_angles = self.model.getJointAngles()
        target_angles  = self.path.update()
        controller.update(present_angles, target_angles)

        control_lin_rates = [self.joint_controllers[i].update(target_angles[i], present_angles[i]) for i in range(3)]
        target_lin_rates = [c.getDesiredLengthRate() for c in self.joint_controllers]
        measured_lin_rates = [c.getLengthRate() for c in self.joint_controllers]

        s = ''
        m = self.pist_helpers[0].clay_pit_pos.mem
        for i in range(len(m)):
            if not i%8:
                s += '%2.2f '%(m[i])
        print s

        commands  = [self.pist_helpers[i].update(control_lin_rates[i], measured_lin_rates[i]) for i in range(3)]
        #commands  = [self.pist_helpers[0].update(control_lin_rates[0], measured_lin_rates[0]),0,0]

        if 0:
            target_ang_rates = [c.desired_vel for c in self.joint_controllers]
            measured_ang_rates = [c.getAngleRate() for c in self.joint_controllers]
            s = 'Measured: '
            for m in measured_ang_rates:
                s += '%1.3f '%(m*180/pi)
            print s
            s = 'Target:   '
            for m in target_ang_rates:
                s += '%1.3f '%(m*180/pi)
            print s
            s = 'M Lin'
            for m in measured_lin_rates:
                s += '%1.3f '%m
            print s
            s = 'T Lin'
            for m in target_lin_rates:
                s += '%1.3f '%m
            print s
            self.pist_helpers[0].clay_pit_pos.printpit()

        return commands
    def gracefulExit(self):
        for i in range(3):
            self.pist_helpers[i].saveState()

gait = Gait()
update = gait.update
graceful_exit = gait.gracefulExit
controller = gait.controller

