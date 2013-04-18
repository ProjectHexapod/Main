import sys
sys.path.append('..')
sys.path.append('planners')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnStand
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

d = {'offset': (0, 0, 0.67)}
s = Simulator(dt=1e-3, plane=1, pave=0, graphical=1, robot=LegOnStand, robot_kwargs=d, start_paused=False)
input_server = InputServer()  # TODO: pass along at least a password argument here
input_server.startListening()

yaw_joint = s.robot.members['hip_yaw']
pitch_joint = s.robot.members['hip_pitch']
knee_joint = s.robot.members['knee_pitch']
shock_joint = s.robot.members['foot_shock']
try:
    while True:
        s.step()
        if not s.getPaused():
            time = s.getSimTime()
            command = input_server.getLastCommand()
            lr = update(time, yaw_joint.getAngle(), pitch_joint.getAngle(), knee_joint.getAngle(), shock_joint.getPosition(), command)
            yaw_joint.setLengthRate(lr[0])
            pitch_joint.setLengthRate(lr[1])
            knee_joint.setLengthRate(lr[2])

except:
    input_server.stopListening()
    yaw_joint.setLengthRate(0)
    pitch_joint.setLengthRate(0)
    knee_joint.setLengthRate(0)
    raise
