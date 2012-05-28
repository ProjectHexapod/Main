import time
import sys
from leg_logger import logger
sys.path.append('../..')
from RealWorldKit.BusInterface import *

from cart_move import update
#from move_one_joint import update
#from hold_position import update
#from zero_flow_rate import update

leg1 = ControlBus(device='/dev/ttyUSB0')
yaw_valve = ValveNode(leg1, node_id=1, name="yaw", bore=0.0254, rod=0.0159, lpm=22.712, deadband=130)
pitch_valve = ValveNode(leg1, node_id=2, name="pitch", bore=0.0381, rod=0.0254, lpm=22.712, deadband=130)
knee_valve = ValveNode(leg1, node_id=3, name="knee", bore=0.0254, rod=0.0159, lpm=22.712, deadband=130)
yaw_encoder = EncoderNode(leg1, node_id=4, gain=1, offset=-90*pi/180, bias=(1200,1200))
pitch_encoder = EncoderNode(leg1, node_id=5, gain=-1, offset=40*pi/180, bias=(1200,1200))
knee_encoder = EncoderNode(leg1, node_id=6, gain=1, offset=220*pi/180, bias=(1200,1200))
shock_encoder = EncoderNode(leg1, node_id=7, gain=1, offset=0, bias=(1200,1200))

time_1 = 0.0
try:
    yaw_encoder.startProbe()
    pitch_encoder.startProbe()
    knee_encoder.startProbe()
    shock_encoder.startProbe()
    time.sleep(0.5)

    while True:
        time_0 = time.time()
        if int(time_0*500.0) != int(time_1*500.0):
	    leg1.tick()
            lr = update(time_0, yaw_encoder.getAngle(), pitch_encoder.getAngle(), knee_encoder.getAngle(), shock_encoder.getPosition())
            logger.info("Gimpy main loop", hip_yaw_rate=0.0, hip_pitch_rate=lr[1], knee_pitch_rate=lr[2],
                        hip_yaw_angle=yaw_encoder.getAngle(), hip_pitch_angle=pitch_encoder.getAngle(),
                        knee_pitch_angle=knee_encoder.getAngle(), shock_depth=shock_encoder.getPosition(),
                        time=time_0)
            yaw_valve.setLengthRate(0.0)
            pitch_valve.setLengthRate(lr[1])
            knee_valve.setLengthRate(lr[2])
	    yaw_encoder.startProbe()
	    pitch_encoder.startProbe()
	    knee_encoder.startProbe()
	    shock_encoder.startProbe()
        
            time_1 = time_0

except:
    yaw_valve.stop()
    pitch_valve.stop()
    knee_valve.stop()
    raise
