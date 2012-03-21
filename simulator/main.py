import sys
sys.path.append('../inc')
from RobotSimulator import Simulator
from SpiderWHydraulicsOptimized import SpiderWHydraulics

d = {'offset':(0,0,3)}
s = Simulator(dt=0,plane=0,pave=1,graphical=1,robot=SpiderWHydraulics,robot_kwargs=d)
while True:
    s.step()
    s.robot.constantSpeedWalk(s.sim_t)
