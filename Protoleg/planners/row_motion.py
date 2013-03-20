from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove
#from ControlsKit.leg_paths import PutFootOnGround
from ControlsKit.math_utils import array, Z
#from UI import logger
from ControlsKit.time_sources import global_time

class Gait(object):
    def __init__( self ):
        self.model = LegModel()
        self.controller = LimbController()
        self.path = None
        self.index = 0
        self.points = []
        self.points.append( (0.4,  0, -0.45, 0.2) )
        #self.points.append( (1.7,  1.25, -1.05, 0.2) )
        #self.points.append( (1.7, -1.25, -1.05, 0.5) )
        #self.points.append( (1.7, -1.25, -1.68, 0.2) )
        #self.points.append( (1.7,  1.25, -1.68, 0.5) )
        #points.append( (1.6,  0.00, -1.7) )
        #self.points.append( (1.7, 0.0, -0.65) )
        #self.points.append( (1.7, 0.0, -1.58) )
        #self.points.append( (2.5, 0.0, -1.38) )
        #self.points.append( (1.2, 0.0, -1.38) )

        # Hackery for notch filter
        self.hip_yaw_commands   = [0.0 for i in range(int((0.5/2.00) / (1/200.0)))]
        self.hip_pitch_commands = [0.0 for i in range(int((0.5/6.30) / (1/200.0)))]
        self.knee_commands = [0.0 for i in range(int((0.5/6.30) / (1/200.0)))]
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
            # HIP PITCH TUNING DONE AT .20 SPEED
            self.index = (self.index+1)%len(self.points)

        # Evaluate path and joint control
        controller.update(self.model.getJointAngles(), self.path.update())

        # Send commands
        commands = controller.getLengthRateCommands()

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

