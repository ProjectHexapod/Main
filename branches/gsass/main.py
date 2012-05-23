import sys
sys.path.append('../..')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnStand
from SimulationKit.helpers import *

from row_the_cart import update

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
            yaw_joint.setLengthRate(lr[0])
            pitch_joint.setLengthRate(lr[1])
            knee_joint.setLengthRate(lr[2])
        
            time_1 = time

except:
    yaw_joint.setLengthRate(0)
    pitch_joint.setLengthRate(0)
    knee_joint.setLengthRate(0)
    raise
