import unittest

from time_sources import TimeSource, StopWatch


# Side effect: tests getTime() and getDelta()
def check(test_case, ts, time, delta):
    test_case.assertAlmostEqual(time, ts.getTime())
    test_case.assertAlmostEqual(delta, ts.getDelta())


class TimeSourceTestCase(unittest.TestCase):
    def setUp(self):
        self.ts = TimeSource()
    def tearDown(self):
        pass

    def testDefaultsToZeros(self):
        check(self, self.ts, 0.0, 0.0)
    
    def testInitialTime(self):
        ts = TimeSource(1.234, 0.036)
        check(self, ts, 1.234, 0.036)
    
    def testUpdateTime(self):
        self.ts.updateTime(0.1)
        check(self, self.ts, 0.1, 0.1)
        self.ts.updateTime(0.33)
        check(self, self.ts, 0.33, 0.23)
    def testUpdateTimeAlwaysIncreasesTime(self):
        self.assertRaises(ValueError, self.ts.updateTime, 0.0)
        self.assertRaises(ValueError, self.ts.updateTime, -0.1)
        
    def testUpdateDelta(self):
        self.ts.updateDelta(0.1)
        check(self, self.ts, 0.1, 0.1)
        self.ts.updateDelta(0.45)
        check(self, self.ts, 0.55, 0.45)
    def testUpdateDeltaAlwaysIncreasesTime(self):
        self.assertRaises(ValueError, self.ts.updateDelta, 0.0)
        self.assertRaises(ValueError, self.ts.updateDelta, -0.1)


class StopWatchTestCase(unittest.TestCase):
    def setUp(self):
        self.ts = TimeSource()
        self.ts.updateTime(6.0)
        self.ts.updateDelta(0.1)
        self.lts = StopWatch(self.ts)
    def tearDown(self):
        pass
    
    def testStartsCountingFromZero(self):
        check(self, self.lts, 0.0, 0.1)
    
    def testUpdatesLocalTime(self):
        self.lts.getTime()  # Cause an update of cached data
        self.ts.updateDelta(0.3)
        self.ts.updateDelta(0.2)
        check(self, self.lts, 0.5, 0.5)
        self.ts.updateDelta(0.1)
        check(self, self.lts, 0.6, 0.1)


if __name__ == '__main__':
    unittest.main()
