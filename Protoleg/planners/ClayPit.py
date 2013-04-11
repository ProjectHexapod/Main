import sys
sys.path.append('..')

class OneDClayPit(object):
    def __init__(self, min_x, max_x, n_points, name=None, init_func=None, k=0.0e-3, max_slope=None, force_monotonic=True):
        """
        min_x and max_x determine the length of the x axis.
        The x axis is then subdivided in to n_points points
        init_func must take one float and return one float.  If provided, it is used
            to initialize the pit.
        k is the fraction of the distance a point in the pit will change when
            provided with a new reading.
        max_slope is the slope beyond which adjacent points will tug at eachother
        force_monotonic forces a positive slope.
        """
        self.name = name
        self.k = k
        self.force_monotonic=force_monotonic
        self.min_x = min_x
        self.dx = (max_x - min_x)/(n_points-1)
        # Internally we express max slope as maximum change between two adjacent cells
        #   in memory.  Externally it's maximum dy/dx
        self.max_dy = max_slope*self.dx

        try:
            self.loadState()
        except IOError:
            print 'No saved state found for %s, generating new profile'%self.name
            self.mem = [0.0 for i in range(n_points)]
            if init_func != None:
                for i in range(n_points):
                    self.mem[i] = init_func(self.min_x+i*self.dx)

    def __index(self, x):
        index = (x-self.min_x)/self.dx
        remainder = index%1
        index = int(index)
        if index < 0:
            index = 0
        elif index > len(self.mem)-2:
            index = len(self.mem)-2
        return index, remainder
    def __interp(self, x):
        index, remainder = self.__index(x)
        retval = (1.0-remainder)*self.mem[index] + (remainder)*self.mem[index+1]
        return retval
    def __smoothneg( self, i ):
        if i == 0:
            return
        dy = self.mem[i] - self.mem[i-1]
        if dy > self.max_dy:
            self.mem[i-1] = self.mem[i] - self.max_dy
            self.__smoothneg(i-1)
        elif self.force_monotonic and dy < 0:
            self.mem[i-1] = self.mem[i]
            self.__smoothneg(i-1)
    def __smoothpos( self, i ):
        if i == len(self.mem)-1:
            return
        dy = self.mem[i+1] - self.mem[i]
        if dy > self.max_dy:
            self.mem[i+1] = self.mem[i] + self.max_dy
            self.__smoothpos(i+1)
        elif self.force_monotonic and dy < 0:
            self.mem[i+1] = self.mem[i]
            self.__smoothpos(i+1)
    def lookup(self, x, y=None, k=None):
        """
        Read the value of the pit at x.
        If y is supplied, push the clay in the direction of y.
        """
        retval = self.__interp(x)
        if y == None:
            return retval
        # Poke the pit
        index,remainder = self.__index(x)
        
        if k == None:
            k = self.k
        
        dy = y-self.mem[index]
        self.mem[index] += k * (1.0-remainder) * dy
        dy = y-self.mem[index+1]
        self.mem[index+1] += k * (remainder) * dy

        # Smooth out the pit in both directions
        self.__smoothneg( index )
        self.__smoothpos( index+1 )
    def printpit(self):
        s=''
        for f in self.mem:
            s += '%0.2f '%f
        print s
        print '\n\n'
    def saveState( self ):
        import pickle
        f = open(self.name, 'wb+')
        pickle.dump(self.mem, f)
        f.close()
    def loadState( self ):
        import pickle
        f = open(self.name, 'rb')
        self.mem = pickle.load(f)
        f.close()
        print 'load success:', self.name
    def dumpToFile( self, fname ):
        """
        Dump the mem to a csv
        """
        f = open(fname, 'w+')
        f.write('x, y\r\n')
        for i in range(len(self.mem)):
            x = self.min_x + self.dx*i
            y = self.mem[i]
            f.write('%1.5f, %1.5f\r\n'%(x,y))
        f.close()

if __name__=='__main__':
    pit = OneDClayPit( -1.0, 1.0, 100, lambda(x):x, k=1e-3, max_slope=1.0, discontinuities_x=[0.0] )
    def printpit(pit):
        s=''
        for f in pit.mem:
            s += '%0.2f '%f
        print s
        print '\n\n'
    printpit(pit)
    for i in range(1000):
        pit.lookup(0.1, 1.0)
    printpit(pit)
    for i in range(1000):
        pit.lookup(0.1, 0.0)
    printpit(pit)
    for i in range(1000):
        pit.lookup(-0.1, 1.0)
    printpit(pit)
    for i in range(1000):
        pit.lookup(-0.1, -1.0)
    printpit(pit)
