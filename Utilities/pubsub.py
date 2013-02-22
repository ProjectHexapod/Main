import pickle
from socket import *
import threading
import StringIO
import time

class Publisher(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Publisher, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    def __init__( self, port ):
        if hasattr(self, 'initialized'):
            print 'Publisher has already initialized, but new one requested.  Returning old instance'
            return
        print 'Initializing new publisher'
        # Start the publishing server on specified TCP port
        self.port         = port
        self.sock         = None
        self.conn         = None
        self.serverThread = None
        self.restartflag  = 0
        self.ready_to_publish = 0

        # Catalog lists all the data offered by the publisher
        self.catalog = {}
        # Subscriptions is a list of all the offerings the client is subscribing to
        self.subscriptions = []
        # These are publishers that the remote side asked us to intantiate
        self.sub_publishers = []
        # Flag to let the world know we're initialized
        self.initialized = 1

    def addToCatalog( self, name, callback ):
        self.catalog[name] = callback

    def start( self ):
        if not self.serverThread:
            self.serverThread     = threading.Thread()
            self.serverThread.run = self.run_server
            self.serverThread.setDaemon( True )
            self.serverThread.start()
    
    def publish( self ):
        # Trigger the publisher to send a frame of data
        if self.ready_to_publish and len(self.subscriptions):
            try:
                frame = {}
                for k in self.subscriptions:
                    f = self.catalog[k]
                    if type(f)==tuple:
                        frame[k] = f[0](f[1])
                    else:
                        frame[k] = f()
                bytes_sent = self.conn.send(pickle.dumps(frame))
                if not bytes_sent:
                    print "Remote disconnect detected"
            except error, mesg:
                print mesg
        # Trigger the sub-publishers to publish
        for publisher in self.sub_publishers:
            publisher.publish()

    def run_server( self ):
        print 'Hello from the publisher server thread on port %d'%self.port
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
                    # Presently two requests are supported:
                    # A list of subscriptions
                    # A new port to open another publisher on
                except error, mesg:
                    print mesg
                    self.restartflag = 1
                if s:
                    try:
                        data = pickle.loads(s)
                        if type(data) == type(0):
                            # Request to open another publisher on a different
                            # port.
                            port = data
                            print "Received request for new publisher on port"\
                                " %d"%port
                            new_pub = Publisher(port)
                            # FIXME: This feels hacky... new publisher refers to
                            # the old publisher's catalog
                            new_pub.catalog = self.catalog
                            new_pub.start()
                            self.sub_publishers.append(new_pub)
                        elif type(data) == type([]):
                            # Subscription request
                            keys = data
                        self.subscriptions = keys
                        self.ready_to_publish = True
                    except:
                        print 'Pickle fail'
                        self.restartflag = 1
                else:
                    print "Timed out without receiving"
                    self.restartflag = 1
            self.ready_to_publish = False
            self.conn.close()
            self.conn = None

    def close( self ):
        print 'Closing publisher gracefully'
        self.conn.close()
        self.sock.close()
        for publisher in self.sub_publishers:
            publisher.close()

class Subscriber:
    def __init__(self, host, port):
        # Connect to the target publisher
        self.stop_flag = 0
        self.frameReceivedCallback = None
        self.clientThread = None
        self.sock = socket( AF_INET, SOCK_STREAM )
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # Call this when the other side disconnects
        self.remoteDisconnectCallback = None
        while 1:
            try:
                self.sock.connect( (host,port) )
            except error, desc:
                print desc
                time.sleep(1.0)
            try:
                #waiting for catalog
                self.catalog = pickle.loads(self.sock.recv(4096))
                break
            except error, desc:
                print desc
                time.sleep(1.0)
            #except:
            #    print 'Pickle fail'
        self.catalog.sort()
    def start( self ):
        self.stop_flag = 0
        self.clientThread = threading.Thread()
        self.clientThread.run = self.run_client
        self.clientThread.setDaemon( True )
        self.clientThread.start()
    def subscribeTo( self, name_list ):
        self.sock.send( pickle.dumps(name_list) )
    def requestAnotherPublisher( self, port ):
        self.sock.send( pickle.dumps(port) )
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
                    if self.remoteDisconnectCallback:
                        self.remoteDisconnectCallback()
    def setCallback( self, callback ):
        self.frameReceivedCallback = callback
    def close( self ):
        print 'Closing subscriber gracefully'
        self.stop_flag =  1
        self.sock.close()
        print 'Done'

if __name__=='__main__':
    def dummy_callback( frame ):
        print 'Got frame!'
        for k,v in frame.items():
            print k,v
    p = Publisher(5055)
    q = Publisher(5057)
    if id(p) != id(q):
        print "Only one publisher should ever be instantiated!"
    import random
    p.addToCatalog('foo', lambda: random.uniform(0,1))
    p.addToCatalog('bar', lambda: random.uniform(0,1))
    p.start()
    time.sleep(0.1)
    s = Subscriber( 'localhost', 5055 )
    s.setCallback( dummy_callback )
    s.subscribeTo(['foo'])
    s.start()
    for x in range(20):
        p.publish()
        time.sleep(0.01)
    p.close()
    s.close()
    time.sleep(0.1)
