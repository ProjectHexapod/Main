import sys
sys.path.append('../..')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnStand
from SimulationKit.helpers import *

from row_the_cart import update

d = {'offset':(0,0,0.67)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=1,robot=LegOnStand,robot_kwargs=d, start_paused = True)

# Put up the goal posts
wickets = []
static_geoms = []
row_n = 6
x_off = .5
y_off = .5
i = 0
# Rack up the pins
for i in range(row_n):
    for j in range(i+1):
        body, geom = s.createCapsule( mass = 1.0e1, length = 1.0, radius = 0.1, pos = (i*x_off, -5.0 - y_off*j + i*(y_off/2),0.7) )
        wickets.append(body)
        static_geoms.append(geom)

yaw_joint = s.robot.members['hip_yaw']
pitch_joint = s.robot.members['hip_pitch']
knee_joint = s.robot.members['knee_pitch']
shock_joint = s.robot.members['foot_shock']

time_1 = 0.0
while True:
    s.step()

    time = s.getSimTime()
    if time != time_1:
        lr = update(time, yaw_joint.getAngle(), pitch_joint.getAngle(), knee_joint.getAngle(), shock_joint.getPosition())
        yaw_joint.setLengthRate(lr[0])
        pitch_joint.setLengthRate(lr[1])
        knee_joint.setLengthRate(lr[2])
        
        time_1 = time