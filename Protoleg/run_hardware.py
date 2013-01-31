import time
import sys
import threading

sys.path.append('..')
from getch import getch
from ControlsKit.import_planner import importPlanner
from ControlsKit.filters import LowPassFilter
from SimulationKit.pubsub import *
from RealWorldKit import *

# Check command-line arguments to find the planner module
retval = importPlanner()
# FIXME: This is to allow backwards compatibility to older versions of importPlanner
if type(retval) == tuple:
    update, controller = retval
else:
    update = retval
    controller = None

# publisher makes data available for plotting and logging
publisher = Publisher(5055)
publisher.addToCatalog( 'time', time.time )
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

time_1 = 0.0
try:
    while run_flag:
        time_0 = time.time()
        if int(time_0*200.0) != int(time_1*200.0):
            time_1 = time_0
            publisher.publish()
            for k,v in publisher.catalog.items():
                f_out.write('%f, '%(v()))
            f_out.write('\n')
except:
    pass
