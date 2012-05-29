import sys
sys.path.append('../..')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnStand
from SimulationKit.helpers import *
from leg_logger import logger

from move_all_joint import update

d = {'offset':(0,0,0.67)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=1,robot=LegOnStand,robot_kwargs=d, start_paused = True)

yaw_joint = s.robot.members['hip_yaw']
pitch_joint = s.robot.members['hip_pitch']
knee_joint = s.robot.members['knee_pitch']
shock_joint = s.robot.members['foot_shock']

time_1 = 0.0
try:
    while True:
        s.step()

        time = s.getSimTime()
        if time != time_1:
            lr = update(time, yaw_joint.getAngle(), pitch_joint.getAngle(), knee_joint.getAngle(), shock_joint.getPosition())
            logger.info("Main loop iteration", time=time, hip_yaw_rate=lr[0], hip_pitch_rate=lr[1], knee_pitch_rate=lr[2], hip_yaw_angle=yaw_joint.getAngle(), hip_pitch_angle=pitch_joint.getAngle(), knee_pitch_angle=knee_joint.getAngle(), shock_depth=shock_joint.getPosition())
            yaw_joint.setLengthRate(lr[0])
            pitch_joint.setLengthRate(lr[1])
            knee_joint.setLengthRate(lr[2])
        
            time_1 = time

except:
    logger.error("Main loop exception!")
    yaw_joint.setLengthRate(0)
    pitch_joint.setLengthRate(0)
    knee_joint.setLengthRate(0)
    raise
