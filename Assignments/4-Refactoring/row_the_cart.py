from math_utils import *
from leg_controller import LegController
import behaviors


# Initialization
leg = LegController()
traj = None

S_INIT_MOVE1 = 0
S_MOVE1 = 1
S_INIT_LOWER = 2
S_LOWER = 3
S_INIT_MOVE2 = 4
S_MOVE2 = 5
S_INIT_MOVE3 = 6
S_MOVE3 = 7

state = S_INIT_MOVE1


def waitFor(traj):
    if traj.isDone():
        return 1
    else:
        return 0

# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state
    
    
    # Update leg
    leg.setTime(time)
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Monitor trajectories
    if state == S_INIT_MOVE1:
        traj = behaviors.TrapezoidalFootMove(leg,
                                             array([1.5, -0.6, -0.4]),
                                             0.2, 0.1)
        state = S_MOVE1
    elif state == S_MOVE1:
        state += waitFor(traj)
    elif state == S_INIT_LOWER:
        traj = behaviors.PutFootOnGround(leg, 0.05)
        state = S_LOWER
    elif state == S_LOWER:
        state += waitFor(traj)
    elif state == S_INIT_MOVE2:
        traj = behaviors.TrapezoidalFootMove(leg,
                                             array([1.5, 0.6, leg.getFootPos()[Z]]),
                                             0.2, 0.1)
        state = S_MOVE2
    elif state == S_MOVE2:
        state += waitFor(traj)
    elif state == S_INIT_MOVE3:
        traj = behaviors.TrapezoidalFootMove(leg,
                                             array([1.5, 0.6, -0.4]),
                                             0.2, 0.1)
        state = S_MOVE3
    elif state == S_MOVE3:
        state += waitFor(traj)
    else:
        state = S_INIT_MOVE1

    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(traj.update(time, leg.getDeltaTime()))
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()
