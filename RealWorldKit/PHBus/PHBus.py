import time
import pcap
import commands
import array
import threading
import signal
from socket import *
from struct import *

from math import *

DEBUG = False

def getmac(iface):
    words = commands.getoutput("ifconfig " + iface).split()
    if "HWaddr" in words:
        mac_str = words[ words.index("HWaddr") + 1 ]
        mac_pieces = mac_str.split(':')
        mac_addr = array.array('B')
        for i in range(len(mac_pieces)):
            mac_addr.append( int(mac_pieces[i], 16) )
        return mac_str, mac_addr.tostring()
    else:
        return '\x00\x00\x00\x00\x00\x00'

def mac_to_str(mac):
    retval = ''
    for c in mac:
        retval += '%02X'%ord(c)
        retval += ':'
    retval = retval[:-1]
    return retval

"""
class PHPacketHeader(Struct):
    _format = Format.BigEndian
    dst_addr = Type.UnsignedByte[6]
    src_addr = Type.UnsignedByte[6]
    magic_word = Type.UnsignedByte
    cmd_id     = Type.UnsignedByte
    packet_id  = Type.UnsignedShort
"""


class WatchDog(object):
    """
    FIXME:  We should have a watchdog in another process.
    This is not particularly safe, but it's safer than nothing.
    """
    lock = threading.Event()
    def __init__(self, timeout = 0.1, callback=None):
        if self.lock.isSet():
            raise Exception, "Only one watchdog can exist at a time!"
        self.lock.set()
        self.timeout = timeout
        self.callback = callback
        if callback:
            signal.signal( signal.SIGALRM, callback )
        else:
            signal.signal( signal.SIGALRM, self._default_callback )
    def __del__(self):
        self.lock.clear()
    def start( self ):
        self.feed()
    def feed( self ):
        """
        Reset the watchdog
        """
        signal.setitimer( signal.ITIMER_REAL, self.timeout )
    def stop( self ):
        signal.setitimer( signal.ITIMER_REAL, 0 )
    def _default_callback( self, signum, frame ):
        print "Watchdog fired!"
        exit(0)

class PHBusInterface(object):
    """
    This is just a physical layer interface that puts data out on the
    ethernet network and receives.  No intelligence.
    FIXME:  I would like this to be based just around Berkeley sockets,
    no pcap BS.  For some reason python raw sockets don't receive correctly.
    """
    def __init__(self, net_if='eth0'):
        """
        """
        self.lock = threading.Lock()
        self.lock.acquire()
        # Set the network interface we're using, default to eth0
        self.net_if = net_if

        # Open a socket to send packets on
        self.sock = socket(AF_PACKET, SOCK_RAW, IPPROTO_RAW)
        self.sock.bind((net_if, 0))

        # Create a list to store received packets
        self.recv_buffer = []
        # Create a dictionary of receive callbacks.
        # These are called upon packet reception, if the received
        # packet matches a callback in the dictionary.
        # Format:
        # { (node_mac, packet_id) : function( raw packet data, timestamp ) ... }
        self.recv_callbacks = {}

        # Open a pcap object to receive packets on
        self.cap = pcap.pcapObject()
        # args are:
        # net interface name
        # Buffer size to allocate
        # Promisc mode on/off
        # time to accumulate packets before making higher level call
        self.cap.open_live(self.net_if, 65535, 1, 10)
        mac_str, src_addr = getmac(net_if)
        self.mac_str  = mac_str
        self.src_addr = src_addr
        self.cap.setfilter( 'ether dst '+mac_str,0,0)
        # Start a listener thread
        self.listen_thread = threading.Thread()
        self.listen_thread.run = self.listener
        self.listen_thread.daemon = 1
        self.listen_thread.start()
        self.lock.release()
    def getMAC( self ):
        return self.src_addr
    def _recv_packet( self, pktlen, data, timestamp ):
        """
        """
        # Check the magic word
        if data[12] != '\x69':
            return
        # Extract the source MAC and packet ID
        src_addr  = data[6:12]
        packet_id = unpack('!H', data[14:16] )[0]
        try:
            self.lock.acquire()
            self.recv_callbacks[ (src_addr, packet_id) ]( data, timestamp )
            if DEBUG:
                print "Matched:"
                print (src_addr, packet_id)
            del self.recv_callbacks[ (src_addr, packet_id) ]
        except KeyError:
            print "Received packet not matching any registered callbacks"
            print mac_to_str( src_addr )
            print packet_id
            print self.recv_callbacks.keys()
            self.recv_buffer.append( (pktlen, data, timestamp) )
        finally:
            self.lock.release()
    def getPacket( self ):
        """
        Returns one packet from the front of the receive buffer.
        """
        if len(self.recv_buffer):
            return self.recv_buffer.pop(0)
        else:
            return None
    def listener(self):
        """
        FIXME:  This has a sleepy wait that adds 1ms of lag.
        """
        print 'Listening...'
        self.cap.setnonblock(1)
        #self.cap.loop( -1, self._recv_packet )
        while 1:
            self.cap.dispatch( 1, self._recv_packet )
            time.sleep(1e-4)
        print 'Listener thread exiting'
    def send(self, data):
        self.sock.send(data)
    def registerReceiveCallback( self, mac, packet_id, callback ):
        """
        """
        self.lock.acquire()
        self.recv_callbacks[ ( mac, packet_id ) ] = callback
        self.lock.release()

