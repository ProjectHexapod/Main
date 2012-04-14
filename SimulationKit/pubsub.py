import pickle
from socket import *
import threading
import StringIO
import time

class Publisher:
    def __init__( self, port ):
        # Start the publishing server on specified TCP port
        self.port         = port
        self.sock         = None
        self.conn         = None
        self.serverThread = None
        self.restartflag  = 0

        # Catalog lists all the data offered by the publisher
        self.catalog = {}
        # Subscriptions is a list of all the offerings the client is subscribing to
        self.subscriptions = []

    def addToCatalog( self, name, callback ):
        self.catalog[name] = callback

    def start( self ):
        self.serverThread     = threading.Thread()
        self.serverThread.run = self.run_server
        self.serverThread.setDaemon( True )
        self.serverThread.start()
    
    def publish( self ):
        # Trigger the publisher to send a frame of data
        if self.conn != None and len(self.subscriptions):
            try:
                frame = {}
                for k in self.subscriptions:
                    f = self.catalog[k]
                    if type(f)==tuple:
                        frame[k] = f[0](f[1])
                    else:
                        frame[k] = f()
                self.conn.send(pickle.dumps(frame))
            except error, mesg:
                print mesg

    def run_server( self ):
        print 'Hello from the server thread'
        self.sock = socket( AF_INET, SOCK_STREAM )
        addr = ('localhost', self.port)
        # This is a hack to allow fast restarts
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind( (addr) )
        while 1:
            self.sock.listen(1)
            self.conn,self.remote_addr = self.sock.accept()
            # Send a copy of the catalog
            s = pickle.dumps(self.catalog.keys())
            self.conn.send(s)
            print 'Entering server loop'
            self.restartflag = 0
            # Main server loop
            while not self.restartflag:
                # Wait for request
                try:
                    s = self.conn.recv(4096)
                except error, mesg:
                    print mesg
                    self.restartflag = 1
                if s:
                    # The request must be a list of catalog keys
                    try:
                        keys = pickle.loads(s)
                        self.subscriptions = keys
                    except:
                        print 'Pickle fail'
                        self.restartflag = 1
                else:
                    print "Timed out without receiving"
                    self.restartflag = 1
            self.conn.close()
            self.conn = None

    def close( self ):
        print 'Closing publisher gracefully'
        self.conn.close()
        self.sock.close()

class Subscriber:
    def __init__(self, host, port):
        # Connect to the target publisher
        self.stop_flag = 0
        self.frameReceivedCallback = None
        self.clientThread = None
        self.sock = socket( AF_INET, SOCK_STREAM )
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        print "attempting connection"
        while 1:
            try:
                self.sock.connect( (host,port) )
            except error, desc:
                print desc
                time.sleep(1.0)
            try:
                "waiting for catalog"
                self.catalog = pickle.loads(self.sock.recv(4096))
                break
            except error, desc:
                print desc
                time.sleep(1.0)
            except:
                print 'Pickle fail'
        print 'Received catalog!'
        self.catalog.sort()
        print self.catalog
    def start( self ):
        self.stop_flag = 0
        self.clientThread = threading.Thread()
        self.clientThread.run = self.run_client
        self.clientThread.setDaemon( True )
        self.clientThread.start()
    def subscribeTo( self, name_list ):
        self.sock.send( pickle.dumps(name_list) )
    def run_client( self ):
        # The client waits to receive frames and then calls the callback
        while not self.stop_flag:
            try:
		recv_string = self.sock.recv(4096)
                frame  = pickle.loads(recv_string)
                self.frameReceivedCallback( frame )
            except error, mesg:
                # Socket error
                print mesg
            except:
                print 'Pickle fail'
		# Check if the socket is still connected
		if not len(recv_string):
		    print "Disconnect detected"
		    self.stop_flag = 1
		    break
    def setCallback( self, callback ):
        self.frameReceivedCallback = callback
    def close( self ):
        print 'Closing subscriber gracefully'
        self.stop_flag =  1
        self.sock.close()
        print 'Done'

def dummy_callback( frame ):
    print 'Got frame!'
    for k,v in frame.items():
        print k,v

if __name__=='__main__':
    p = Publisher(5056)
    import random
    p.addToCatalog('mydick', lambda: random.uniform(0,1))
    p.addToCatalog('ass', lambda: random.uniform(0,1))
    p.start()
    time.sleep(0.1)
    s = Subscriber( 'localhost', 5056 )
    s.setCallback( dummy_callback )
    s.subscribeTo(['mydick'])
    s.start()
    for x in range(100):
        p.publish()
        time.sleep(0.01)
    p.close()
    s.close()
    time.sleep(0.1)
