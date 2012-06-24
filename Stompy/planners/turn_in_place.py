from ControlsKit import time_sources, BodyModel, logger, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from scipy import zeros
from ControlsKit.leg_paths import TrapezoidalFootMove

body = BodyModel()
path = None
state = 0

TURN_FIRST_TRIPOD = 1
TURN_SECOND_TRIPOD = 2
RESOLVE = 3

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates):
    global path, state
    
    time_sources.global_time.updateTime(time)
    body.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    if path is None:
        path = BodyPause(model, controller, .1)
        state = TURN_FIRST_TRIPOD
    
    if path.isDone():
        if state==TURN_FIRST_TRIPOD:
            state=TURN_SECOND_TRIPOD
        if state==TURN_SECOND_TRIPOD:
            state=RESOLVE
        if state==RESOLVE:
            state=TURN_FIRST_TRIPOD
    
    
    target_angle_matrix = path.update()
    body.setDesiredJointAngles(joint_angle_matrix)
    
    # Send commands
    return controller.update(model.getJointAngleMatrix(), target_angle_matrix)

def turnBody(angle):
	pass
