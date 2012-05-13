import unittest

from pid_controller import PidController


class PidControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.pid = PidController(0.2, 0.02, 0.1)
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

if __name__ == '__main__':
    unittest.main()

