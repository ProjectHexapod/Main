from leg_logger import logger
from math_utils import *
import time_sources
from leg_controller import LegController
from trajectories import PutFootOnGround, TrapezoidalFootMove, Pause


# Initialization
leg = LegController()
ja = None
sw = None

# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global state, ja, sw

    # Update leg
    time_sources.global_time.updateTime(time)
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Init traj. Do this after the first update.
    if ja is None:
        ja = leg.getJointAngles()
        ja[HP] = -0.7
        ja[KP] = 1.5
        sw = time_sources.StopWatch()
        print "SW1"
    print "between"
    if sw.getTime() > 5.0:
        if ja[KP] == 1.5:
            ja[KP] = 1.8
        else:
            ja[KP] = 1.5
        sw = time_sources.StopWatch()
    
    # Evaluate trajectory and joint control
#    print "JA command:", ja
#    print "JA measured:", leg.getJointAngles()
    leg.setDesiredJointAngles(ja)
    leg.updateLengthRateCommands()

    # Send commands
    lr = leg.getLengthRateCommands()
    lr[YAW] = 0.0
    lr[HP] = 0.0
    return lr

