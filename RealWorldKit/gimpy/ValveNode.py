from BusInterface import *
from math import *

# XXX This is to constrain the speed of the pistons in the leg cart.  The
# valves are capable of driving them much faster than is safe.
SATURATION_LIMIT = 100.0
RATE_EQUALS_ZERO_TOLERANCE = 0.0001


class ValveNode(BusNode):
    def __init__(self, bus, node_id, name, bore, rod, lpm, e_deadband=0, r_deadband=0):
        BusNode.__init__(self, bus=bus, node_id=node_id, name=name)
        bore_section = pi * ((bore / 2) ** 2)
        rod_section = pi * ((rod / 2) ** 2)
        self.max_extend_rate = (lpm / 1000.0 / 60.0) / bore_section
        self.max_retract_rate = (lpm / 1000.0 / 60.0) / (bore_section - rod_section)
        self.e_deadband = e_deadband
        self.r_deadband = r_deadband
        self.pwm0 = 0
        self.pwm1 = 0

    def getPWM0(self):
        return self.pwm0

    def getPWM1(self):
        return self.pwm1

    def setPWM(self, pwm):
        """
        Bypass length rate calculations, set pwms directly
        """
        self.pwm0 = 0
        self.pwm1 = 0
        if pwm < 0:
            self.pwm0 = -pwm
        else:
            self.pwm1 = pwm
        data = chr(int(self.pwm0)) + chr(int(self.pwm1))
        self.startTransaction(memory_offset=0, data=data)

    def setLengthRate(self, rate):
        pwm0 = 0
        pwm1 = 0
        # XXX This uses a linear interpolation between the deadband and the
        # maximum PWM output.  The real valve response is unlikely to be
        # anywhere near so linear.
        if rate < -RATE_EQUALS_ZERO_TOLERANCE:
            pwm0 = (-rate / self.max_retract_rate) * (255.0 - self.r_deadband) + self.r_deadband
            if pwm0 > SATURATION_LIMIT:
                pwm0 = SATURATION_LIMIT
        elif rate > RATE_EQUALS_ZERO_TOLERANCE:
            pwm1 = (rate / self.max_extend_rate) * (255.0 - self.e_deadband) + self.e_deadband
            if pwm1 > SATURATION_LIMIT:
                pwm1 = SATURATION_LIMIT
        self.pwm0 = pwm0
        self.pwm1 = pwm1
        # print self.name, "pwm0", pwm0, "pwm1", pwm1, "rate", rate
        data = chr(int(pwm0)) + chr(int(pwm1))
        self.startTransaction(memory_offset=0, data=data)

    def stop(self):
        data = chr(0) * 2
        self.startTransaction(memory_offset=0, data=data)

    def callback(self, memory_offset, data):
        pass
