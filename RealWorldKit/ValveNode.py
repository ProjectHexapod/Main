from BusInterface import *
from math import *

# XXX This is to constrain the speed of the pistons in the leg cart.  The
# valves are capable of driving them much faster than is safe.
SATURATION_LIMIT = 200.0

class ValveNode(BusNode):
    def __init__(self, bus, node_id, name, bore, rod, lpm, deadband=0):
        BusNode.__init__(self, bus=bus, node_id=node_id, name=name)
        bore_section = pi*((bore/2)**2)
        rod_section = pi*((rod/2)**2)
        self.max_extend_rate = (lpm/1000.0/60.0) / bore_section
        self.max_retract_rate = (lpm/1000.0/60.0) / (bore_section - rod_section)
        self.deadband = deadband

    def setLengthRate(self, rate):
        pwm0 = 0
        pwm1 = 0
	# XXX This uses a linear interpolation between the deadband and the
	# maximum PWM output.  The real valve response is unlikely to be
	# anywhere near so linear.
        if rate < 0:
            pwm0 = (-rate / self.max_retract_rate) * (255.0 - self.deadband) + self.deadband
            if pwm0 > SATURATION_LIMIT:
                pwm0 = SATURATION_LIMIT
        elif rate > 0:
            pwm1 = (rate / self.max_extend_rate) * (255.0 - self.deadband) + self.deadband
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
