from ControlsKit import time_sources, LegModel, logger, LimbController
from ControlsKit.Paths import Pause, TrapezoidalFootMove, PutFootOnGround
from ControlsKit.math_utils import array, Z


# Initialization
model = LegModel()
controller = LimbController()
traj = None

S_MOVE1 = 0
S_LOWER = 1
S_MOVE2 = 2
S_MOVE3 = 3

state = S_MOVE3


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state
    
    
    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Init traj. Do this after the first update.
    if traj is None:
        traj = Pause(model, controller, 1.0)
    
    # Monitor leg_trajectories
    if traj.isDone():
        if state == S_MOVE3:
            traj = TrapezoidalFootMove(model, controller,
                                       array([1.5, -0.6, -0.4]),
                                       0.2, 0.1)
            state = S_MOVE1
        elif state == S_MOVE1:
            traj = PutFootOnGround(model, controller, 0.05)
            state = S_LOWER
        elif state == S_LOWER:
            ground_level = model.getFootPos()[Z]
            traj = TrapezoidalFootMove(model, controller,
                                       array([1.5, .6, ground_level]),
                                       0.2, 0.1)
            state = S_MOVE2
        elif state == S_MOVE2:
            traj = TrapezoidalFootMove(model, controller,
                                       array([1.5, 0.6, -0.4]),
                                       0.2, 0.1)
            state = S_MOVE3
        logger.info("State changed.", state=state)

    # Evaluate path and joint control
    controller.update(model.getJointAngles(), path.update())

    # Send commands
    return controller.getLengthRateCommands()