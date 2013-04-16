from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.math_utils import array
from ControlsKit.leg_paths import TrapezoidalFootMove, Pause
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
            print "Move" * 1000
            path = TrapezoidalFootMove(model, controller, array([1.5, 0.0, -0.4]), 0.5, 0.5)
            state = S_MOVE_JOINT
        elif state == S_MOVE_JOINT:
            print "Done" * 1000
            state = S_DONE
            pass
        logger.info("State changed.", state=state)
    
    print "Foot:", model.getFootPos()
    # Evaluate path and joint control
    controller.update(model.getJointAngles(), path.update())


    # Send commands
    return controller.getLengthRateCommands()
