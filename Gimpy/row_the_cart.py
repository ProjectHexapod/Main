from ControlsKit import time_sources, LegController, logger
from ControlsKit.trajectories import Pause, TrapezoidalFootMove, PutFootOnGround
from ControlsKit.math_utils import array, Z


# Initialization
leg = LegController()
traj = None

S_MOVE1 = 0
S_LOWER = 1
S_MOVE2 = 2
S_MOVE3 = 3

state = S_MOVE3


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state
    
    
    # Update leg
    time_sources.global_time.updateTime(time)
    leg.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Init traj. Do this after the first update.
    if traj is None:
        traj = Pause(leg, 1.0)
    
    # Monitor trajectories
    if traj.isDone():
        if state == S_MOVE3:
            traj = TrapezoidalFootMove(leg,
                                       array([1.5, -0.6, -0.4]),
                                       0.2, 0.1)
            state = S_MOVE1
        elif state == S_MOVE1:
            traj = PutFootOnGround(leg, 0.05)
            state = S_LOWER
        elif state == S_LOWER:
            ground_level = leg.getFootPos()[Z]
            traj = TrapezoidalFootMove(leg,
                                       array([1.5, .6, ground_level]),
                                       0.2, 0.1)
            state = S_MOVE2
        elif state == S_MOVE2:
            traj = TrapezoidalFootMove(leg,
                                       array([1.5, 0.6, -0.4]),
                                       0.2, 0.1)
            state = S_MOVE3
        logger.info("State changed.", state=state)

    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(traj.update())
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()
