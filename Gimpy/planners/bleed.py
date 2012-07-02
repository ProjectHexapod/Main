from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.math_utils import array


# Initialization
model = LegModel()
controller = LimbController()
path = None


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
    global path, state

    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Evaluate path and joint control
    controller.update(model.getJointAngles(), path.update())


    return array([0.0, 5.0, 0.0])
