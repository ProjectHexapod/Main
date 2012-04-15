import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics, LegOnStand
import time

d = {'offset':(0,0,3)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=0,robot=LegOnStand,robot_kwargs=d, start_paused = False)

joints = s.robot.joints
lRates = [.01,0,0]

while True:
    s.step()
    for j,r in zip(joints, lRates):
        j.setLengthRate(r)
