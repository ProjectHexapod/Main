import sys

sys.path.append('../inc')

import time
from pubsub import *
from matplotlib import pyplot

subscriptions = ['time']

def receiveFrame( f ):
    for k,v in f.items():
       data[k].pop(0)
       data[k].append(f[k])

s = Subscriber( 'localhost', 5055 )

n_plots = 1
plot_vars = [[]]
subplot = 0

while 1:
    print 'Options:'
    print '1. Add subscription'
    print '2. Select subplot'
    print '3. Start plotting'
    c = int(input('Choice:'))
    if c == 1:
        for i in range(len(s.catalog)):
            print '%.2u: %s'%(i,s.catalog[i])
        i = int(input('Choice:'))
        if i >= 0 and i < len(s.catalog):
            while subplot >= n_plots:
                plot_vars.append([])
                n_plots+=1
            subscriptions.append(s.catalog[i])
            plot_vars[subplot].append(s.catalog[i])
            print subscriptions
    elif c == 2:
        subplot = int(input('Select subplot:'))
    elif c == 3:
        break

pyplot.ion()
data = { k:[0 for x in range(1000)] for k in subscriptions }
s.setCallback( receiveFrame )
s.subscribeTo( subscriptions )
s.start()

colors = ['b', 'g', 'r', 'c', 'k']

while 1:
    #pyplot.clf()
    for i in range(n_plots):
        pyplot.subplot(n_plots,1,i)
        pyplot.cla()
        label = ''
        for j in range(len(plot_vars[i])):
            k = plot_vars[i][j]
            pyplot.plot( data['time'], data[k], colors[j])
            label += k + '\n'
        axes = list(pyplot.axis())
        axes[0] = data['time'][0]
        axes[1] = data['time'][-1]
        pyplot.axis(axes)
        pyplot.ylabel(label)
    pyplot.draw()
    time.sleep(0.1)
s.close()
