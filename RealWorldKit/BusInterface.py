import sys, random, threading, serial
from array import array
from math import *

from pubsub import *
from helpers import *

class NodeTransaction:
    """
    A transaction with a single node that can consist of multiple
    reads and writes.
    """
    def __init__(self, target_node = 0):
        """
        Initialize as an empty string.
        """
        assert target_node <  16
        assert target_node >= 0
        assert type(target_node) == type(0)
        self.target_node = target_node
        self.cmd_str     = array('B')
        # Add a place holder for the header
        self.cmd_str.append(0x00)
    def setTargetNode(self, node):
        assert node <  16
        assert node >= 0
        assert type(node) == type(0)
        self.target_node = node

    def addReadCommand(self, index):
        assert index <  32
        assert index >= 0
        assert type(index) == type(0)
        self.cmd_str.append(index)
    def addWriteCommand(self, index, value):
        assert index <  32
        assert index >= 0
        assert type(index) == type(0)
        assert value < 256
        assert value >= 0
        assert type(value) == type(0)
        self.cmd_str.append(index+128)
        self.cmd_str.append(value)
    def generateHeader( self ):
        """
        Examine the command string and generate an appropriate header byte.
        The header encodes the node id and the length of the command string.
        """
        data_len = len(self.cmd_str) - 1
        assert data_len < 16
        self.cmd_str[0] = data_len*16 + self.target_node
    def getString( self ):
        return str(self.cmd_str)

class BusNode:
    """
    This is the parent class of all nodes on the control bus.
    This class describes the memory map of the nodes and generates
    bus command strings with the ControlBus can use to talk to hardware.
    """
    def __init__(self, bus, index):
        """
        bus is the ControlBus object on which this BusNode exists
        index is the position of this node in the bus
        """
        assert type(index) == type(0)
        assert index >= 0 and index < 16
        self.bus = bus
        self.index = index
        # These names describe what you will find at these indices
        self.m_to_s_names = ['NULL' for i in range(32)]
        self.s_to_m_names = ['NULL' for i in range(32)]
        # This is the data we want sent to and from the bus
        self.m_to_s_data  = [None for i in range(32)]
        self.s_to_m_data  = [None for i in range(32)]


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
        self.port = serial.Serial(port=device, baudrate=1000000, timeout=1e-2)
        self.nodes = []
    def addNode( self, node_constructor ):
        self.nodes.append(node_constructor(self, len(self.nodes)))
    def countNodes( self ):
        """
        Count the nodes on the control bus
        """
        # Generate a null transaction
        cmd_str = NodeTransaction().getString()
        s.write(cmd_str)
        retval = s.read(len(cmd_str))

    def validateDescription( self ):
        """
        validateDescription checks that the description that has been fed
        in to this class instance by progressive calls to addNode matches the
        hardware.
        It does this by first checking the number of nodes on the bus.
        Then it goes through one by one checking the node type field on the
        memory maps of the nodes on the bus.
        """
    def sendCommandString( self, cmd_str):
        """
        """
        #TODO: WRITE
        s.write(cmd_str)
        retval = s.read(len(cmd_str))
        


class RobotServer:
    """
    RobotServer is responsible for talking to all control buses, calling control code
    and sanity checking.
    """
    def __init__(self):
        """
        """
        self.buses = {}
    def addBus(self, name=None, device=None):
        """
        Opens a serial port to the control bus
        """
    def getLastTime(self):
        """
        Return the last time sensor values were updated
        """
        pass
