import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnColumn

d = {'offset':(0,0,1.5)}
s = Simulator(dt=2e-3,plane=1,graphical=1,ground_grade=.00,robot=LegOnColumn,robot_kwargs=d,\
    render_objs=1, draw_COM=0, draw_support=0, draw_contacts=0)
while True:
    s.step()
