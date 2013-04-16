from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove, PutFootOnGround
from ControlsKit.math_utils import array, Z
from UI import logger
from ControlsKit.time_sources import global_time

# Initialization
model = LegModel()
controller = LimbController()
path = None

points = []
points.append((1.5,  0.75, -0.55))
points.append((1.5, -0.75, -0.55))
points.append((1.5, -0.75, -0.78))
points.append((1.5,  0.75, -0.78))
index = 0

# Body of control loop


def update(time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
    global points, path, index
    
    
    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Init path. Do this after the first update.
    if path is None:
        path = Pause(model, controller, 1.0)
    
    if path.isDone():
        path = TrapezoidalFootMove(model, controller,
                                   array(points[index]),
                                   0.5, 0.4)
        index = (index + 1) % len(points)

    # Evaluate path and joint control
    controller.update(model.getJointAngles(), path.update())

    # Send commands
    return controller.getLengthRateCommands()
