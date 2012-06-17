from ControlsKit import time_sources, LegModel, logger, LimbController
from ControlsKit.leg_paths import Pause, MoveJoint
from ControlsKit.math_utils import HP, KP


# Initialization
model = LegModel()
controller = LimbController()
path = None


# States
S_MOVE1 = 0
S_MOVE2 = 1
S_DONE = 10
S_INIT = 11

state = S_INIT


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global path, state

    # Update leg model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Init path. Do this after the first update.
    if path is None:
        path = Pause(model, controller, 5.0)
        path.initial_angles[HP] = -0.6

    # Monitor model_path
    if path.isDone():
        if state == S_INIT:
            print "Move"*1000
            path = MoveJoint(model, controller, joint_idx=KP, duration=3.0, direction=1, velocity=0.2)
            state = S_MOVE1
        elif state == S_MOVE1:
            print "Move"*1000
            path = MoveJoint(model, controller, joint_idx=KP, duration=3.0, direction=-1, velocity=0.2)
            state = S_MOVE2
        elif state == S_MOVE2:
            print "Done"*1000
            state = S_INIT
            pass
        logger.info("State changed.", state=state)
    
    # Evaluate path and joint control
    controller.update(model.getJointAngles(), path.update())

    # Send commands
    return controller.getLengthRateCommands()
