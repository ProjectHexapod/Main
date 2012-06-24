from ControlsKit import time_sources, BodyModel, logger, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from ControlsKit.body_paths import RotateFeetAboutOrigin, BodyPause, TrapezoidalFeetAlign
from scipy import zeros

controller = BodyController()
model = BodyModel()
path = None
state = 0

ORIENT = 1
CCLOCKWISE = 2
CLOCKWISE = 3

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates):
    global path, state
    
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    target_angle_matrix = zeros((NUM_LEGS, LEG_DOF))
    
    #THIS IS WHERE WE CALL ON THE PATH TO DO MATH AND PRODUCE joint_angle_matrix (6x3 matrix)
    if path is None:
        path = BodyPause(model, controller, .1)
        state = ORIENT
    
    if path.isDone():
        if state == ORIENT:
            path = TrapezoidalFeetAlign(model, controller, [0, -.7,  2], 2, 1)
            state = CCLOCKWISE
        elif state == CCLOCKWISE:
            path = RotateFeetAboutOrigin(model, controller, [0,1,2,3,4,5], .2, 2, 1)
            state = CLOCKWISE
        elif state == CLOCKWISE:
            path = RotateFeetAboutOrigin(model, controller, [0,1,2,3,4,5], -.2, 2, 1)
            state = CCLOCKWISE
        elif state == 0:
            path = BodyPause(model, controller, 10)

        logger.info("State changed.", state=state)
    
    # Evaluate path and joint control
    target_angle_matrix  = path.update()

    # Send commands
    return controller.update(model.getJointAngleMatrix(), target_angle_matrix)
