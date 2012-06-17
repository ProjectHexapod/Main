from ControlsKit import time_sources, BodyModel, logger, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from ControlsKit.body_paths import TrapezoidalSitStand, BodyPause
from scipy import zeros

controller = BodyController()
model = BodyModel()
path = None
state = 0

STAND = 1
SIT = 2

state = STAND

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates):
    global path, state
    
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    joint_angle_matrix = zeros((NUM_LEGS, LEG_DOF))
    
    #THIS IS WHERE WE CALL ON THE PATH TO DO MATH AND PRODUCE joint_angle_matrix (6x3 matrix)
    if path is None:
        path = BodyPause(model, controller, 2)
        state = SIT
    
    if path.isDone():
        if state == SIT:
            path = TrapezoidalSitStand(model, 0, 1, .5)
            state = STAND
        logger.info("State changed.", state=state)
    
    # Evaluate path and joint control
    joint_angle_matrix  = path.update()

    # Send commands
    return controller.update(model.getJointAngleMatrix(), joint_angle_matrix)
