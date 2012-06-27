from ControlsKit import time_sources, BodyModel
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from scipy import zeros


body = BodyModel()
traj = None
state = 0
leg_pair = 0
stride = 1  # in meters

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates):
    global traj, legs

    time_sources.global_time.updateTime(time)
    body.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates)
    legs = body.getLegs()

    if traj.isDone():
        pass
    # TODO: once the IK takes joint limits into account check it to see if the joint can go stride further
    # TODO: move each pair of legs forward by stride
    # TODO: with the feet on the ground move all of the feet backwards by stride

def getLeftAndRightLegsInPair(legs, pair):
    pair %= NUM_LEGS
    return legs[pair], legs[NUM_LEGS - pair - 1]

def enterState(state, legs, pair):
    left, right = getLeftAndRightLegsInPair(legs, pair)
    if state == 0:  # move all legs back by stride
        pass
    elif state == 1:
        pass
    elif state == 2:
        pass
    elif state == 3:
        pass
    elif state == 4:
        pass






