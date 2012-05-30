from leg_logger import logger
from math_utils import *
import time_sources
from leg_controller import LegController
from trajectories import PutFootOnGround, TrapezoidalJointMove, Pause

# Initialization
leg = LegController()
traj = None


# States
S_MOVE_JOINT = 0
S_DONE = 1
S_INIT = 2

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

    # Monitor trajectories
    if traj.isDone():
        if state == S_INIT:
            print "Move"*1000
            traj = TrapezoidalJointMove(leg, final_angles=[0, -0.59483773, 1.81300376],
                                        max_velocity=1, acceleration=.1) # Simulation starts at angles=[-0.7504911, -0.99483773, 1.21300376]
            state = S_MOVE_JOINT
        elif state == S_MOVE_JOINT:
            print "Done"*1000
            state = S_DONE
            pass
        logger.info("State changed.", state=state)
    
    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(traj.update())
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()

