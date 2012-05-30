from leg_logger import logger
from math_utils import *
import time_sources
from leg_controller import LegController
from trajectories import PutFootOnGround, TrapezoidalFootMove, Pause


# Initialization
leg = LegController()
traj = None


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state

    # Update leg
    time_sources.global_time.updateTime(time)
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(leg.getJointAngles())
    leg.updateLengthRateCommands()


    return array([0.0, 5.0, 0.0])

