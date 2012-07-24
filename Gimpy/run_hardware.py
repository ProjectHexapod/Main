import time
import sys
sys.path.append('..')
from getch import getch

from RealWorldKit import *
#from ControlsKit import logger
from ControlsKit.import_planner import importPlanner
from ControlsKit.filters import LowPassFilter
from SimulationKit.pubsub import *
import time
import threading

# Check command-line arguments to find the planner module
update, controller = importPlanner()
retval = importPlanner()
# FIXME: This is to allow backwards compatibility to older versions of importPlanner
if type(retval) == tuple:
    update, controller = retval
else:
    update = retval
    controller = None

leg1 = ControlBus(device='/dev/ttyUSB0')
yaw_valve = ValveNode(leg1       , node_id=1 , name="yaw_valve"     , bore=0.0254 , rod=0.0189        , lpm=22.712 , e_deadband=89 , r_deadband=75)
pitch_valve = ValveNode(leg1     , node_id=2 , name="pitch_valve"   , bore=0.0381 , rod=0.0254        , lpm=22.712 , e_deadband=77 , r_deadband=70)
knee_valve = ValveNode(leg1      , node_id=3 , name="knee_valve"    , bore=0.0254 , rod=0.0159        , lpm=22.712 , e_deadband=87 , r_deadband=69)
yaw_encoder = EncoderNode(leg1   , node_id=4 , name="yaw_encoder"   , gain=1      , offset=35*pi/180 , bias=(1200 , 1200))
pitch_encoder = EncoderNode(leg1 , node_id=5 , name="pitch_encoder" , gain=-1     , offset=45*pi/180 , bias=(1200 , 1200))
knee_encoder = EncoderNode(leg1  , node_id=6 , name="knee_encoder"  , gain=1      , offset=225*pi/180 , bias=(1200 , 1200))
shock_encoder = EncoderNode(leg1 , node_id=7 , name="shock_encoder" , gain=1      , offset=0          , bias=(1200 , 1200))

pitch_filt   = LowPassFilter( gain=1.0, corner_frequency=20 )
yaw_filt     = LowPassFilter( gain=1.0, corner_frequency=20 )
#yaw_cmd_filt = LowPassFilter( gain=1.0, corner_frequency=100 )

publisher = Publisher(5055)
publisher.addToCatalog( 'time', time.time )
publisher.addToCatalog( 'yaw_ang',   yaw_encoder.getAngleDeg )
publisher.addToCatalog( 'yaw_ang_filt', lambda:180*yaw_filt.getVal()/pi )
publisher.addToCatalog( 'yaw_sin',   yaw_encoder.getSinValue )
publisher.addToCatalog( 'yaw_cos',   yaw_encoder.getCosValue )
publisher.addToCatalog( 'pitch_ang', pitch_encoder.getAngleDeg )
publisher.addToCatalog( 'pitch_ang_filt', lambda:180*pitch_filt.getVal()/pi )
publisher.addToCatalog( 'pitch_sin',   pitch_encoder.getSinValue )
publisher.addToCatalog( 'pitch_cos',   pitch_encoder.getCosValue )
publisher.addToCatalog( 'knee_ang',  knee_encoder.getAngleDeg )
publisher.addToCatalog( 'knee_sin',   knee_encoder.getSinValue )
publisher.addToCatalog( 'knee_cos',   knee_encoder.getCosValue )
publisher.addToCatalog( 'yaw_cmd_ret', yaw_valve.getPWM0 )
publisher.addToCatalog( 'yaw_cmd_ex', yaw_valve.getPWM1 )
publisher.addToCatalog( 'pitch_cmd_ret', pitch_valve.getPWM0 )
publisher.addToCatalog( 'pitch_cmd_ex', pitch_valve.getPWM1 )
publisher.addToCatalog( 'knee_cmd_ret', knee_valve.getPWM0 )
publisher.addToCatalog( 'knee_cmd_ex', knee_valve.getPWM1 )
if controller != None:
    publisher.addToCatalog( 'yaw_ang_target',   controller.getDesiredYawDeg )
    publisher.addToCatalog( 'yaw_vel_est',   controller.pid_controllers[0].d_lowpass.getVal )
    publisher.addToCatalog( 'pitch_ang_target',   controller.getDesiredPitchDeg )
    publisher.addToCatalog( 'knee_ang_target',   controller.getDesiredKneeDeg )
publisher.start()

class rateEstimator(object):
    def __init__( self ):
        self.last_state = 0.0
        self.vel_est = LowPassFilter( gain=1.0, corner_frequency=10.0 )
    def update( new_state ):
        return self.vel_est.update((new_state-self.last_state)/global_time.getDelta())
    def getVal( self ):
        return self.vel_est.getVal()

f_out = open('data_log_%f.csv'%time.time(), 'w+')
for k,v in publisher.catalog.items():
    f_out.write('%s, '%k)
f_out.write('\n')

run_flag = True

