from ControlsKit import time_sources, BodyModel, logger, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from scipy import zeros
from ControlsKit.body_paths import RotateFeetAboutOrigin, BodyPause
from ControlsKit.body_paths import TrapezoidalFeetAlign, TrapezoidalFeetLiftLower
from ControlsKit.leg_paths import TrapezoidalFootMove

controller=BodyController()
model = BodyModel()
path = None
state = 0

RAISE_FIRST_TRIPOD = 1
TURN_FIRST_TRIPOD = 2
RAISE_SECOND_TRIPOD = 3
TURN_SECOND_TRIPOD = 4
RESOLVE = 5
STAND = 6

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates):
    global path, state
    
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    if path is None:
        path = BodyPause(model, controller, .1)
        state = STAND
    
    if path.isDone():
        if state == STAND:
            path = TrapezoidalFeetAlign(model, controller, [0, -.7,  2], 2, 1)
            state = RAISE_FIRST_TRIPOD
        if state == RAISE_FIRST_TRIPOD:
            path = TrapezoidalFeetLiftLower(model, controller, [0,2,4], .3, 2, 1)
            state = TURN_FIRST_TRIPOD
        if state == TURN_FIRST_TRIPOD:
            path = RotateFeetAboutOrigin(model, controller, [0,2,4], .2, 2, 1)
            state = RAISE_SECOND_TRIPOD
        if state == RAISE_SECOND_TRIPOD:
            path = TrapezoidalFeetLiftLower(model, controller, [1,3,5], .3, 2, 1)
            state = TURN_SECOND_TRIPOD
        if state == TURN_SECOND_TRIPOD:
            path = RotateFeetAboutOrigin(model, controller, [1,3,5], .2, 2, 1)
            state = RESOLVE
        if state == RESOLVE:
            path = RotateFeetAboutOrigin(model, controller, range(5), -.2, 2, 1)
            state = RAISE_FIRST_TRIPOD
    
    
    target_angle_matrix = path.update()
    #controller.setDesiredJointAngles(joint_angle_matrix)
    
    # Send commands
    return controller.update(model.getJointAngleMatrix(), target_angle_matrix)

def turnBody(angle):
	pass
