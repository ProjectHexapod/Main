from socket import *
import pcap
from ctypes import *
from struct import *
import time
import commands
import array
import threading
import binascii

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
        retval += '%2X'%ord(c)
        retval += ':'
    retval = retval[:-1]
    return retval

def even_parity( arg ):
    val = arg
    n = 0
    while val:
        n += val&1
        val = val >> 1
    return not n%2

total_delay = 0.0
n_recv = 0

def read_packet( pktlen, data, timestamp ):
    global packet_id, stime, total_delay, n_recv
    rtime = time.time()
    print "Received %d bytes"%pktlen
    delay_ms = (rtime-stime)*1000
    total_delay += delay_ms
    n_recv += 1
    print 'Delay: %.2fms'%(total_delay/n_recv)
    print 'DST: ' + mac_to_str( data[ : 6] )
    print 'SRC: ' + mac_to_str( data[6:12] )
    s = ''
    data = [ ord(c) for c in data ]
    local_packet_id = (data[14]<<8) + (data[15])
    if local_packet_id != packet_id:
        print "PACKET_ID MISMATCH!"
        print "Received: %d"%local_packet_id
        print "Sent:     %d"%packet_id
        return
    for c in data:
        s += '%2X '%c
    reduced = (data[16]<<16) + (data[17]<<8) + (data[18])
    reduced = reduced >> 5

    print 'reduced\t', reduced

    parity = reduced & 1
    reduced = reduced >> 1

    if parity != even_parity(reduced):
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

def listener():
    global p
    print 'Listening...'
    p.setnonblock(1)
    while 1:
        p.dispatch( 1, read_packet )
        time.sleep(0.00001)

        

net_if = 'eth0'

s = socket(AF_PACKET, SOCK_RAW, IPPROTO_RAW)
s.bind((net_if, 0))

p = pcap.pcapObject()
net, mask = pcap.lookupnet(net_if)
# args are:
# net interface name
# Buffer size to allocate
# Promisc mode on/off
# time to accumulate packets before making higher level call
p.open_live(net_if, 65535, 1, 10)
time.sleep(0.01)

# We're putting together an ethernet frame here, 
# but you could have anything you want instead
# Have a look at the 'struct' module for more 
# flexible packing/unpacking of binary data
# and 'binascii' for 32 bit CRC

# 1 magic word (0x69)
# 1 command id (0)
# 2 packet id  (incrementing)
# 2 read addr  (12 gets us the magnetic encoder data )
# 2 read len   (3 is the number of bytes of magnetic encoder data)
# 2 write addr (15 is the start of valve power and dir)
# 2 write len  (2 is the number of bytes to set valve power and dir)
# 2 data to write (we know in this case we want to write just two bytes)

# ! means put in network byte order
send_pack = Struct('!B B H   H H H H Bb')
mac_str, src_addr = getmac(net_if)
p.setfilter( 'ether dst '+mac_str,0,0)
dst_addr = "\x00\xCF\x52\x35\x00\x07"
duty = 0
v_dir = 0
magic_num = 0x69
cmd_id    = 0
packet_id = 0

listen_thread = threading.Thread()
listen_thread.run = listener
listen_thread.daemon = 1
listen_thread.start()

try:
    while True:
        send_str = send_pack.pack(  magic_num, 
                                    0, 
                                    packet_id, 
                                    12, 
                                    3,
                                    15,
                                    2,
                                    duty,
                                    v_dir)
        send_str = dst_addr+src_addr+send_str
        #Pad
        send_str += '\x00'*(60-len(send_str))
        print 'Sending: %s'%send_str
        #crc = binascii.crc32(send_str)
        #print 'crc32 = 0x%08x' % crc
        #send_str += pack('<I', crc)
        stime = time.time()
        s.send(send_str)
        time.sleep(0.1)
        #duty = 32
        #v_dir = 1
        duty += 4
        if duty > 250:
            duty = 0
            if v_dir == -1:
                v_dir = 1
            else:
                v_dir = -1
        print 'Duty: %d'%duty
        packet_id += 1
        if packet_id > 1000:
            packet_id = 0
except KeyboardInterrupt:
    s.close()
    print '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()

