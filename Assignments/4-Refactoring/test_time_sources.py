import unittest

from time_sources import TimeSource


class TimeSourceTestCase(unittest.TestCase):
    def setUp(self):
        self.ts = TimeSource()
    def tearDown(self):
        pass

    # Side effect: tests getTime() and getDelta()
    def check(self, time, delta, ts=None):
        if ts is None:
            ts = self.ts
        self.assertEqual(time, ts.getTime())
        self.assertEqual(delta, ts.getDelta())
    
    def testDefaultsToZeros(self):
        self.check(0.0, 0.0)
    
    def testInitialTime(self):
        ts = TimeSource(1.234, 0.036)
        self.check(1.234, 0.036, ts)
    
    def testUpdateTime(self):
        self.ts.updateTime(0.1)
        self.check(0.1, 0.1)
        self.ts.updateTime(0.33)
        self.check(0.33, 0.23)
        
    def testUpdateDelta(self):
        self.ts.updateDelta(0.1)
        self.check(0.1, 0.1)
        self.ts.updateDelta(0.45)
        self.check(0.55, 0.45)


if __name__ == '__main__':
    unittest.main()
