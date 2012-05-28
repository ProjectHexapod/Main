from leg_logger import logger
from math_utils import *
import time_sources
from leg_controller import LegController
from trajectories import PutFootOnGround, TrapezoidalFootMove, Pause


# Initialization
leg = LegController()
traj = None
ja = None

# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state, ja

    # Update leg
    time_sources.global_time.updateTime(time)
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Init traj. Do this after the first update.
    if traj is None:
        ja = leg.getJointAngles()
        traj = Pause(leg, 1.0)
    
    # Evaluate trajectory and joint control
#    print "JA command:", ja
#    print "JA measured:", leg.getJointAngles()
    leg.setDesiredJointAngles(ja)
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()

