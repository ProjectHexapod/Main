import sys
sys.path.append('..')
from SimulationKit import Simulator
from SimulationKit.Robots import SpiderWHydraulics
from SimulationKit.helpers import *
#from ControlsKit import logger
from ControlsKit.import_planner import importPlanner


# Check command-line arguments to find the planner module
update = importPlanner()


d = {'offset':(0,0,2.5)}
s = Simulator(dt=1e-3,plane=1,pave=0,graphical=1,robot=SpiderWHydraulics,robot_kwargs=d, start_paused = True)

try:
    while True:
        s.step()
        if not s.getPaused():
            time = s.getSimTime()+.0001 # FIXME: first time time_delta is called, it returns zero, which means pid commands infinity
            # FIXME: Known bug, getAcceleration returns (0,0,0)
            lr = update(time,\
                s.robot.getEncoderAngleMatrix(),\
                s.robot.getOrientation(),\
                s.robot.getAcceleration(),\
                s.robot.getAngularRates())
            s.robot.setLenRateMatrix( lr )
            #s.robot.constantSpeedWalk()
            #logger.info("Main loop iteration", time=time, hip_yaw_rate=lr[0], hip_pitch_rate=lr[1], knee_pitch_rate=lr[2], hip_yaw_angle=yaw_joint.getAngle(), hip_pitch_angle=pitch_joint.getAngle(), knee_pitch_angle=knee_joint.getAngle(), shock_depth=shock_joint.getPosition())

except:
    #logger.error("Main loop exception!")
    raise
