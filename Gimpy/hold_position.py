from ControlsKit import time_sources, LegController
from ControlsKit.trajectories import Pause


# Initialization
leg = LegController()
traj = None
ja = None


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global traj, state, ja

    # Update leg
    time_sources.global_time.updateTime(time)
    leg.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    leg.updateFootOnGround()

    # Init traj. Do this after the first update.
    if traj is None:
        ja = leg.getJointAngles()
        traj = Pause(leg, 1.0)
    
    # Evaluate trajectory and joint control
#    print "JA command:", ja
#    print "JA measured:", leg.getJointAngles()
    leg.setDesiredJointAngles(ja)
    leg.updateLengthRateCommands()

    # Send commands
    return leg.getLengthRateCommands()
