import unittest

from pid_controller import PidController


class PidControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.pid = PidController(0.2, 0.02, 0.1, -5000, 5000)  # TODO: shrink these values once more realistic ones are known
    def tearDown(self):
        pass

    def testUpdateNoop(self):
        self.assertEquals(0, self.pid.update(.1, 0, 0))

    def testUpdateSmallPositiveError(self):
        self.assertTrue(0 < self.pid.update(.1, .1, 0))

    def testUpdateSmallNegativeError(self):
        self.assertTrue(0 > self.pid.update(.1, -.1, 0))

    def testUpdatePTerm(self):
        self.pid.ki = 0
        self.pid.kd = 0
        small = self.pid.update(.1, .1, 0)
        large = self.pid.update(.1, 2, 0)
        self.assertTrue(small < large)

    def testUpdateDTerm(self):
        self.pid.kp = 0
        self.pid.ki = 0
        large = self.pid.update(.1, .1, 0)
        self.pid.error_1 = .2
        small = self.pid.update(.1, .1, 0)
        self.assertTrue(small < large)

    def testUpdateITerm(self):
        self.pid.kp = 0
        self.pid.kd = 0
        small = self.pid.update(.1, .1, 0)
        large = self.pid.update(.1, .1, 0)
        self.assertTrue(small < large)

    def testZeroTimeUpdates(self):
        self.assertEquals(0, self.pid.update(0, 5, 5))  # 5 5 here should be inconsequential
        self.pid.prev_response = 3
        self.assertEquals(3, self.pid.update(0, 10, 0))  # ditto 10 0 here

    def testNanGetsSanitized(self):
        try:
            self.pid.update(float("nan"), 1, 2)
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("cannot be NaN" in str(error))

        try:
            self.pid.update(.1, float("nan"), 2)
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("cannot be NaN" in str(error))

        try:
            self.pid.update(.1, .1, float("nan"))
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("cannot be NaN" in str(error))

    def testMeasurementOutOfSoftRangeError(self):
        self.pid.soft_min = -1
        self.pid.soft_max = 1
        try:
            self.pid.update(.1, 0, -5)  # should error even though 0 is in range because -5 is not
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("Measured position out of soft range!" in str(error))

        try:
            self.pid.update(.1, 0, 5)  # should error even though 0 is in range because 5 is not
            self.assertTrue(False)
        except ValueError as error:
            self.assertTrue("Measured position out of soft range!" in str(error))

        # The good case where the measurement is not out of range is covered by other tests

if __name__ == '__main__':
    unittest.main()

