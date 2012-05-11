import unittest
from scipy import arange, pi, sin

from leg_controller import LegController


class LegControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.leg = LegController()
    def tearDown(self):
        pass
    
    def testShockDepthThredholdsAreSane(self):
        l = self.leg
        self.assertGreater(l.SHOCK_DEPTH_THRESHOLD_HIGH, 0.0)
        self.assertGreater(l.SHOCK_DEPTH_THRESHOLD_LOW, 0.0)
        self.assertGreater(l.SHOCK_DEPTH_THRESHOLD_HIGH, l.SHOCK_DEPTH_THRESHOLD_LOW)
    def testFootOnGroundDefaultsToFalse(self):
        self.assertFalse(self.leg.isFootOnGround())
    def testFootOnGroundTurnsOn(self):
        l = self.leg
        for sd in arange(0.0, 0.1, 0.001):
            l.setLegState(0.0, 0.0, 0.0, sd)
            l.updateFootOnGround()
            self.assertEqual(sd > l.SHOCK_DEPTH_THRESHOLD_HIGH, l.isFootOnGround())
    def testFootOnGroundTurnsOff(self):
        l = self.leg
        for sd in arange(0.1, 0.0, -0.001):
            l.setLegState(0.0, 0.0, 0.0, sd)
            l.updateFootOnGround()
            self.assertEqual(sd > l.SHOCK_DEPTH_THRESHOLD_LOW, l.isFootOnGround())
    def testFootOnGroundNoiseImmunity(self):
        l = self.leg
        
        time = arange(0.0, 1.0, 0.001)
        amp = (l.SHOCK_DEPTH_THRESHOLD_HIGH - l.SHOCK_DEPTH_THRESHOLD_LOW - 0.001) / 2.0
        offset = (l.SHOCK_DEPTH_THRESHOLD_HIGH + l.SHOCK_DEPTH_THRESHOLD_LOW) / 2.0
        shock_depth = amp * sin(2*pi*time * 10.0) + offset

        l.setLegState(0.0, 0.0, 0.0, 0.0)
        l.updateFootOnGround()
        for sd in shock_depth:
            l.setLegState(0.0, 0.0, 0.0, sd)
            l.updateFootOnGround()
            self.assertFalse(l.isFootOnGround())

        l.setLegState(0.0, 0.0, 0.0, l.SHOCK_DEPTH_THRESHOLD_HIGH * 2.0)
        l.updateFootOnGround()
        for sd in shock_depth:
            l.setLegState(0.0, 0.0, 0.0, sd)
            l.updateFootOnGround()
            self.assertTrue(l.isFootOnGround())


if __name__ == '__main__':
    unittest.main()

