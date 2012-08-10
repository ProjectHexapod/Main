from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.leg_paths import SafeMove, Pause
from UI import logger


# Initialization
model = LegModel()
controller = LimbController()
path = None


# States
S_MOVE_JOINT = 0
S_DONE = 1
S_INIT = 2

state = S_INIT


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
    global path, state

    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Init path. Do this after the first update.
    if path is None:
        path = Pause(model, controller, 5.0)

    # Monitor leg_paths
    if path.isDone():
        if state == S_INIT:
            path = SafeMove(model, controller, [2, 1, .5], 1, .1, 0) # Simulation starts at angles=[-0.7504911, -0.99483773, 1.21300376]
            state = S_MOVE_JOINT
        elif state == S_MOVE_JOINT:
            path = SafeMove(model, controller, [1.5, -.5, -1], 1, .1, 0) # Simulation starts at angles=[-0.7504911, -0.99483773, 1.21300376]
            state = 3
        elif state == 3:
            path = SafeMove(model, controller, [1.5, .5, -1], 1, .1, 0) # Simulation starts at angles=[-0.7504911, -0.99483773, 1.21300376]
            state = 4
        elif state == 4:
            path = SafeMove(model, controller, [2, -1, .5], 1, .1, 0) # Simulation starts at angles=[-0.7504911, -0.99483773, 1.21300376]
            state = S_INIT
        elif state == 5:
            state = S_DONE
            pass
        logger.info("State changed.", state=state)

    # Evaluate path and joint control
    controller.update(model.getJointAngles(), path.update())

    # Send commands
    return controller.getLengthRateCommands()

