from ControlsKit import time_sources, LegModel, leg_logger, LimbController
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove, PutFootOnGround
from ControlsKit.math_utils import array, Z


# Initialization
model = LegModel()
controller = LimbController()
path = None

S_MOVE1 = 0
S_LOWER = 1
S_MOVE2 = 2
S_MOVE3 = 3

state = S_MOVE3


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
    global path, state
    
    
    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Init path. Do this after the first update.
    if path is None:
        path = Pause(model, controller, 1.0)
    
    # Monitor leg_paths
    if path.isDone():
        if state == S_MOVE3:
            path = TrapezoidalFootMove(model, controller,
                                       array([1.5, -0.6, -0.4]),
                                       0.2, 0.1)
            state = S_MOVE1
        elif state == S_MOVE1:
            path = PutFootOnGround(model, controller, 0.05)
            state = S_LOWER
        elif state == S_LOWER:
            ground_level = model.getFootPos()[Z]
            path = TrapezoidalFootMove(model, controller,
                                       array([1.5, .6, ground_level]),
                                       0.2, 0.1)
            state = S_MOVE2
        elif state == S_MOVE2:
            path = TrapezoidalFootMove(model, controller,
                                       array([1.5, 0.6, -0.4]),
                                       0.2, 0.1)
            state = S_MOVE3
        leg_logger.logger.info("State changed.", state=state)

    # Evaluate path and joint control
    controller.update(model.getJointAngles(), path.update())

    # Send commands
    return controller.getLengthRateCommands()
