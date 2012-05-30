from leg_logger import logger
from math_utils import *
import time_sources
from leg_controller import LegController
from trajectories import PutFootOnGround, TrapezoidalFootMove, Pause


# Initialization
leg = LegController()
traj = None

j_idx = KP
delta = 0.00005
lr = array([0.0, 0.0, 0.0])


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state, lr

    # Update leg
    time_sources.global_time.updateTime(time)
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(array([0.0, 0.0, 0.0]))
    leg.updateLengthRateCommands()

    lr[j_idx] += delta
    return lr

