import unittest

from time_sources import global_time
from pid_controller import PidController


class PidControllerTestCase(unittest.TestCase):
    def setUp(self):
        global_time.reset()
        self.pid = PidController(0.2, 0.02, 0.1, -5000, 5000)  # TODO: shrink these values once more realistic ones are known
    def tearDown(self):
        pass

    def testUpdateNoop(self):
        global_time.updateDelta(0.1)
        self.assertEquals(0, self.pid.update(0, 0))

    def testUpdateSmallPositiveError(self):
        global_time.updateDelta(0.1)
        self.assertTrue(0 < self.pid.update(.1, 0))

    def testUpdateSmallNegativeError(self):
        global_time.updateDelta(0.1)
        self.assertTrue(0 > self.pid.update(-.1, 0))

    def testUpdatePTerm(self):
        self.pid.ki = 0
        self.pid.kd = 0
        global_time.updateDelta(0.1)
        small = self.pid.update(.1, 0)
        global_time.updateDelta(0.1)
        large = self.pid.update(2, 0)
        self.assertTrue(small < large)

    def testUpdateDTerm(self):
        self.pid.kp = 0
        self.pid.ki = 0
        global_time.updateDelta(0.1)
        large = self.pid.update(.1, 0)
        self.pid.error_1 = .2
        global_time.updateDelta(0.1)
        small = self.pid.update(.1, 0)
        self.assertTrue(small < large)

    def testUpdateITerm(self):
        self.pid.kp = 0
        self.pid.kd = 0
        global_time.updateDelta(0.1)
        small = self.pid.update(.1, 0)
        global_time.updateDelta(0.1)
        large = self.pid.update(.1, 0)
        self.assertTrue(small < large)

    def testZeroTimeUpdates(self):
        global_time.updateDelta(0.0)
        self.assertEquals(0, self.pid.update(5, 5))  # 5 5 here should be inconsequential
        self.pid.prev_response = 3
        global_time.updateDelta(0.0)
        self.assertEquals(3, self.pid.update(10, 0))  # ditto 10 0 here

    def testNanGetsSanitized(self):
        try:
            self.pid.update(float("nan"), 2)
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("cannot be NaN" in str(error))

        try:
            self.pid.update(.1, float("nan"))
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("cannot be NaN" in str(error))

    def testMeasurementOutOfSoftRangeError(self):
        self.pid.soft_min = -1
        self.pid.soft_max = 1
        try:
            global_time.updateDelta(0.1)
            self.pid.update(0, -5)  # should error even though 0 is in range because -5 is not
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("Measured position out of soft range!" in str(error))

        try:
            global_time.updateDelta(0.1)
            self.pid.update(0, 5)  # should error even though 0 is in range because 5 is not
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("Measured position out of soft range!" in str(error))

        # The good case where the measurement is not out of range is covered by other tests

    def testSetPointCappedToSoftRange(self):
        self.pid.soft_min = -1
        self.pid.soft_max = 1
        global_time.updateDelta(0.1)
        first = self.pid.update(10, 0)
        self.pid.prev_error = 0
        self.pid.integral_error_accumulator = 0
        second = self.pid.update(1, 0)
        self.assertEquals(first, second)

        self.pid.prev_error = 0
        self.pid.integral_error_accumulator = 0
        first = self.pid.update(-10, 0)
        self.pid.prev_error = 0
        self.pid.integral_error_accumulator = 0
        global_time.updateDelta(0.1)
        second = self.pid.update(-1, 0)
        self.assertEquals(first, second)


if __name__ == '__main__':
    unittest.main()

