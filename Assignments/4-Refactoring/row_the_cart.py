from leg_logger import logger
from math_utils import *
import time_sources
from leg_controller import LegController
from trajectories import PutFootOnGround, TrapezoidalFootMove


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
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Monitor trajectories
    if traj is None or traj.isDone():
        if state == S_MOVE3:
            traj = TrapezoidalFootMove(leg,
                                       array([1.5, -0.6, -0.4]),
                                       0.2, 0.1)
            state = S_MOVE1
            logger.info("Entering MOVE1", state="S_MOVE1", trap_max_vel=.2, trap_acc=.1)
        elif state == S_MOVE1:
            traj = PutFootOnGround(leg, 0.05)
            state = S_LOWER
            logger.info("Entering S_LOWER", state="S_LOWER", trap_max_vel=.2, trap_acc=.1)
        elif state == S_LOWER:
            ground_level = leg.getFootPos()[Z]
            for i in range(1000):
                print ground_level
            target_coords = [1.5, .6, ground_level]
            traj = TrapezoidalFootMove(leg, array(target_coords), 0.2, 0.1)
            state = S_MOVE2
            logger.info("Entering MOVE2", state="S_MOVE2", trap_max_vel=.2, trap_acc=.1)
        elif state == S_MOVE2:
            traj = TrapezoidalFootMove(leg,
                                       array([1.5, 0.6, -0.4]),
                                       0.2, 0.1)
            state = S_MOVE3
            logger.info("Entering MOVE3", state="S_MOVE23", trap_max_vel=.2, trap_acc=.1)

    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(traj.update())
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()
