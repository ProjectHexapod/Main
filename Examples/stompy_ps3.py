import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics
from ControlsKit.filters import LowPassFilter
from ControlsKit.time_sources import global_time
from UI import InputServer
import time

input_server = InputServer()
input_server.startListening()

d = {'offset':(0,0,1.5)}
s = Simulator(dt=2e-3, plane=1, pave=0, graphical=1, ground_grade=0., robot=SpiderWHydraulics, robot_kwargs=d, render_objs=1, draw_contacts=0)
last_t = 0


try:
    while True:
        s.step()
        global_time.updateTime(s.getSimTime())
        if s.getSimTime()-last_t > .001:
            cmd = input_server.getLastCommand()
            if not cmd:
                time.sleep(.5)
                continue
            x = cmd[18] - 128
            y = cmd[17] - 128
            z = cmd[20] - 128
            rot = cmd[19] - 128
            print x, y, z, rot
            s.robot.constantSpeedWalkSmart(\
                x_scale =   x,\
                y_scale =   y,\
                z_scale =   z,\
                rot_scale = rot)
            last_t = s.getSimTime()
finally:
    input_server.stopListening()