def handleUserInput():
    global controller, yaw_cmd, pitch_cmd, knee_cmd, run_flag
    # grab user input and adjust operating parameters
    while True:
        input_str = getch()
        """
        for c in input_str:
            if c in 'x':
                exit()
            elif c in 'm':
                manual_mode = True
                print "MANUAL MODE SET"
            elif c in 'q':
                #yaw extend
                yaw_cmd += 0.01
                print 'YAW: ', yaw_cmd
            elif c in 'a':
                yaw_cmd -= 0.01
                print 'YAW: ', yaw_cmd
            elif c in 'w':
                #pitch extend
                pitch_cmd += 0.01
                print 'PITCH: ', pitch_cmd
            elif c in 's':
                pitch_cmd -= 0.01
                print 'PITCH: ', pitch_cmd
            elif c in 'e':
                #knee extend
                knee_cmd += 0.01
                print 'KNEE: ', knee_cmd
            elif c in 'd':
                knee_cmd -= 0.01
                print 'KNEE: ', knee_cmd
                """
        for c in input_str:
            if c in 'x':
                run_flag = False
                exit()
            elif c in 'm':
                manual_mode = True
                print "MANUAL MODE SET"
            elif c in 'q':
                controller.pid_controllers[0].kp += 0.05
                print 'P: ', controller.pid_controllers[0].kp
            elif c in 'a':
                controller.pid_controllers[0].kp -= 0.05
                print 'P: ', controller.pid_controllers[0].kp
            elif c in 'w':
                controller.pid_controllers[0].ki += 0.05
                print 'I: ', controller.pid_controllers[0].ki
            elif c in 's':
                controller.pid_controllers[0].ki -= 0.05
                print 'I: ', controller.pid_controllers[0].ki
            elif c in 'e':
                controller.pid_controllers[0].kd += 0.01
                print 'D: ', controller.pid_controllers[0].kd
            elif c in 'd':
                controller.pid_controllers[0].kd -= 0.01
                print 'D: ', controller.pid_controllers[0].kd
            elif c in 'r':
                controller.pid_controllers[0].kff += 0.01
                print 'F: ', controller.pid_controllers[0].kff
            elif c in 'f':
                controller.pid_controllers[0].kff -= 0.01
                print 'F: ', controller.pid_controllers[0].kff
            elif c in 't':
                controller.pid_controllers[0].kfa += 0.01
                print 'A: ', controller.pid_controllers[0].kfa
            elif c in 'g':
                controller.pid_controllers[0].kfa -= 0.01
                print 'A: ', controller.pid_controllers[0].kfa

input_thread = threading.Thread()
input_thread.run = handleUserInput
input_thread.start()

time_1 = 0.0
try:
    # XXX Make sure we've got angle samples to start.  Should be done better.
    yaw_encoder.startProbe()
    pitch_encoder.startProbe()
    knee_encoder.startProbe()
    shock_encoder.startProbe()
    time.sleep(0.5)
    manual_mode = False
    yaw_cmd = 0.0
    pitch_cmd = 0.0
    knee_cmd = 0.0

    while run_flag:
        time_0 = time.time()
        if int(time_0*200.0) != int(time_1*200.0):
            leg1.tick()
            a = pitch_encoder.getAngle()
            pitch_filt.update(a)
            a = yaw_encoder.getAngle()
            yaw_filt.update(a)
            lr = update(time_0, yaw_filt.getVal(), pitch_filt.getVal(), knee_encoder.getAngle(), shock_encoder.getPosition())
            if not manual_mode:
                #if abs(lr[0])>1 or abs(lr[1])>1 or abs(lr[2])>1:
                #    yaw_valve.setPWM(lr[0])
                #    pitch_valve.setPWM(lr[1])
                #    knee_valve.setPWM(lr[2])
                #else:
                    #yaw_cmd_filt.update( lr[0] )
                    #yaw_valve.setLengthRate(yaw_cmd_filt.getVal())
                    #print "%.3f, %.3f"%(lr[0], yaw_cmd_filt.getVal())
                yaw_valve.setLengthRate(lr[0])
                #error = controller.getDesiredYaw()-yaw_filt.getVal()
                #print 'Error: %.2f'%(error)
                #print '%.2f, %d ,%d'%(lr[0], yaw_valve.pwm0, yaw_valve.pwm1)
                #def sign(x):
                #    return x/abs(x)
                #print ''
                pitch_valve.setLengthRate(lr[1])
                knee_valve.setLengthRate(lr[2])
            else:
                yaw_valve.setLengthRate(   yaw_cmd  )
                pitch_valve.setLengthRate( pitch_cmd)
                knee_valve.setLengthRate(  knee_cmd )
            yaw_encoder.startProbe()
            pitch_encoder.startProbe()
            knee_encoder.startProbe()
            shock_encoder.startProbe()
        
            time_1 = time_0
            publisher.publish()
            for k,v in publisher.catalog.items():
                f_out.write('%f, '%(v()))
            f_out.write('\n')

except:
    pass
yaw_valve.stop()
pitch_valve.stop()
knee_valve.stop()
f_out.close()
