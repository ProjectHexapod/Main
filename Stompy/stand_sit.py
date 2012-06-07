from ControlsKit import time_sources, BodyController, logger
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from ControlsKit.body_trajectories import TrapezoidalSitStand
from scipy import zeros

body = BodyController()
traj = None
state = 0

STAND = 1
SIT = 2

state = STAND

def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates):
    global traj, state
    
    time_sources.global_time.updateTime(time)
    body.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    joint_angle_matrix = zeros((NUM_LEGS, LEG_DOF))
    
    #THIS IS WHERE WE CALL ON THE TRAJ TO DO MATH AND PRODUCE joint_angle_matrix (6x3 matrix)
    if traj is None:
        traj = TrapezoidalSitStand(body, .2, 1, .5)
        state = SIT
    
    if traj.isDone():
        if state == SIT:
            traj = TrapezoidalSitStand(body, 0, 1, .5)
            state = STAND
        logger.info("State changed.", state=state)
    
    # Evaluate trajectory and joint control
    joint_angle_matrix  = traj.update()

    body.setDesiredJointAngles(joint_angle_matrix)
    
    # Send commands
    return body.getLengthRateCommands()
