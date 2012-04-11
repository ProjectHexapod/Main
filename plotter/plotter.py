import sys

sys.path.append('..')

import time
import pickle
from SimulationKit.pubsub import *

import wx

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation


data = {}
colors = ['r', 'g', 'b', 'c', 'k']

class Scope:
    def __init__( self, ax, xsubs=None, ysubs=None ):
        global colors
        self.ax = ax
        self.ax.grid()
        if xsubs==None:
            self.xsubs=[]
        else:
            self.xsubs=xsubs
        if ysubs==None:
            self.ysubs=[]
        else:
            self.ysubs=ysubs
        assert len(self.xsubs) == len(self.ysubs)
        label = ''
        for y in self.ysubs:
            label += y + ', '
        label = label[0:-2]
        print label
        self.ax.set_title(label)

    def update( self ):
        global data
        self.ax.cla()
        for i in range(len(self.xsubs)):
            self.ax.plot(\
                data[self.xsubs[i]],\
                data[self.ysubs[i]],\
                colors[i])
        label = ''
        for y in self.ysubs:
            label += y + ', '
        label = label[0:-2]
        self.ax.set_title(label)
        self.ax.grid(b=True)
        self.ax.autoscale(tight=True)
        return []

subscriptions = ['time']
n_plots = 1
plot_vars = [[]]

try:
    f = open('plot_settings.dump', 'r')
    l = pickle.load(f)
    subscriptions = l[0]
    n_plots = l[1]
    plot_vars = l[2]
    f.close()
    print 'Load successful'
except:
    'Failed to load settings... starting with defaults'

def receiveFrame( f ):
    for k,v in f.items():
       data[k].pop(0)
       data[k].append(f[k])

s = Subscriber( 'localhost', 5055 )
subplot = 0

print 'Present subscriptions:'
for sub in subscriptions:
    print sub

while 1:
    print 'Options:'
    print '1. Add subscription'
    print '2. Select subplot'
    print '3. Clear subscriptions'
    print '4. Start plotting'
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
        subscriptions = ['time']
        n_plots = 1
        plot_vars = [[]]
        subplot = 0
        print 'Cleared'
    elif c == 4:
        break

data = { k:[0 for x in range(1000)] for k in subscriptions }
s.setCallback( receiveFrame )
s.subscribeTo( subscriptions )
s.start()

scopes = []

def updateAll(arg):
    global scopes
    for scope in scopes:
        scope.update()
    plt.draw()
    return []

fig = plt.figure()
for i in range(n_plots):
    ax = fig.add_subplot(n_plots, 1, i)
    scopes.append( Scope(ax, \
        ['time' for k in plot_vars[i]],\
        plot_vars[i]) )

ani = animation.FuncAnimation(fig, updateAll, interval=100, blit=False)

plt.show()

s.close()

print 'Saving...'
try:
    l = []
    l.append(subscriptions)
    l.append(n_plots)
    l.append(plot_vars)
    f = open('plot_settings.dump', 'wb+')
    pickle.dump(l, f)
    f.close()
    print 'Save successful'
except error:
    print error
    print 'Failed to save settings...'

print 'goodbye'
