from ControlsKit import time_sources, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from scipy import zeros


body = BodyController()
traj = None
state = 0


def update(time, leg_sensor_matrix, imu_orientation, imu_angular_rates):
    global traj, state
    
    time_sources.global_time.updateTime(time)
    body.setBodyState(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    joint_angle_matrix = zeros((NUM_LEGS, LEG_DOF))
    body.setDesiredJointAngles(joint_angle_matrix)
    return body.getLengthRateCommands()
