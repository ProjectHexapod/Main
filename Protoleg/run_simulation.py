import sys
sys.path.append('..')
sys.path.append('planners')
from SimulationKit import Simulator
from SimulationKit.Robots import LegOnColumn
from SimulationKit.helpers import *
from ControlsKit.import_planner import importPlanner
from Utilities.pubsub import Publisher

def keyboardInterruptHandler( sig, frame ):
    print 'Caught keyboard interrupt!'
    print "Goodbye!"
    exit(0)

import signal
signal.signal(signal.SIGINT, keyboardInterruptHandler)

# Check command-line arguments to find the planner module
retval = importPlanner()
# FIXME: This is to allow backwards compatibility to older versions of importPlanner
if type(retval) == tuple:
    if len(retval)==3:
        update, controller, graceful_exit = retval
    elif len(retval)==2:
        update, controller = retval
else:
    update = retval
    controller = None

commands = [0,0,0]

publisher = Publisher(5055)
if controller != None:
    publisher.addToCatalog( 'yaw_ang_target'   , controller.getDesiredYawDeg )
    publisher.addToCatalog( 'pitch_ang_target' , controller.getDesiredPitchDeg )
    publisher.addToCatalog( 'knee_ang_target'  , controller.getDesiredKneeDeg )
publisher.addToCatalog( 'yaw_cmd'          , lambda: commands[0] )
publisher.addToCatalog( 'pitch_cmd'        , lambda: commands[1] )
publisher.addToCatalog( 'knee_cmd'         , lambda: commands[2] )

d = {'offset':(0,0,2.00)}
s = Simulator(dt=5e-3,plane=1,pave=0,graphical=1,robot=LegOnColumn,robot_kwargs=d, start_paused = 1, render_objs=1, draw_contacts=1, publish_int=20)

yaw_joint      = s.robot.joints['hip_yaw']
pitch_joint    = s.robot.joints['hip_pitch']
knee_joint     = s.robot.joints['knee_pitch']
yaw_joint_bl   = s.robot.joints['hip_yaw_bl']
pitch_joint_bl = s.robot.joints['hip_pitch_bl']
knee_joint_bl  = s.robot.joints['knee_pitch_bl']
shock_joint    = s.robot.joints['foot_shock']

control_period = 5e-3
last_time = 0.0

while True:
    s.step()
    time = s.getSimTime()
    if not s.getPaused() and time - last_time >= control_period:
        valve_cmd = update(time,\
                yaw_joint.getAngle()+yaw_joint_bl.getAngle(),\
                pitch_joint.getAngle()+pitch_joint_bl.getAngle(),\
                knee_joint.getAngle()+knee_joint_bl.getAngle(),\
                shock_joint.getPosition())
        last_time = time
        commands[0] = valve_cmd[0]
        commands[1] = valve_cmd[1]
        commands[2] = valve_cmd[2]
        yaw_joint.setValveCommand(valve_cmd[0])
        pitch_joint.setValveCommand(valve_cmd[1])
        knee_joint.setValveCommand(valve_cmd[2])
