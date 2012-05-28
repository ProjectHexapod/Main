import time
import sys
sys.path.append('../..')
from RealWorldKit.BusInterface import *

from row_the_cart import update

leg1 = ControlBus(device='/dev/ttyUSB0')
yaw_valve = ValveNode(leg1, 1, bore=0.0254, rod=0.0159, lpm=22.712)
pitch_valve = ValveNode(leg1, 2, bore=0.0381, rod=0.0254, lpm=22.712)
knee_valve = ValveNode(leg1, 3, bore=0.0254, rod=0.0159, lpm=22.712)
yaw_encoder = EncoderNode(leg1, 4, gain=1, offset=-90*pi/180, bias=(1200,1200))
pitch_encoder = EncoderNode(leg1, 5, gain=-1, offset=40*pi/180, bias=(1200,1200))
knee_encoder = EncoderNode(leg1, 6, gain=1, offset=220*pi/180, bias=(1200,1200))
shock_encoder = EncoderNode(leg1, 7, gain=1, offset=0, bias=(1200,1200))

time_1 = 0.0
try:
    while True:
        time_0 = time.time()
        if int(time_0*500.0) != int(time_1*500.0):
	    leg1.tick()
            lr = update(time_0, yaw_encoder.getAngle(), pitch_encoder.getAngle(), knee_encoder.getAngle(), shock_encoder.getPosition())
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
