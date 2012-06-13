from numpy.core.umath import pi
from filters import *
import numpy as np


import unittest

from time_sources import global_time, resetTimeSourceForTestingPurposes
from numpy import arange


#def generate_sin_array(frequency):
#    time_array = arange(0., frequency*pi, 0.0001)

class FilterTestBase(object):

    def _step(self, time, signal):
        global_time.updateDelta(time)
        return self.filter.update(signal)

    def _percent_passed(self, frequency):
        """
        Returns the portion of the amplitude of a signal that is passed
        at a given frequency.
        """

        NUM_STEPS = 500

        end_time = 1./frequency

        input_series = np.linspace(0., 2. * pi, NUM_STEPS)
        sin_series = np.sin(input_series)

        time_delta = end_time/NUM_STEPS

        base_sum = np.sum(np.abs(sin_series))
        filtered_sum = np.sum(np.abs([self._step(time_delta, value) for value in sin_series]))
        ratio = filtered_sum / base_sum

        print frequency, ratio

        return ratio


class LowPassFilterTestCase(unittest.TestCase, FilterTestBase):
    def setUp(self):
        resetTimeSourceForTestingPurposes(global_time)
        self.filter = LowPassFilter(1., 0.8)
        self.filter.update(0.)

    def test_passes_low_frequencies(self):
        self.assertAlmostEqual(1.0, self._percent_passed(1.e-8))

    def test_cuts_high_frequencies(self):
        self.assertAlmostEqual(0.0, self._percent_passed(1.e8))


class HighPassFilterTestCase(unittest.TestCase, FilterTestBase):
    def setUp(self):
        resetTimeSourceForTestingPurposes(global_time)
        self.filter = HighPassFilter(1., 0.8)
        self.filter.update(0.)

    def test_cuts_low_frequencies(self):
        self.assertAlmostEqual(0., self._step(1.e15, 20.))

    def test_passes_high_frequencies(self):
        self.assertAlmostEqual(10., self._step(1.e-15, 10.))

class ZPKFilterTestCase(unittest.TestCase, FilterTestBase):
    def setUp(self):
        resetTimeSourceForTestingPurposes(global_time)
        self.filter = ZPKFilter()


if __name__ == '__main__':
    unittest.main()

