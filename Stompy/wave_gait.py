from ControlsKit import time_sources, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from scipy import zeros

body = BodyController()
traj = None
state = 0
stride = 1  # in meters

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates):
    global traj, state

    time_sources.global_time.updateTime(time)
    body.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates)
    # TODO: write me
