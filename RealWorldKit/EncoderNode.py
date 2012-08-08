from BusInterface import *
from math import *

class EncoderNode(BusNode):
    def __init__(self, bus, node_id, name, gain, offset, bias):
        BusNode.__init__(self, bus=bus, node_id=node_id, name=name)
        self.gain = gain
        self.offset = offset
        self.bias = bias
        self.angle = None
        self.sin_value = 0
        self.cos_value = 0

    def startProbe(self):
        data = chr(0)*4
        self.startTransaction(memory_offset=0, data=data)

    def callback(self, memory_offset, data):
        assert memory_offset == 0 and len(data) == 4
        sin_value = ord(data[0])*256+ord(data[1]) - self.bias[0]
        cos_value = ord(data[2])*256+ord(data[3]) - self.bias[1]
        length = sqrt(sin_value**2 + cos_value**2)
        # XXX Sanity check that the output is sane.  Should be done better.
        #assert length >= 200 and length <= 1200
        self.sin_value = sin_value
        self.cos_value = cos_value
        self.angle = clipAngle(atan2(sin_value, cos_value) * self.gain + self.offset)
        #print self.name, "sin", sin_value, "cos", cos_value, "angle", self.angle*180/pi
    def getSinValue(self):
        return self.sin_value
    def getCosValue(self):
        return self.cos_value
    def getAngle(self):
        return self.angle
    def getAngleDeg(self):
        return 180*self.angle/pi

    def getPosition(self):
        # XXX Need to fill this in.  Possibly split into a separate class.
        return 0

def clipAngle(a):
    if a > pi:
        a -= 2*pi
    elif a < -pi:
        a += 2*pi
    return a
