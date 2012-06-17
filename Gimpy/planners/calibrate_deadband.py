from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.math_utils import array, KP


# Initialization
model = LegModel()
path = None

j_idx = KP
delta = 0.00005
lr = array([0.0, 0.0, 0.0])


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global path, state, lr

    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Evaluate path and joint control
    controller.update(model.getJointAngles(), array([0.0, 0.0, 0.0]))


    lr[j_idx] += delta
    return lr