class NodeManager(object):
    """
    """
    def __init__(self, interface, dest_addr):
        """
        """
        self.interface = interface
        self.addr      = dest_addr
        ##### THE STRUCTURES BELOW MUST BE THREADSAFE
        ##### self.lock PROTECTS THEM
        self.lock = threading.Lock()
        self.lock.acquire()
        # Packet ID is an incrementing counter
        self.packet_id = 0
        # Keep a copy of the packets we haven't gotten responses to yet
        # { packet_id: (sent_data, recv_callback) }
        self.outstanding_packets = {}
        # This event represents whether there are any outstanding packets or not.
        self.synced = threading.Event()
        self.synced.set()
        self.lock.release()

        # TODO: represent this more elegantly.
        # mag_encoder_count is an integer in [0,4096)
        self.mag_encoder_count = 0
        # mag_encoder_good is based on the INC and DEC flags from the encoder
        # and whether the parity check is correct
        self.mag_encoder_good = 0

    def forceSync( self ):
        """
        Clears the internal outstanding packet buffers and resets the sync lock
        """
        raise NotImplemented
    def waitForSync( self, timeout=1e6 ):
        """
        Timeout is in seconds.  None means wait indefinitely
        returns false if timeout occurs.
        FIXME: timeout arg doesn't work right... supplying None should
        wait indefinitely but instead does...something...weird... and
        messes with the watchdog.
        """
        return self.synced.wait(timeout)
    def isSynced( self ):
        return self.synced.isSet()
    def _send_outerlayer( self, cmd_id, payload="", callback=None ):
        """
        Master send function.
        cmd_id is the command ID
        payload is everything in the frame after the packet id
        """
        send_str = ""
        # Pack the dest address
        send_str += self.addr
        # Pack the source addr
        send_str += self.interface.getMAC()
        # Pack the magic (0x69)
        send_str += '\x69'
        # Pack the command ID
        send_str += pack('!B', cmd_id)
        # Pack the packet id
        send_str += pack('!H', self.packet_id)
        # Pack the payload
        send_str += payload
        # Pad the frame
        send_str += '\x00'*(60-len(send_str))
        # TODO - implement non-blocking send behavior.
        self.waitForSync()
        self.lock.acquire()
        # Install the hook for when the response is received
        self.interface.registerReceiveCallback( self.addr, self.packet_id, self.receive_callback )
        # Save the sent packet so we can match it up when we receive the response
        self.outstanding_packets[self.packet_id] = (send_str, callback)
        # We have an outstanding packet and are no longer synced.  Reflect this.
        self.synced.clear()
        # send the frame
        self.interface.send(send_str)
        # Finished
        self.packet_id += 1
        self.packet_id %=  pow(2,16)
        self.lock.release()
    def sendGenericReadWrite( self, read_addr=0, read_len=0, write_addr=0, write_len=0, write_data=None, callback=None ):
        """
        Sends a command ID 0
        """
        send_str = ""
        send_str += pack('!H', read_addr)
        # Pack the read len
        send_str += pack('!H', read_len)
        # Pack the write addr
        send_str += pack('!H', write_addr)
        # Pack the write len
        send_str += pack('!H', write_len)
        # Pack the data to write, if any
        if write_len:
            if len(write_data)==write_len:
                send_str += write_data
            else:
                print 'Supplied write_len does not match length of supplied data'
                raise
        self._send_outerlayer( 0, send_str, callback=callback )
    def commitToFlash( self ):
        """
        Whatever changes have been made to the node, commit them to
        non-volatile memory.
        """
        self._send_outerlayer( 1 )
    def reset( self ):
        """
        Reset the node
        """
        self._send_outerlayer( 2 )
    def sendMACAddr( self, new_addr ):
        """
        Send a new MAC addr to the target node.
        DOES NOT COMMIT NEW MAC TO FLASH.
        Node will not present as new MAC until reset.
        """
        assert len(new_addr) == 6, "Supplied MAC addr not 6 bytes!"
        self.sendGenericReadWrite( 0, 0, 0, 6, new_addr )
    def changeMACAddr( self, new_addr ):
        """
        Program a new MAC addr to the node
        """
        self.sendMACAddr( new_addr )
        self.commitToFlash()
    def _evenParity( self, arg ):
        val = arg
        n = 0
        while val:
            n += val&1
            val = val >> 1
        return not n%2
    def _printMagData( self, senf_data, recv_data, timestamp ):
        """
        Helper function to read magnetic encoder data from a packet
        """
        #reduced = (ord(recv_data[16])<<16) + (ord(recv_data[17])<<8) + (ord(recv_data[18]))
        reduced = unpack('!L', recv_data[15:19])[0]
        reduced = reduced & 0x00ffffff
        reduced = reduced >> 5

        parity = reduced & 1
        reduced = reduced >> 1

        if parity != self._evenParity(reduced):
            print 'PARITY ERROR'
        
        magdec = reduced & 1
        reduced = reduced >>1

        maginc = reduced & 1
        reduced = reduced >>1

        linearity = reduced & 1
        reduced = reduced >>1

        cof = reduced & 1
        reduced = reduced >>1

        ocf = reduced & 1
        reduced = reduced >>1

        angle = reduced & 0xfff

        print 'parity\t', parity
        print 'magdec\t', magdec
        print 'maginc\t', maginc
        print 'linear\t', linearity
        print 'cordic\t', cof
        print 'offset\t', ocf
        print 'angle\t', angle
        print ''
    def getMagEncoderAngle( self ):
        """
        Return the angle in radians, as well as the good flag.
        returns: (float angle in radians, bool good)
        """
        angle_radians = 2*pi*(self.mag_encoder_count/4096.)
        return angle_radians, self.mag_encoder_good
    def _processMagData( self, senf_data, recv_data, timestamp ):
        """
        Helper function to read magnetic encoder data from a packet
        Populates self.mag_encoder_count and self.mag_encoder_good
        """
        reduced = unpack('!L', recv_data[15:19])[0]
        reduced = reduced & 0x00ffffe0
        reduced = reduced >> 5

        parity = reduced & 1
        reduced = reduced >> 1
        parity_correct = parity == self._evenParity(reduced)

        
        magdec = reduced & 1
        reduced = reduced >>1

        maginc = reduced & 1
        reduced = reduced >>1

        linearity = reduced & 1
        reduced = reduced >>1

        cof = reduced & 1
        reduced = reduced >>1

        ocf = reduced & 1
        reduced = reduced >>1

        angle = reduced & 0xfff

        self.mag_encoder_count = angle
        self.mag_encoder_good = (parity_correct*4) + (magdec*2) + (maginc*1)

        if 0:
            print 'parity\t', parity
            print 'magdec\t', magdec
            print 'maginc\t', maginc
            print 'linear\t', linearity
            print 'cordic\t', cof
            print 'offset\t', ocf
            print 'angle\t', angle
            print ''
    def exchangeMagValveData( self, valve_command ):
        """
        Send a valve command and requests magnetic encoder data back.
        args:
            valve_command: float: -1 to 1
        """
        payload = ""
        # offset 15
        # unsigned char valve_power
        # signed char valve_dir
        valve_power = int(abs(valve_command)*256)
        if valve_command == 0:
            valve_dir = 0
        else:
            valve_dir = int(valve_command/abs(valve_command))
        payload += pack('!Bb', valve_power, valve_dir)
        # addr 12 len 3 is the offset for reading back mag enc data
        #self.sendGenericReadWrite( 12, 3, 15, 2, payload, self._printMagData )
        self.sendGenericReadWrite( 12, 3, 15, 2, payload, self._processMagData )
    def receive_callback( self, recv_data, timestamp ):
        """
        This function is meant to be called only by the PHBusInterface's
        receive callback handler.
        """
        self.lock.acquire()
        # Extract the packet ID
        packet_id = unpack('!H', recv_data[14:16] )[0]
        try:
            # Find the matching packet in sent packets
            send_data, callback = self.outstanding_packets[packet_id]
            del self.outstanding_packets[packet_id]
            # Check to see if we're synced
            if len(self.outstanding_packets) == 0:
                if DEBUG:
                    print 'Synced! Setting self.synced...'
                self.synced.set()
            else:
                if DEBUG:
                    print 'Not synced, %d outstanding remain'%len(self.outstanding_packets)
            # If a callback was set, call it
            if callback:
                callback( send_data, recv_data, timestamp )
        except KeyError:
            print "WARNING: Received a packet without a sent packet matching up"
            print "         Node:      %s"%mac_to_str(self.addr)
            print "         Packet ID: %d"%packet_id
        self.lock.release()

