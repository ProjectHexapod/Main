from ControlsKit import time_sources, LegController
from ControlsKit.math_utils import array, KP


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
    leg.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(array([0.0, 0.0, 0.0]))
    leg.updateLengthRateCommands()

    lr[j_idx] += delta
    return lr
