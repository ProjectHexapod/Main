from ControlsKit import time_sources, BodyModel, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from scipy import zeros
from ControlsKit.body_paths import RotateFeetAboutOrigin, BodyPause
from ControlsKit.body_paths import GoToStandardHexagon, TrapezoidalFeetLiftLower
from ControlsKit.leg_paths import TrapezoidalFootMove

controller = BodyController()
model = BodyModel()
path = None
state = 0

RAISE_FIRST_TRIPOD = 1
TURN_FIRST_TRIPOD = 2
RAISE_SECOND_TRIPOD = 3
TURN_SECOND_TRIPOD = 4
FEET_ON_GROUND = leg_lift_height = .2
RESOLVE = 6
STAND = 7
PAUSE = 8

LIFT_TRIPOD_024 = [1, -1, 1, -1, 1, -1]
LIFT_TRIPOD_135 = [-i for i in LIFT_TRIPOD_024]
TURN_ANGLE = 0.2


def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates, command):
    global path, state, leg_lift_height

    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)

    target_angle_matrix = zeros((NUM_LEGS, LEG_DOF))

    if path is None:
        path = BodyPause(model, controller, 1)
        state = STAND
        leg_lift_height = .2

    if path.isDone():
        if state == STAND:
            path = GoToStandardHexagon(model, controller)
            state = RAISE_FIRST_TRIPOD
        elif state == RAISE_FIRST_TRIPOD:
            path = TrapezoidalFeetLiftLower(model, controller, range(NUM_LEGS),
                                            [i * leg_lift_height for i in LIFT_TRIPOD_024], 2, 1)
            state = TURN_FIRST_TRIPOD
        elif state == TURN_FIRST_TRIPOD:
            path = RotateFeetAboutOrigin(model, controller, [0, 2, 4], TURN_ANGLE, 2, 1)
            state = RAISE_SECOND_TRIPOD
        elif state == RAISE_SECOND_TRIPOD:
            leg_lift_height = .4
            path = TrapezoidalFeetLiftLower(model, controller, range(NUM_LEGS),
                                            [i * leg_lift_height for i in LIFT_TRIPOD_135], 2, 1)
            state = TURN_SECOND_TRIPOD
        elif state == TURN_SECOND_TRIPOD:
            path = RotateFeetAboutOrigin(model, controller, [1, 3, 5], TURN_ANGLE, 2, 1)
            state = FEET_ON_GROUND
        elif state == FEET_ON_GROUND:
            leg_lift_height = .2
            path = TrapezoidalFeetLiftLower(model, controller, range(NUM_LEGS),
                                            [i * leg_lift_height for i in LIFT_TRIPOD_024], 2, 1)
            state = RESOLVE
        elif state == RESOLVE:
            path = RotateFeetAboutOrigin(model, controller, range(NUM_LEGS), -TURN_ANGLE, 2, 1)
            state = RAISE_FIRST_TRIPOD

    target_angle_matrix = path.update()
    # controller.setDesiredJointAngles(joint_angle_matrix)

    # Send commands
    return controller.update(model.getJointAngleMatrix(), target_angle_matrix)


def turnBody(angle):
    pass
