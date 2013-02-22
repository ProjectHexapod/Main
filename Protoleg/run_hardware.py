import time
import sys
import threading

sys.path.append('..')
from getch import getch
from ControlsKit.import_planner import importPlanner
#from ControlsKit.filters import LowPassFilter
from Utilities.pubsub import *
from RealWorldKit.PHBus import *

# This is our list of MAC addresses, in order:
# [ yaw, pitch, knee ]
mac_list = []
mac_list.append( "\x00\xCF\x52\x35\x00\x07" );
mac_list.append( "\x00\xCF\x52\x35\x00\x08" );
mac_list.append( "\x00\xCF\x52\x35\x00\x09" );

# Open a connection to the leg
bus = BusManager( 'eth0', mac_list )

# Check command-line arguments to find the planner module
retval = importPlanner()
# FIXME: This is to allow backwards compatibility to older versions of importPlanner
if type(retval) == tuple:
    update, controller = retval
else:
    update = retval
    controller = None

if 1:
    #publisher makes data available for plotting and logging
    publisher = Publisher(5055)
    publisher.addToCatalog( 'time', time.time )
    publisher.addToCatalog( 'yaw_deg',      lambda:180*bus.nodes[0].getMagEncoderAngle()[0]/pi )
    publisher.addToCatalog( 'pitch_deg',    lambda:180*bus.nodes[1].getMagEncoderAngle()[0]/pi )
    publisher.addToCatalog( 'knee_deg',     lambda:180*bus.nodes[2].getMagEncoderAngle()[0]/pi )
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

def gracefulShutdown( signum, stack ):
    print "Watchdog fired!"
    print "Got signal %d"%signum
    print "Goodbye!"
    exit(0)

watchdog = WatchDog( 0.1, gracefulShutdown )

run_flag = True

valve_commands = [0,0,0]

error_rates = [0,0,0]
run_count = 0

time_1 = 0.0
watchdog.start()
while run_flag:
    time_0 = time.time()
    if int(time_0*200.0) != int(time_1*200.0):
        run_count += 1
        time_1 = time_0

        bus.exchangeMagValveData( valve_commands )
        bus.waitForSync()
        angles, flags = bus.getMagEncoderAngle()
        for i in range(len(flags)):
            if flags[i]:
                print 'WARNING: Mag field unhappy on index %d: flag %d'%(i, flags[i])
                error_rates[i] += 0.01
            error_rates[i] *= 0.99
        if run_count % 100 == 0:
            print "FRAME:"
            print '%3.2f %3.2f %3.2f' % ((180/pi)*angles[0], (180/pi)*angles[1], (180/pi)*angles[2])
            print '%4.d %4.d %4.d' % (angles[0]*4096/(2*pi), angles[1]*4096/(2*pi), angles[2]*4096/(2*pi))
            print '%3.2f %3.2f %3.2f' % (error_rates[0], error_rates[1], error_rates[2])
            #print error_rates
        valve_commands = update( time_0, angles[0], angles[1], angles[2], 0.0 )
        bus.exchangeMagValveData( valve_commands )
        bus.waitForSync()
        watchdog.feed()
        publisher.publish()
        #for k,v in publisher.catalog.items():
        #    f_out.write('%f, '%(v()))
        #f_out.write('\n')
