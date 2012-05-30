from leg_logger import logger
from math_utils import *
import time_sources
from leg_controller import LegController
from trajectories import PutFootOnGround, TrapezoidalFootMove, Pause, MoveJoint

# Initialization
leg = LegController()
traj = None
print('here')


# States
S_MOVE1 = 0
S_MOVE2 = 1
S_DONE = 10
S_INIT = 11

state = S_INIT


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state

    # Update leg
    time_sources.global_time.updateTime(time)
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Init traj. Do this after the first update.
    if traj is None:
        traj = Pause(leg, 5.0)
        traj.initial_angles[HP] = -0.6

    # Monitor trajectories
    if traj.isDone():
        if state == S_INIT:
            print "Move"*1000
            traj = MoveJoint(leg, joint_idx=KP, duration=3.0, direction=1, velocity=0.2)
            state = S_MOVE1
        elif state == S_MOVE1:
            print "Move"*1000
            traj = MoveJoint(leg, joint_idx=KP, duration=3.0, direction=-1, velocity=0.2)
            state = S_MOVE2
        elif state == S_MOVE2:
            print "Done"*1000
            state = S_INIT
            pass
        logger.info("State changed.", state=state)
    
    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(traj.update())
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()
