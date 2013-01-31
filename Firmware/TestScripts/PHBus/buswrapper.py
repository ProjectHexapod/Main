from subprocess import *
import time
import os
import select
import fcntl

from high_struct import *
from cStringIO import StringIO

class PHStreamHeader(Struct):
    _format = Format.BigEndian
    data_len = Type.UnsignedShort

class PHBusInterface(object):
    """
    It's been a long and terrible journey to this design.
    Python's built in socket doesn't work in raw receive
    mode for some reason.  I don't know why.  I didn't want
    to bother with wrapping, so I wrote a little c program
    that locks down a network interface in raw mode and
    forwards traffic from stdin to the NIC, and from the NIC
    so stdout, filtering for the packets that bear our magic
    number.

    There was probably some clever way to do it with socat.

    This class starts the c program and opens pipes to it.
    It sets the pipes to non-blocking.
    """
    def __init__(self, if_name='eth0'):
        """
        if_name is the name of the interface we want to lock down.
        """
        self.bus_sub = Popen(["./PHBusTest", if_name], bufsize=0,\
            stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

        # make pipes non-blocking
        fl = fcntl.fcntl(self.bus_sub.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.bus_sub.stdout, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        fl = fcntl.fcntl(self.bus_sub.stdin, fcntl.F_GETFL)
        fcntl.fcntl(self.bus_sub.stdin, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # buffer of received packets
        self.recv_buf = []
        self.recv_stream = ''
    def send( self, payload ):
        """
        Send a single packet of data to the interface.
        payload is a full ethernet payload, complete with MAC addrs.
        """
        stream_payload = StringIO()
        stream_header=PHStreamHeader()
        stream_header.data_len = len(payload)
        stream_payload.write(str(stream_header))
        stream_payload.write(payload)
        self.bus_sub.stdin.write(stream_payload.getvalue())
        self.bus_sub.stdin.flush()
    def recv( self, timeout=1.0 ):
        """
        Receive a single packet from the interface.
        Returns the complete ethernet payload, complete with MAC addrs.
        If timeout elapses before packet arrives, returns empty string.
        """
        (rlist, wlist, xlist) = select.select( [self.bus_sub.stdout], [], [], timeout )
        if len(rlist):
            self.recv_stream += self.bus_sub.stdout.read()
            print 'len recv_stream: %d'%len(self.recv_stream)
            s = StringIO(self.recv_stream)
            while s.tell() < len(self.recv_stream):
                stream_header  = PHStreamHeader(s.read(PHStreamHeader._struct_size))
                print stream_header.data_len
                packet_payload = s.read(stream_header.data_len)
                self.recv_buf.append(packet_payload)
            self.recv_stream = self.recv_stream[s.tell():]
            s.close()
        if len(self.recv_buf):
            return self.recv_buf.pop(0)
        else:
            return ''

def getmac(iface):
    import commands
    import array
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

if __name__=='__main__':
    iface_name = 'eth0'
    iface = PHBusInterface(iface_name) 
    dst_addr = '\x00\xCF\x52\x35\x00\x07'
    mac_str, src_addr = getmac(iface_name)
    magic_word = '\x69\x00'
    print iface.bus_sub.poll()
    print 'Sending...'
    iface.send(dst_addr+src_addr+magic_word+'fuuuuck')
    print 'Sent'
    print iface.bus_sub.poll()
    count = 0
    while 1:
        pack = iface.recv()
        print iface.bus_sub.poll()
        if pack:
            print '%04d. Received %d bytes'%(count,len(pack))
            count += 1
        else:
            break
