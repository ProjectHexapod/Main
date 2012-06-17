from ControlsKit import time_sources, LegController, logger
from ControlsKit.leg_trajectories import Pause, MoveJoint
from ControlsKit.math_utils import HP, KP


# Initialization
leg = LegController()
traj = None


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
    leg.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Init traj. Do this after the first update.
    if traj is None:
        traj = Pause(leg, 5.0)
        traj.initial_angles[HP] = -0.6

    # Monitor leg_trajectories
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
