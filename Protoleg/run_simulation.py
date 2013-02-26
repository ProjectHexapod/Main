import sys
sys.path.append('..')
sys.path.append('planners')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnColumn
from SimulationKit.helpers import *
from ControlsKit.import_planner import importPlanner
from UI import InputServer


# Check command-line arguments to find the planner module
retval = importPlanner()
# FIXME: This is to allow backwards compatibility to older versions of importPlanner
if type(retval) == tuple:
    update, controller = retval
else:
    update = retval
    controller = None

d = {'offset':(0,0,1.67)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=1,robot=LegOnColumn,robot_kwargs=d, start_paused = True, render_objs=1, draw_contacts=1)

yaw_joint   = s.robot.joints['hip_yaw']
pitch_joint = s.robot.joints['hip_pitch']
knee_joint  = s.robot.joints['knee_pitch']
shock_joint = s.robot.joints['foot_shock']

try:
    while True:
        s.step()
        if not s.getPaused():
            time = s.getSimTime()
            lr = update(time, yaw_joint.getAngle(), pitch_joint.getAngle(), knee_joint.getAngle(), shock_joint.getPosition())
            yaw_joint.setLengthRate(lr[0])
            pitch_joint.setLengthRate(lr[1])
            knee_joint.setLengthRate(lr[2])

except:
    yaw_joint.setLengthRate(0)
    pitch_joint.setLengthRate(0)
    knee_joint.setLengthRate(0)
    raise
