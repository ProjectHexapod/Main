from math_utils import *
from leg_controller import LegController
import behaviors


# Initialization
leg = LegController()
state = 0
traj = None


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global state, traj
    
    
    # Update leg
    leg.setTime(time)
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Monitor trajectories
    if state == 1:
        state = 2
        traj = behaviors.PutFootOnGround(leg, 0.1)
        # traj = behaviors.?
        pass

    # Evaluate trajectory and joint control
    if time < 2.0:
        leg.setDesiredJointAngles(array([0.0, -0.5, 0.1 + pi_2]))
    elif state == 0:
        state = 1
    if traj is not None:
        if leg.isFootOnGround():
            print leg.getLegState(), traj.isDone()
        leg.setDesiredJointAngles(traj.update(time, leg.getDeltaTime()))
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()
