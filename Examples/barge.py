import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics, LegOnStand

d = {'offset':(0,0,3)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=1,robot=LegOnStand,robot_kwargs=d)

joints = s.robot.joints
lRates = [.01,0,0]

while True:
    s.step()
    for j,r in zip(joints, lRates):
        j.setLengthRate(r)
