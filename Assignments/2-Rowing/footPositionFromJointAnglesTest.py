from footPositionFromJointAngles import *
from transformations import *

import sys

sys.path.append('../..')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnStand

d = {'offset':(0,0,.63)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=1,robot=LegOnStand,robot_kwargs=d, start_paused = True)

yaw   = s.robot.members['hip_yaw']
pitch = s.robot.members['hip_pitch']
knee  = s.robot.members['knee_pitch']
foot_shock = s.robot.members['foot_shock']

while True:
    s.step()
    if not s.paused:
        print footPositionFromJointAngles(yaw.getAngle(),
                                          pitch.getAngle(),
                                          knee.getAngle(),
                                          foot_shock.getPosition(),
                                          s.robot)