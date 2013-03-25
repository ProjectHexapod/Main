from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove
from ControlsKit.math_utils import array, Z
from ControlsKit.time_sources import global_time
from  joint_controller import PistonController
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
        self.firstrun = True

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
        
        yaw_pist   = PistonController(YAW_ACT  , 0.26, 0.28)
        pitch_pist = PistonController(PITCH_ACT, 0.27, 0.27)
        knee_pist  = PistonController(KNEE_ACT , 0.22, 0.20)

        self.pist_helpers = [yaw_pist, pitch_pist, knee_pist]
        
        # Hackery for notch filter
        self.hip_yaw_commands   = [0.0 for i in range(int((0.5/2.00) / (1/200.0)))]
        self.hip_pitch_commands = [0.0 for i in range(int((0.5/6.30) / (1/200.0)))]
        self.knee_commands = [0.0 for i in range(int((0.5/6.30) / (1/200.0)))]

    def update( self, time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
        time_sources.global_time.updateTime(time)

        if self.firstrun:
            self.firstrun = False
            self.tracked_ang = [yaw, hip_pitch, knee_pitch]
            self.target_ang  = [0.0, -84.0*deg2rad, 175*deg2rad]

        # Increment the tracked angles
        for i in range(3):
            if self.tracked_ang[i] < self.target_ang[i]:
                self.tracked_ang[i] += deg2rad*0.02
            else:
                self.tracked_ang[i] -= deg2rad*0.02

        # Evaluate path and joint control
        controller.update( (yaw, hip_pitch, knee_pitch), self.tracked_ang )

        # Send commands
        rates = controller.getLengthRateCommands()

        commands = [self.pist_helpers[i].update(rates[i]) for i in range(3)]

        # Manual Hackery
        # Install 2.00Hz notch filter on the hip pitch command to avoid that oscillation we seem to excite on retraction
        filtered_cmd = (commands[0]+self.hip_yaw_commands.pop(0))/2
        self.hip_yaw_commands.append(commands[0])
        commands[0] = filtered_cmd
        # Install 6.2Hz notch filter on the hip pitch command to avoid that oscillation we seem to excite on retraction
        filtered_cmd = (commands[1]+self.hip_pitch_commands.pop(0))/2
        self.hip_pitch_commands.append(commands[1])
        commands[1] = filtered_cmd
        # Install 6.2Hz notch filter on the hip pitch command to avoid that oscillation we seem to excite on retraction
        filtered_cmd = (commands[2]+self.knee_commands.pop(0))/2
        self.knee_commands.append(commands[2])
        commands[2] = filtered_cmd

        return commands

gait = Gait()
update = gait.update
controller = gait.controller

