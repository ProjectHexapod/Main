import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics
import pygame.joystick as joystick
import time

if not joystick.get_init():
    joystick.init()
if joystick.get_count() != 1:
    print "Sorry, need joystick"
    exit()

stick = joystick.Joystick(0)
stick.init()
print "Joystick detected: ", stick.get_name()
print "Axes:              ", stick.get_numaxes()
print "Balls:             ", stick.get_numballs()
print "Hats:              ", stick.get_numhats()
print "Buttons:           ", stick.get_numbuttons()
stick_neutrals = []

d = {'offset':(0,0,1.5)}
s = Simulator(dt=2e-3,plane=1,pave=0,graphical=1,ground_grade=.00,robot=SpiderWHydraulics,robot_kwargs=d,\
    renderObjs=0)
last_t = 0
while True:
    s.step()
    if s.getSimTime()-last_t > .01:
        x =   -(stick.get_axis(1)+.15466)
        if x < 0:
            x *= 2
        x /= .7
        y =   -(stick.get_axis(0)+.15466)
        if y < 0:
            y *= 2
        y /= .7
        z =   -(stick.get_axis(3)-.29895)
        if z < 0:
            z *= 2
        rot = stick.get_axis(2)+.226806
        print x, y, z, rot
        s.robot.constantSpeedWalkSmart(\
            x_scale =   x,\
            y_scale =   y,\
            z_scale =   z,\
            rot_scale = rot)
        last_t = s.getSimTime()
