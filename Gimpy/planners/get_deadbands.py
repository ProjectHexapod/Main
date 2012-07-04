from ControlsKit import time_sources, LegModel, leg_logger, LimbController
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove, PutFootOnGround
from ControlsKit.math_utils import array, Z


# Initialization
model = LegModel()
controller = LimbController()
path = None
state = 0

class IIR(object):
    def __init__(self, val_init, k=.9, t_init=0, t_const=1 ):
        """
        By default, absorb .9 of the update value in 1 second
        """
        self.k = k**(t_const)
        self.state = val_init
        self.t = t_init
    def getVal(self):
        return self.state
    def update(self, val, t):
        dt = t-self.t
        adjusted_k = self.k**(1/dt)
        self.state *= (1-adjusted_k)
        self.state += adjusted_k*val
        self.t = t

file_out = file('offsets.txt', 'w+')
vel_IIR = None
pwm_val = 0
last_pos = 0
last_t = 0

MOVE_THRESH = .03

# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
    global path, state, file_out, vel_IIR, pwm_val, last_pos, last_t
    
    cmd = [0,0,0]

    if state == 0:
        # Initialize to test hip pitch
        vel_IIR = IIR( 0.0, k=.9, t_init=time, t_const=0.5 )
        last_t = time
        last_pos = hip_pitch
        state += 1
    elif state == 1:
        dt = time-last_time
        vel_est = (hip_pitch-last_pos)/(time-last_t)
        vel_IIR.update(vel_est, time)
        pwm_val += dt*10
        cmd[1] = pwm_val
        last_t = time
        last_pos = hip_pitch
        if abs(vel_IIR.getVal()) > MOVE_THRESH:
            file_out.write( "pitch extend: %f\n"%pwm_val )
            print "Limit hit! %f"%pwm_val
            pwm_val = 0
            vel_IIR = IIR( 0.0, k=.9, t_init=time, t_const=0.5 )
            state += 1
    elif state == 2:
        dt = time-last_time
        vel_est = (hip_pitch-last_pos)/(time-last_t)
        vel_IIR.update(vel_est, time)
        pwm_val += dt*10
        cmd[1] = -pwm_val
        last_t = time
        last_pos = hip_pitch
        if abs(vel_IIR.getVal()) > MOVE_THRESH:
            file_out.write( "pitch retract: %f\n"%pwm_val )
            print "Limit hit! %f"%pwm_val
            pwm_val = 0
            vel_IIR = IIR( 0.0, k=.9, t_init=time, t_const=0.5 )
            last_pos = knee_pitch
            state += 1
    elif state == 3:
        dt = time-last_time
        vel_est = (knee_pitch-last_pos)/(time-last_t)
        vel_IIR.update(vel_est, time)
        pwm_val += dt*10
        cmd[2] = pwm_val
        last_t = time
        last_pos = knee_pitch
        if abs(vel_IIR.getVal()) > MOVE_THRESH:
            file_out.write( "knee extend: %f\n"%pwm_val )
            print "Limit hit! %f"%pwm_val
            pwm_val = 0
            vel_IIR = IIR( 0.0, k=.9, t_init=time, t_const=0.5 )
            state += 1
    elif state == 4:
        dt = time-last_time
        vel_est = (knee_pitch-last_pos)/(time-last_t)
        vel_IIR.update(vel_est, time)
        pwm_val += dt*10
        cmd[2] = -pwm_val
        last_t = time
        last_pos = knee_pitch
        if abs(vel_IIR.getVal()) > MOVE_THRESH:
            file_out.write( "knee_retract: %f\n"%pwm_val )
            print "Limit hit! %f"%pwm_val
            pwm_val = 0
            last_pos = yaw
            vel_IIR = IIR( 0.0, k=.9, t_init=time, t_const=0.5 )
            state += 1
    elif state == 5:
        dt = time-last_time
        vel_est = (yaw-last_pos)/(time-last_t)
        vel_IIR.update(vel_est, time)
        pwm_val += dt*10
        cmd[0] = pwm_val
        last_t = time
        last_pos = yaw
        if abs(vel_IIR.getVal()) > MOVE_THRESH:
            file_out.write( "yaw extend: %f\n"%pwm_val )
            print "Limit hit! %f"%pwm_val
            pwm_val = 0
            vel_IIR = IIR( 0.0, k=.9, t_init=time, t_const=0.5 )
            state += 1
    elif state == 6:
        dt = time-last_time
        vel_est = (yaw-last_pos)/(time-last_t)
        vel_IIR.update(vel_est, time)
        pwm_val += dt*10
        cmd[0] = -pwm_val
        last_t = time
        last_pos = yaw
        if abs(vel_IIR.getVal()) > MOVE_THRESH:
            file_out.write( "yaw retract: %f\n"%pwm_val )
            print "Limit hit! %f"%pwm_val
            pwm_val = 0
            vel_IIR = IIR( 0.0, k=.9, t_init=time, t_const=0.5 )
            state += 1
    else:
        file_out.close()
    
    # Send commands
    return cmd
