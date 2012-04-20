import sys
sys.path.append('..')
import random
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnStand
import time

import StudentControl

d = {'offset':(0,0,1.1)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=1,robot=LegOnStand,robot_kwargs=d, start_paused = True)

# Put up the goal posts
wickets = []
row_n = 6
x_off = .5
y_off = .5
i = 0

# Rack up the pins
for i in range(row_n):
    for j in range(i+1):
        body, geom = s.createCapsule( mass = 1.0e1, length = 1.0, radius = 0.1, pos = (5.0+i*x_off, y_off*j - i*(y_off/2),0.7) )
        wickets.append(body)

# Place the ball
ball,g = s.createSphere( mass=1.0e2, radius=0.25, pos=(1.75,random.uniform(-.05,.05),.25))

# Declare the victory condition
def checkVictory():
    points = 0
    for body in wickets:
        if body.getRotation() != (1.0, 0.0, 0.0,\
                                  0.0, 1.0, 0.0,\
                                  0.0, 0.0, 1.0):
            points += 1
    return points

end_t = 0

p = ball.getPosition()
print 'Ball starting at: (%.2f,%.2f,%.2f)'%(p[0],p[1],p[2])

# The three joints are:
# [ hip yaw, hip pitch, knee pitch ]
joints = s.robot.joints

while True:
    s.step()
    points = checkVictory()
    if points:
        if end_t == 0.0:
            # Now that we've won, set a time to end the simulation
            end_t = s.getSimTime() + 5.0
            print 'Victory detected! Counting down to exit...'
        elif s.getSimTime() > end_t:
            print "You won with %d points!"%points
            break
    lRates = StudentControl.control( sim_time = s.getSimTime(), hip_yaw_angle=joints[0].getAngle()+s.robot.YAW_OFFSET, hip_pitch_angle=joints[1].getAngle()+s.robot.PITCH_OFFSET, knee_angle=joints[2].getAngle()+s.robot.KNEE_OFFSET )
    for j,r in zip(joints, lRates):
        j.setLengthRate(r)
