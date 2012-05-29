from BusInterface import *
from math import *

SATURATION_LIMIT = 200.0

class ValveNode(BusNode):
    def __init__(self, bus, node_id, name, bore, rod, lpm, deadband=0):
        BusNode.__init__(self, bus=bus, node_id=node_id, name=name)
        bore_section = pi*((bore/2)**2)
        rod_section = pi*((rod/2)**2)
        self.extend_rate = (lpm/1000.0/60.0) / bore_section
        self.retract_rate = (lpm/1000.0/60.0) / (bore_section - rod_section)
        self.deadband = deadband

    def setLengthRate(self, rate):
        pwm0 = 0
        pwm1 = 0
        if rate < 0:
            pwm0 = (-rate / self.retract_rate) * (255.0 - self.deadband) + self.deadband
            if pwm0 > SATURATION_LIMIT:
                pwm0 = SATURATION_LIMIT
        elif rate > 0:
            pwm1 = (rate / self.extend_rate) * (255.0 - self.deadband) + self.deadband
            if pwm1 > SATURATION_LIMIT:
                pwm1 = SATURATION_LIMIT
        print self.name, "pwm0", pwm0, "pwm1", pwm1, "rate", rate
        data = chr(int(pwm0)) + chr(int(pwm1))
        self.startTransaction(memory_offset=0, data=data)

    def stop(self):
        data = chr(0)*2
        self.startTransaction(memory_offset=0, data=data)

    def callback(self, memory_offset, data):
        pass
