import sys, random, threading, serial
from array import array
from math import *


class BusNode:
    """
    This is the parent class of all nodes on the control bus.
    This class describes the memory map of the nodes and generates
    bus command strings with the ControlBus can use to talk to hardware.
    """
    def __init__(self, bus, node_id, name):
        """
        bus is the ControlBus object on which this BusNode exists
        node_id is the position of this node in the bus
        """
        assert node_id >= 0 and node_id <= 15
        assert type(node_id) == type(0)
        self.bus = bus
        self.node_id = node_id
        self.name = name

        # These names describe what you will find at these indices
        self.m_to_s_names = ['NULL' for i in range(32)]
        self.s_to_m_names = ['NULL' for i in range(32)]
        # This is the data we want sent to and from the bus
        self.m_to_s_data  = [None for i in range(32)]
        self.s_to_m_data  = [None for i in range(32)]

        self.bus.addNode(node_id, self)

    def startTransaction(self, memory_offset, data):
        self.bus.startTransaction(self.node_id, memory_offset, data)


class ControlBus:
    """
    A ControlBus is composed of a string of BusNodes talking
    to a single serial port.
    This class contains the serial port and the software representations
    of the nodes.  It handles sending and receiving of messages from the bus.
    """
    def __init__(self, device):
        """
        Open a serial port to a control bus.
        Device is a path the the device, eg. /dev/ttyS0
        """
        self.port = serial.Serial(port=device, baudrate=500000, timeout=1e-2)
        self.nodes = [None]*16
        self.old_packet = ""

        # This read will time out, returning any junk that was in the buffer.
        junk = self.port.read(16384)

        # Ring out the number of nodes.
        packet = chr(0x00)
        self.port.write(packet*20)
        resp = self.port.read(16384)
        # Light validation of response.
        assert len(resp) >= 4 and len(resp) <= 20
        assert resp[-1] == resp[-2] and resp[-2] == resp[-3] and resp[-3] == resp[-4]
        self.num_nodes = 16 - ord(resp[-1]) / 16
        # XXX Can't distinguish 0 and 16; which should we allow?
        assert self.num_nodes <= 15
        print "number of nodes = %d" % self.num_nodes

        # Now switch to non-blocking mode.
        self.port.nonblocking()
        self.port.timeout=0

    def getNodeCount(self):
        """
        Return the number of nodes on the control bus.
        """
        return self.num_nodes
        
    def addNode(self, node_id, node):
        self.nodes[node_id] = node

    def startTransaction(self, node_id, memory_offset, data):
        if len(data) > 0:
            packet = chr(node_id * 16 + len(data) + 1)
            packet += chr(memory_offset)
            packet += data
        else:
            packet = chr(node_id * 16 + 0)
        self.port.write(packet)

    def tick(self):
        # Read any incoming responses.
        packet = self.old_packet + self.port.read(4096)
        while len(packet) > 0:
            data_len = ord(packet[0]) % 16
            if len(packet) < data_len + 1:
                # Wait for the rest of the packet.
                break
            node_id = (ord(packet[0]) / 16) + self.num_nodes - 16
            if data_len > 0:
                memory_offset = ord(packet[1])
                data = packet[2:2+data_len-1]
            else:
                memory_offset = 0
                data = ""
            packet = packet[2+data_len-1:]
            self.nodes[node_id].callback(memory_offset, data)
        self.old_packet = packet
