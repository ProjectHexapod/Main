import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics, LegOnStand

d = {'offset':(0,0,3)}
s = Simulator(dt=0,plane=1,pave=0,graphical=1,robot=LegOnStand,robot_kwargs=d)

joints = s.robot.joints
angles = [-0.5,1,-2]

while True:
    s.step()
    for j,ang in zip(joints, angles):
        j.setLengthRate(ang)

