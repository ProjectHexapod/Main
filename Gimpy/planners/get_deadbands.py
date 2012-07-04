from ControlsKit.filters import LowPassFilter
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove, PutFootOnGround
from ControlsKit import time_sources, LegModel, leg_logger, LimbController
from ControlsKit.math_utils import array

# Initialization

class Gait:
    def __init__(self):
        self.file_out = file('offsets.txt', 'w+')
        self.vel_IIR = None
        self.pwm_val = 0
        self.last_pos = 0
        self.last_t = 0
        self.MOVE_THRESH = .03
        self.firstrun = True
        self.dof_list = []
        self.dof_list.append('hip_pitch_e')
        self.dof_list.append('hip_pitch_r')
        self.dof_list.append('knee_pitch_e')
        self.dof_list.append('knee_pitch_r')
        self.dof_list.append('hip_yaw_e')
        self.dof_list.append('hip_yaw_r')
        self.callback = self.moveToInitialPosition
        self.model = LegModel()
        self.controller = LimbController()
    def update( self, *args, **kwargs ):
        return self.callback(*args, **kwargs)
    def moveToInitialPosition( self, time, yaw, hip_pitch, knee_pitch, shock_depth, command=None ):
        self.model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
        if not hasattr(self, 'initial_path'):
            self.initial_path = TrapezoidalFootMove(self.model, self.controller,\
                                       array([2.0, 0.0, -0.2]),\
                                       0.2, 0.1)
        self.controller.update(self.model.getJointAngles(), self.initial_path.update())
        if self.initial_path.isDone():
            self.callback = self.discoverDeadband
        return self.controller.getLengthRateCommands()
    def discoverDeadband( self, time, yaw, hip_pitch, knee_pitch, shock_depth, command=None ):
        # Have we made it through all the joints?
        if not len(self.dof_list):
            # If so, exit the program
            self.file_out.close()
            exit()
        if self.dof_list[0][:-2] == 'hip_pitch':
            pos = hip_pitch
            cmd_i = 1
        elif self.dof_list[0][:-2] == 'knee_pitch':
            pos = knee_pitch
            cmd_i = 2
        elif self.dof_list[0][:-2] == 'hip_yaw':
            pos = yaw
            cmd_i = 0
        else:
            raise
        if self.dof_list[0][-1] == 'e':
            sign = 1
        elif self.dof_list[0][-1] == 'r':
            sign = -1
        else:
            raise
        # Default command: command no movement on all valves
        # valves are yaw, pitch, knee, in that order
        # Scale depends on the mode of the underlying layer...
        # sometimes it expects a length rate in meters/sec,
        # sometimes it expects a command value between -255 and 255
        cmd = [0,0,0]
        # Is this our first tick on a new DOF?
        if self.firstrun:
            # Initialize state variables
            print "Initializing for %s"%self.dof_list[0]
            self.pwm_val = 0
            self.vel_IIR = LowPassFilter( gain=1.0, corner_frequency=1 )
            self.firstrun = False
        else:
            # Calculate velocity, update filter
            dt = time-self.last_t
            dpos = pos - self.last_pos
            vel_est = dpos/dt
            self.vel_IIR.update(vel_est)
            self.pwm_val += dt*1e-2
            cmd[cmd_i] = sign*self.pwm_val
        self.last_t = time
        self.last_pos = pos
        # Are we moving faster than our threshold?
        if sign*self.vel_IIR.getVal() > self.MOVE_THRESH:
            # If so, note the PWM value we had to apply and prepare to move the
            # next joint
            self.file_out.write( "%s: %f\n"%(self.dof_list[0],self.pwm_val) )
            print "%s: %f"%(self.dof_list[0],self.pwm_val)
            self.dof_list.pop(0)
            self.firstrun = True
        return cmd

gait = Gait()

update = gait.update
