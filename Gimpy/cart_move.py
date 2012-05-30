from ControlsKit import time_sources, LegController, logger
from ControlsKit.math_utils import array
from ControlsKit.trajectories import TrapezoidalFootMove, Pause


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
    leg.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Init traj. Do this after the first update.
    if traj is None:
        traj = Pause(leg, 5.0)

    # Monitor trajectories
    if traj.isDone():
        if state == S_INIT:
            print "Move"*1000
            traj = TrapezoidalFootMove(leg, array([1.5, 0.0, -0.4]), 0.5, 0.5)
            state = S_MOVE_JOINT
        elif state == S_MOVE_JOINT:
            print "Done"*1000
            state = S_DONE
            pass
        logger.info("State changed.", state=state)
    
    print "Foot:", leg.getFootPos()
    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(traj.update())
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()
