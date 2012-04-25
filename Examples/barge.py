import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics, LegOnStand
from SimulationKit.helpers import *
import time

from math import *

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

yaw   = s.robot.members['hip_yaw']
pitch = s.robot.members['hip_pitch']
knee  = s.robot.members['knee_pitch']

while True:
    s.step()
    sim_t = s.getSimTime()
    yaw_target   = (pi/6)*cos(2*pi*sim_t/5.0)
    pitch_target = (pi/6)*sin(2*pi*sim_t/5.0)-(pi/6)
    knee_target  = pi/2
    yaw.setLengthRate(   -0.15*calcAngularError(yaw.getAngle(), yaw_target) )
    pitch.setLengthRate( -0.15*calcAngularError(pitch.getAngle(), pitch_target) )
    knee.setLengthRate(  -0.15*calcAngularError(knee.getAngle(), knee_target) )
    #print pitch.getLength()
    #print pitch.getAngle()
    #knee.setLengthRate(  -0.01 )
    #if sim_t < 1:
    #    s.robot.members['hip_pitch'].setLengthRate(0.1)
    #    s.robot.members['hip_yaw'].setLengthRate(0.1)
    #else:
    #    s.robot.members['hip_yaw'].setLengthRate(0.05*sin((2*pi)*sim_t/(4.0)))
    #    s.robot.members['hip_pitch'].setLengthRate(0.01+0.05*cos((2*pi)*sim_t/(4.0)))
    #    s.robot.members['knee_pitch'].setLengthRate(0.00)