class BusManager(object):
    """
    The BusManager is a container for NodeManagers constituting a bus
    and the PHBusInterface they exist on.  It provides high level
    access to the bus.
    """
    def __init__( self, iface_name='eth0', node_addrs=[] ):
        """
        iface_name is a string containing the network interface the bus is connected to.
        node_addrs is a list of MAC addresses, already in binary (strings of length 6)
        """
        self.iface = PHBusInterface(iface_name)
        # self.nodes is a dictionary { mac_address : NodeManager instance, ... }
        self.nodes = [ NodeManager(self.iface,addr) for addr in node_addrs ]
    def discover( self ):
        """
        Broadcasts packets out to the bus and looks for responses.  Could be helpful
        in the future.
        TODO: Implement.  Am not sure if the firmware presently accepts broadcast packets.
        """
        raise NotImplemented
    def waitForSync( self, timeout=1e3 ):
        """
        Waits for sync with all nodes on the bus.
        """
        t_start = time.time()
        for node in self.nodes:
            t_remaining = timeout - (time.time()-t_start)
            if t_remaining <= 0.0:
                break
            node.waitForSync(t_remaining)
        return (t_remaining > 0.0)
    def callForEachNode( self, callback, args_list=None ):
        """
        Code shorter than comments would be.  Read code.
        """
        if(args_list == None):
            pass
        retval = []
        for node, args in zip(self.nodes, args_list ):
            retval.append(callback( node, *args ))
        return retval
    def getMagEncoderAngle( self ):
        values = self.callForEachNode( NodeManager.getMagEncoderAngle, [[] for node in self.nodes] )
        angles, flags = zip(*values)
        return angles, flags
    def pingNodes( self ):
        """
        Pings the nodes with an empty command one by one.
        returns
        """
    def exchangeMagValveData( self, valve_commands ):
        self.callForEachNode( NodeManager.exchangeMagValveData, [[cmd] for cmd in valve_commands] )
    def softStop( self ):
        """
        Tell all nodes to close valves.
        TODO: should this be here or is this too low level?
        """
        raise NotImplemented

