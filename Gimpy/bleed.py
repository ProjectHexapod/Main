from ControlsKit import time_sources, LegController
from ControlsKit.math_utils import array


# Initialization
leg = LegController()
traj = None


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state

    # Update leg
    time_sources.global_time.updateTime(time)
    leg.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(leg.getJointAngles())
    leg.updateLengthRateCommands()


    return array([0.0, 5.0, 0.0])
