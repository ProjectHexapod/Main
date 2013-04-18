import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnStand
from SimulationKit.helpers import *
import time

from math import *

d = {'offset': (0, 0, 0.67)}
s = Simulator(dt=1e-3,
              plane=1,
              pave=0,
              graphical=1,
              robot=LegOnStand,
              robot_kwargs=d,
              start_paused=True)

# Put up the goal posts
wickets = []
static_geoms = []
row_n = 2
x_off = .5
y_off = .5
i = 0
# Rack up the pins
for i in range(row_n):
    for j in range(i + 1):
        body, geom = s.createCapsule(mass=1.0e1,
                                     length=1.0,
                                     radius=0.1,
                                     pos=(i * x_off, -5.0 - y_off * j + i * (y_off / 2), 0.7))
        wickets.append(body)
        static_geoms.append(geom)

robot = s.robot
yaw   = robot.members['hip_yaw']
pitch = robot.members['hip_pitch']
knee  = robot.members['knee_pitch']
shock = robot.members['foot_shock']

cycle_time = 10.0

while True:
    s.step()
    sim_t = s.getSimTime()

    x_target = robot.YAW_L + robot.THIGH_L
    y_target = 1.0 * cos(2 * pi * sim_t / cycle_time)
    z_target = max(0.2 * sin(2 * pi * sim_t / cycle_time), -0.00) - robot.HIP_FROM_GROUND_HEIGHT

    yaw_target, pitch_target, knee_target = robot.jointAnglesFromFootPosition((x_target, y_target, z_target))

    yaw.setLengthRate(-0.25 * calcAngularError(yaw.getAngle(), yaw_target))
    pitch.setLengthRate(-0.25 * calcAngularError(pitch.getAngle(), pitch_target))
    knee.setLengthRate(-0.25 * calcAngularError(knee.getAngle(), knee_target))
    #print shock.getPosition()
