import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics

d = {'offset':(0,0,3.5)}
s = Simulator(dt=2e-3,plane=0,graphical=1,ground_grade=.00,robot=SpiderWHydraulics,robot_kwargs=d,\
    render_objs=0, draw_COM=0, draw_support=0, draw_contacts=1,\
    height_map="heightmap.jpg", terrain_scales=(1,1,3))
while True:
    s.step()
    s.robot.constantSpeedWalkSmart()
