from ControlsKit import time_sources, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from scipy import zeros
from ControlsKit.leg_trajectories import TrapezoidalFootMove

body = BodyController()
traj = None
state = 0

TURN = 1
RESOLVE = 2

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates):
    global traj, state
    
    time_sources.global_time.updateTime(time)
    body.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    joint_angle_matrix = turnBody(desired_orientation, imu_orientation)
    body.setDesiredJointAngles(joint_angle_matrix)
    return body.getLengthRateCommands()

def turnBody(angle):
	pass
