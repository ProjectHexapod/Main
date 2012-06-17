from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.math_utils import YAW, HP, KP


# Initialization
model = LegModel()
controller = LimbController()
ja = None
sw = None


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth):
    global state, ja, sw

    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Init path. Do this after the first update.
    if ja is None:
        ja = model.getJointAngles()
        ja[HP] = -0.7
        ja[KP] = 1.5
        sw = time_sources.StopWatch()
        print "SW1"
    print "between"
    if sw.getTime() > 5.0:
        if ja[KP] == 1.5:
            ja[KP] = 1.8
        else:
            ja[KP] = 1.5
        sw = time_sources.StopWatch()
    
    # Evaluate path and joint control
    controller.update(ja,model.getJointAngles())


    # Send commands
    lr = controller.getLengthRateCommands()
    lr[YAW] = 0.0
    lr[HP] = 0.0
    return lr

