from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.math_utils import array, KP, HP, YAW


# Initialization
model = LegModel()
controller = LimbController()
path = None

j_idx = YAW
delta = 0.00005
lr = array([0.0, 0.0, 0.0])

file_name = "gimpy_calibration_of_joint_%d.csv" % j_idx
flie = open(file_name, "w")


# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
    global path, state, lr

    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Evaluate path and joint control
    JA = model.getJointAngles()
    controller.update(JA, array([0.0, 0.0, 0.0]))


    flie.write("%f,%f,%f,%f,%f,%f\n" % (lr[0], lr[1], lr[2], JA[0], JA[1], JA[2]))
    
    lr[j_idx] += delta
    return lr
