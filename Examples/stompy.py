import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics

d = {'offset':(0,0,3)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=1,robot=SpiderWHydraulics,robot_kwargs=d)
#s = Simulator(dt=0,plane=1,pave=1,graphical=1,robot=LegOnStand,robot_kwargs=d)
while True:
    s.step()
    s.robot.constantSpeedWalk()
