import time
import sys
sys.path.append('..')

from RealWorldKit import *
from ControlsKit import logger
from ControlsKit.import_planner import importPlanner
from SimulationKit.pubsub import *

# Check command-line arguments to find the planner module
update, controller = importPlanner()

deadband = 75

leg1 = ControlBus(device='/dev/ttyUSB0')
yaw_valve = ValveNode(leg1       , node_id=1 , name="yaw_valve"     , bore=0.0254 , rod=0.0159        , lpm=22.712 , e_deadband=deadband+10 , r_deadband=deadband)
pitch_valve = ValveNode(leg1     , node_id=2 , name="pitch_valve"   , bore=0.0381 , rod=0.0254        , lpm=22.712 , e_deadband=deadband+05 , r_deadband=deadband)
knee_valve = ValveNode(leg1      , node_id=3 , name="knee_valve"    , bore=0.0254 , rod=0.0159        , lpm=22.712 , e_deadband=deadband , r_deadband=deadband-5)
yaw_encoder = EncoderNode(leg1   , node_id=4 , name="yaw_encoder"   , gain=1      , offset=30*pi/180 , bias=(1200 , 1200))
pitch_encoder = EncoderNode(leg1 , node_id=5 , name="pitch_encoder" , gain=1     , offset=-135*pi/180  , bias=(1200 , 1200))
knee_encoder = EncoderNode(leg1  , node_id=6 , name="knee_encoder"  , gain=1      , offset=220*pi/180 , bias=(1200 , 1200))
shock_encoder = EncoderNode(leg1 , node_id=7 , name="shock_encoder" , gain=1      , offset=0          , bias=(1200 , 1200))

print "YAW: e=%f, r=%f" % (yaw_valve.max_extend_rate, yaw_valve.max_retract_rate)
print "HP: e=%f, r=%f" % (pitch_valve.max_extend_rate, pitch_valve.max_retract_rate)
print "KP: e=%f, r=%f" % (knee_valve.max_extend_rate, knee_valve.max_retract_rate)

publisher = Publisher(5055)

publisher.addToCatalog( 'time', time.time )
publisher.addToCatalog( 'yaw_ang',   yaw_encoder.getAngleDeg )
publisher.addToCatalog( 'yaw_ang_target',   controller.getDesiredYawDeg )
publisher.addToCatalog( 'pitch_ang', pitch_encoder.getAngleDeg )
publisher.addToCatalog( 'pitch_ang_target',   controller.getDesiredPitchDeg )
publisher.addToCatalog( 'knee_ang',  knee_encoder.getAngleDeg )
publisher.addToCatalog( 'knee_ang_target',   controller.getDesiredKneeDeg )
publisher.addToCatalog( 'yaw_cmd_ret', yaw_valve.getPWM0 )
publisher.addToCatalog( 'yaw_cmd_ex', yaw_valve.getPWM1 )
publisher.addToCatalog( 'pitch_cmd_ret', pitch_valve.getPWM0 )
publisher.addToCatalog( 'pitch_cmd_ex', pitch_valve.getPWM1 )
publisher.addToCatalog( 'knee_cmd_ret', knee_valve.getPWM0 )
publisher.addToCatalog( 'knee_cmd_ex', knee_valve.getPWM1 )

publisher.start()

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
        if int(time_0*50.0) != int(time_1*50.0):
            leg1.tick()
            lr = update(time_0, yaw_encoder.getAngle(), pitch_encoder.getAngle(), knee_encoder.getAngle(), shock_encoder.getPosition())
            logger.info("Gimpy main loop", hip_yaw_rate=0.0, hip_pitch_rate=lr[1], knee_pitch_rate=lr[2],
                        hip_yaw_angle=yaw_encoder.getAngle(), hip_pitch_angle=pitch_encoder.getAngle(),
                        knee_pitch_angle=knee_encoder.getAngle(), shock_depth=shock_encoder.getPosition(),
                        time=time_0)
            yaw_valve.setLengthRate(lr[0])
            pitch_valve.setLengthRate(lr[1])
            knee_valve.setLengthRate(lr[2])
            yaw_encoder.startProbe()
            pitch_encoder.startProbe()
            knee_encoder.startProbe()
            shock_encoder.startProbe()
        
            time_1 = time_0
            publisher.publish()

except:
    logger.error("Main loop exception")
    yaw_valve.stop()
    pitch_valve.stop()
    knee_valve.stop()
    raise
