from leg_controller import LegController
import behaviors


# Initialization
leg = LegController()
state = 0
traj = behaviors.PutFootOnGround(leg, 0.05)


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    # Monitor trajectories
    if traj.isDone():
        # traj = behaviors.?
        pass

    # Update leg
    leg.setTime(time)
    leg.setLegState(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Evaluate trajectory and joint control
    leg.setDesiredJointAngles(traj.update(time))
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()
