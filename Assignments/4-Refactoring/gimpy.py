import time
import sys
from leg_logger import logger
sys.path.append('../..')
from RealWorldKit import *

from cart_move import update
#from move_one_joint import update
#from hold_position import update
#from zero_flow_rate import update

leg1 = ControlBus(device='/dev/ttyUSB0')
yaw_valve = ValveNode(leg1, node_id=1, name="yaw_valve", bore=0.0254, rod=0.0159, lpm=22.712, deadband=130)
pitch_valve = ValveNode(leg1, node_id=2, name="pitch_valve", bore=0.0381, rod=0.0254, lpm=22.712, deadband=130)
knee_valve = ValveNode(leg1, node_id=3, name="knee_valve", bore=0.0254, rod=0.0159, lpm=22.712, deadband=130)
yaw_encoder = EncoderNode(leg1, node_id=4, name="yaw_encoder", gain=1, offset=-90*pi/180, bias=(1200,1200))
pitch_encoder = EncoderNode(leg1, node_id=5, name="pitch_encoder", gain=-1, offset=40*pi/180, bias=(1200,1200))
knee_encoder = EncoderNode(leg1, node_id=6, name="knee_encoder", gain=1, offset=220*pi/180, bias=(1200,1200))
shock_encoder = EncoderNode(leg1, node_id=7, name="shock_encoder", gain=1, offset=0, bias=(1200,1200))

time_1 = 0.0
try:
    # XXX Make sure we've got angle samples to start.  Should be done better.
    yaw_encoder.startProbe()
    pitch_encoder.startProbe()
    knee_encoder.startProbe()
    shock_encoder.startProbe()
    time.sleep(0.5)

    while True:
        time_0 = time.time()
	# XXX Find a cleaner way to run at 500Hz.
        if int(time_0*500.0) != int(time_1*500.0):
	    leg1.tick()
            lr = update(time_0, yaw_encoder.getAngle(), pitch_encoder.getAngle(), knee_encoder.getAngle(), shock_encoder.getPosition())
            logger.info("Gimpy main loop", hip_yaw_rate=0.0, hip_pitch_rate=lr[1], knee_pitch_rate=lr[2],
                        hip_yaw_angle=yaw_encoder.getAngle(), hip_pitch_angle=pitch_encoder.getAngle(),
                        knee_pitch_angle=knee_encoder.getAngle(), shock_depth=shock_encoder.getPosition(),
                        time=time_0)
	    # XXX Yaw encoder is currently non-functional.
	    lr[0] = 0.0
            yaw_valve.setLengthRate(lr[0])
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
