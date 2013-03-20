from ControlsKit.filters import LowPassFilter
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove, PutFootOnGround
from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.time_sources import global_time
from ControlsKit.math_utils import array

# Initialization

class Gait:
    def __init__(self):
        self.file_out = file('offsets.txt', 'w+')
        self.vel_IIR = None
        self.pwm_val = 0
        self.last_pos = 0
        self.last_t = 0
        self.MOVE_THRESH = .035
        self.STOP_THRESH = .005
        self.firstrun = True
        self.dof_list = []
        self.dof_list.append('knee_pitch_r')
        self.dof_list.append('knee_pitch_e')
        self.dof_list.append('hip_pitch_r')
        self.dof_list.append('hip_yaw_e')
        self.dof_list.append('hip_yaw_r')
        self.dof_list.append('hip_pitch_e')
        self.dof_list.append('hip_pitch_r')
        self.callback = self.moveToInitialPosition
        self.model = LegModel()
        self.controller = LimbController()
    def update( self, *args, **kwargs ):
        global_time.updateTime(args[0])
        return self.callback(*args, **kwargs)
    def moveToInitialPosition( self, time, yaw, hip_pitch, knee_pitch, shock_depth, command=None ):
        self.model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
        if not hasattr(self, 'initial_path'):
            print "Starting move to initial position"
            self.initial_path = TrapezoidalFootMove(self.model, self.controller,\
                                       array([1.6, 0.0, -1.15]),\
                                       0.4, 0.2)
        self.controller.update(self.model.getJointAngles(), self.initial_path.update())
        if self.initial_path.isDone():
            self.callback = self.pause
        lr = self.controller.getLengthRateCommands()
        return lr
    def pause( self, time, yaw, hip_pitch, knee_pitch, shock_depth, command=None ):
        if not hasattr( self, 'start_pause_time' ):
            print "Waiting..."
            self.start_pause_time = time
            #self.pause_path = Pause( self.model, self.controller, 3.0 )
        #self.controller.update(self.model.getJointAngles(), self.pause_path.update())
        if time - self.start_pause_time > 3.0:
            self.callback = self.discoverDeadband
            del self.start_pause_time
        return [0.0,0.0,0.0]
    def discoverDeadband( self, time, yaw, hip_pitch, knee_pitch, shock_depth, command=None ):
        # Have we made it through all the joints?
        if not len(self.dof_list):
            # FIXME: Exit safely
            self.file_out.close()
            self.callback = self.pause
            return
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
        cmd = [0.0,0.0,0.0]
        # Is this our first tick on a new DOF?
        if self.firstrun:
            # Initialize state variables
            print "Initializing for %s"%self.dof_list[0]
            self.pwm_val = 0
            self.vel_IIR = LowPassFilter( gain=1.0, corner_frequency=2.0 )
            self.firstrun = False
            self.moving = 0
        else:
            # Calculate velocity, update filter
            dt = time-self.last_t
            dpos = pos - self.last_pos
            vel_est = dpos/dt
            self.vel_IIR.update(vel_est)
            # Take 20 seconds to ramp valve command
            if not self.moving:
                self.pwm_val += dt*0.05
            cmd[cmd_i] = sign*self.pwm_val
        self.last_t = time
        self.last_pos = pos
        # Are we moving faster than our threshold?
        if not self.moving and sign*self.vel_IIR.getVal() > self.MOVE_THRESH:
            # If so, note the PWM value we had to apply and prepare to move the
            # next joint
            self.file_out.write( "%s: %f\n"%(self.dof_list[0],self.pwm_val) )
            print "%s: %f"%(self.dof_list[0],self.pwm_val)
            self.moving = True
        if self.moving and sign*self.vel_IIR.getVal() < self.STOP_THRESH:
            self.dof_list.pop(0)
            self.firstrun = True
            self.moving=False
            self.callback = self.pause
        return cmd

gait = Gait()

update = gait.update
controller = gait.controller