if __name__=="__main__":
    print 'Starting demo...'
    def gracefulShutdown( signum, stack ):
        print "Watchdog fired!"
        print "Got signal %d"%signum
        print "Goodbye!"
        exit(0)
    watchdog = WatchDog( 0.1, gracefulShutdown )
    n_iterations = int(1e6)
    if 0:
        iface = PHBusInterface('eth0')
        node_manager = NodeManager( iface,  "\x00\xCF\x52\x35\x00\x07" )
        watchdog.start()
        t_start = time.time()
        for i in range(n_iterations):
            #node_manager.sendGenericReadWrite()
            node_manager.exchangeMagValveData(.5)
            watchdog.feed()
        node_manager.waitForSync()
    if 1:
        mac_list = []
        mac_list.append( "\x00\xCF\x52\x35\x00\x07" );
        mac_list.append( "\x00\xCF\x52\x35\x00\x08" );
        mac_list.append( "\x00\xCF\x52\x35\x00\x09" );
        valve_commands = [0.0 for entry in mac_list]
        bus_manager = BusManager( 'eth0', mac_list )
        watchdog.start()
        t_start = time.time()
        for i in range(n_iterations):
            #bus_manager.sendGenericReadWrite()
            bus_manager.exchangeMagValveData(valve_commands)
            ang, flag = bus_manager.getMagEncoderAngle()
            print ang
            print flag
            watchdog.feed()
            time.sleep(1e-3)
        bus_manager.waitForSync()
    if 0:
        print "Changing MAC"
        new_mac = "\x00\xCF\x52\x35\x00\x08"
        node_manager.changeMACAddr( new_mac )
    print "Elapsed: %0.03fs"%(time.time()-t_start)
    print "Avg: %0.03fms"%(1000*(time.time()-t_start)/n_iterations)
