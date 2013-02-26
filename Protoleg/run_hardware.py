import time
import sys
import threading
import signal

#import curses
#stdscr = curses.initscr()
#curses.noecho()
#curses.cbreak()
#stdscr.keypad(1)

sys.path.append('..')
from getch import getch
from ControlsKit.import_planner import importPlanner
from Utilities.pubsub import *
from RealWorldKit.PHBus import *

#
# Designed yaw ROM: 60
# YAW ROM:  187,  251
# Designed pitch ROM: 75
# PITCH ROM: 33.48, 107.05
# Designed knee ROM: 110
# KNEE ROM: 208.59, 317.37

def _angleWrap(ang):
    while ang > pi:
        ang -= 2*pi
    while ang < -pi:
        ang += 2*pi
    return ang

def calibrateAngles( uncalibrated_angles ):
    """
    Takes raw angles in radians from the joint encoders.
    Returns angles in radians that have been shifted to match
    our expected reference frame.
    This function is SPECIFIC TO PROTOLEG
    """
    angles = list(uncalibrated_angles)
    # Yaw offset INVERT
    angles[0] *= -1
    angles[0] += (219.0*pi/180)
    # Pitch offset 
    angles[1] -= (117.0*pi/180)
    # Knee offset INVERT
    angles[2] *= -1
    angles[2] += (288.5*pi/180)

    # Constrain
    for i in range(len(angles)):
        angles[i] = _angleWrap(angles[i])

    return angles


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
update = retval
controller = None

angles = [0,0,0]
valve_commands = [0,0,0]

if 1:
    #publisher makes data available for plotting and logging
    publisher = Publisher(5055)
    publisher.addToCatalog( 'time', time.time )
    publisher.addToCatalog( 'yaw_rad',      lambda: angles[0] )
    publisher.addToCatalog( 'pitch_rad',    lambda: angles[1] )
    publisher.addToCatalog( 'knee_rad',     lambda: angles[2] )
    publisher.addToCatalog( 'yaw_deg',      lambda:180*bus.nodes[0].getMagEncoderAngle()[0]/pi )
    publisher.addToCatalog( 'pitch_deg',    lambda:180*bus.nodes[1].getMagEncoderAngle()[0]/pi )
    publisher.addToCatalog( 'knee_deg',     lambda:180*bus.nodes[2].getMagEncoderAngle()[0]/pi )
    publisher.addToCatalog( 'yaw_cmd',      lambda: valve_commands[0] ) 
    publisher.addToCatalog( 'pitch_cmd',    lambda: valve_commands[1] ) 
    publisher.addToCatalog( 'knee_cmd',     lambda: valve_commands[2] ) 
    publisher.start()

    class rateEstimator(object):
        def __init__( self ):
            self.last_state = 0.0
            self.vel_est = LowPassFilter( gain=1.0, corner_frequency=10.0 )
        def update( new_state ):
            return self.vel_est.update((new_state-self.last_state)/global_time.getDelta())
        def getVal( self ):
            return self.vel_est.getVal()

    f_out = open('data/data_log_%d.csv'%int(time.time()), 'w+')
    for k,v in publisher.catalog.items():
        f_out.write('%s, '%k)
    f_out.write('\n')

def gracefulShutdown( signum, stack ):
    print "Watchdog fired!"
    print "Got signal %d"%signum
    print "Goodbye!"
    global run_flag
    run_flag = False
    time.sleep(.5)
    exit(0)

run_flag = True

def handleUserInput():
    global valve_commands
    # grab user input and adjust operating parameters
    while True:
        c = getch()
        if len(c) == 0:
            continue
        if c in 'q':
            valve_commands[0] += 0.05
        elif c in 'w':
            valve_commands[1] += 0.05
        elif c in 'e':
            valve_commands[2] += 0.05
        elif c in 'a':
            valve_commands[0] =-0.0
        elif c in 's':
            valve_commands[1] =-0.0
        elif c in 'd':
            valve_commands[2] =-0.0
        elif c in 'z':
            valve_commands[0] +=-0.05
        elif c in 'x':
            valve_commands[1] +=-0.05
        elif c in 'c':
            valve_commands[2] +=-0.05
        elif c in 'm':
            global run_flag
            run_flag = False
            time.sleep(.5)
            exit(0)

input_thread = threading.Thread()
input_thread.daemon = True
input_thread.run = handleUserInput
input_thread.start()

def keyboardInterruptHandler( sig, frame ):
    print 'Caught keyboard interrupt!'
    print "Goodbye!"
    global run_flag
    run_flag = False

signal.signal(signal.SIGINT, keyboardInterruptHandler)

rate_controller = threading.Event()
rate_controller.clear()

def rateController():
    while run_flag:
        time.sleep(0.005)
        rate_controller.set()

rate_controller_thread = threading.Thread()
rate_controller_thread.run = rateController
rate_controller.daemon = True
rate_controller_thread.start()

watchdog = WatchDog( 0.1, gracefulShutdown )

error_rates = [0,0,0]
run_count = 0

time_1 = 0.0
watchdog.start()
while run_flag:
    time_0 = time.time()
    rate_controller.wait()
    rate_controller.clear()
    run_count += 1

    bus.exchangeMagValveData( valve_commands )
    bus.waitForSync()
    uncalibrated_angles, flags = bus.getMagEncoderAngle()
    angles = calibrateAngles( uncalibrated_angles )
    for i in range(len(flags)):
        if flags[i]:
            print 'WARNING: Mag field unhappy on index %d: flag %d'%(i, flags[i])
            error_rates[i] += 0.01
        error_rates[i] *= 0.99
    valve_commands = update( time_0, angles[0], angles[1], angles[2], 0.0 )
    bus.exchangeMagValveData( valve_commands )
    bus.waitForSync()
    watchdog.feed()
    if not run_count%1:
        publisher.publish()
    for k,v in publisher.catalog.items():
        f_out.write('%f, '%(v()))
    f_out.write('\n')

print 'Sending valve command 0.0 to valves'
valve_commands = [0.0,0.0,0.0]
bus.exchangeMagValveData( valve_commands )
bus.waitForSync()
print "Exiting with no errors.  Goodbye."
exit(0)

