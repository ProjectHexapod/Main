from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.leg_paths import Pause


# Initialization
model = LegModel()
controller = LimbController()
path = None
ja = None


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global path, state, ja

    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Init path. Do this after the first update.
    if path is None:
        ja = model.getJointAngles()
        path = Pause(model, controller, 1.0)
    
    # Evaluate path and joint control
    controller.update(path.update(),model.getJointAngles())

    # Send commands
    return controller.getLengthRateCommands()
