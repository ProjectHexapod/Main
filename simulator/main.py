import sys
sys.path.append('../inc')
from RobotSimulator import Simulator
from Robots import SpiderWHydraulics
from Robots import LegOnStand

d = {'offset':(0,0,3)}
#s = Simulator(dt=0,plane=0,pave=1,graphical=1,robot=SpiderWHydraulics,robot_kwargs=d)
s = Simulator(dt=0,plane=1,pave=0,graphical=1,robot=LegOnStand,robot_kwargs=d)
while True:
    s.step()
    #s.robot.constantSpeedWalk(s.sim_t)
