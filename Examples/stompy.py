import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics

d = {'offset':(0,0,1.5)}
s = Simulator(dt=2e-3,plane=1,pave=0,graphical=1,ground_grade=.00,robot=SpiderWHydraulics,robot_kwargs=d)
while True:
    s.step()
    s.robot.constantSpeedWalkSmart()
