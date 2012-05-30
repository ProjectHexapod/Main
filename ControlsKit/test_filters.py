from numpy.core.umath import pi
from filters import *


import unittest

from time_sources import global_time, resetTimeSourceForTestingPurposes
from numpy import arange


#def generate_sin_array(frequency):
#    time_array = arange(0., frequency*pi, 0.0001)


class LowPassFilterTestCase(unittest.TestCase):
    def setUp(self):
        resetTimeSourceForTestingPurposes(global_time)
        self.filter = LowPassFilter(1., 0.8)
        self.filter.update(0.)

    def _step(self, time, signal):
        global_time.updateDelta(time)
        return self.filter.update(signal)

    def test_passes_low_frequencies(self):
        self.assertAlmostEqual(20., self._step(1.e15, 20.))

    def test_cuts_high_frequencies(self):
        self.assertAlmostEqual(0., self._step(1.e-15, 10.))


class HighPassFilterTestCase(unittest.TestCase):
    def setUp(self):
        resetTimeSourceForTestingPurposes(global_time)
        self.filter = HighPassFilter(1., 0.8)
        self.filter.update(0.)

    def _step(self, time, signal):
        global_time.updateDelta(time)
        return self.filter.update(signal)

    def test_cuts_low_frequencies(self):
        self.assertAlmostEqual(0., self._step(1.e15, 20.))

    def test_passes_high_frequencies(self):
        self.assertAlmostEqual(10., self._step(1.e-15, 10.))

if __name__ == '__main__':
    unittest.main()

