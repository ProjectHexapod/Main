import unittest
from math_utils import *

from leg_controller import LegController


class LegControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.leg = LegController()
        self.leg_state = [array([0.0, 0.0, 0.0]), 0.0]
    def tearDown(self):
        pass

    def testLinkLengthsAreSane(self):
        l = self.leg
        self.assertGreater(l.YAW_LEN, 0.0)
        self.assertGreater(l.THIGH_LEN, 0.0)
        self.assertGreater(l.CALF_LEN, 0.0)
        
        # Thigh should be 5ish times as long as the yaw stub
        self.assertLess(abs(l.THIGH_LEN / l.YAW_LEN - 5.0), 2.0)
        # Thigh should be pretty much the same length as the calf
        self.assertLess(abs(l.THIGH_LEN / l.CALF_LEN - 1.0), 0.3)
    
    def testFootPosFromLegStateZeroAnglesIsSumOfLengthsInX(self):
        l = self.leg
        self.assertTrue(arraysAreEqual(
                array([l.YAW_LEN + l.THIGH_LEN + l.CALF_LEN, 0.0, 0.0]),
                l.footPosFromLegState(self.leg_state)))
    def testFootPosFromLegStatePosRightAngles(self):
        l = self.leg
        
        self.leg_state[0][YAW] = pi_2
        self.assertTrue(arraysAreEqual(
                array([0.0, -(l.YAW_LEN + l.THIGH_LEN + l.CALF_LEN), 0.0]),
                l.footPosFromLegState(self.leg_state)))
        
        self.leg_state[0][HP] = pi_2
        self.assertTrue(arraysAreEqual(
                array([0.0, -l.YAW_LEN, -(l.THIGH_LEN + l.CALF_LEN)]),
                l.footPosFromLegState(self.leg_state)))
        
        self.leg_state[0][KP] = pi_2
        self.assertTrue(arraysAreEqual(
                array([0.0, l.CALF_LEN - l.YAW_LEN, -l.THIGH_LEN]),
                l.footPosFromLegState(self.leg_state)))
    def testFootPosFromLegStateShockDepthModifiesCalfLen(self):
        l = self.leg
        self.leg_state[0][KP] = pi_2
        self.leg_state[1] = 0.1234
        self.assertTrue(arraysAreEqual(
                array([l.YAW_LEN + l.THIGH_LEN, 0.0, -(l.CALF_LEN - 0.1234)]),
                l.footPosFromLegState(self.leg_state)))
    def testFootPosFromLegStateComplex(self):
        l = self.leg
        
        self.leg_state[0][YAW] = -pi_4
        self.assertTrue(arraysAreEqual(
                array([(l.YAW_LEN + l.THIGH_LEN + l.CALF_LEN) / 2**0.5,
                       (l.YAW_LEN + l.THIGH_LEN + l.CALF_LEN) / 2**0.5,
                       0.0]),
                l.footPosFromLegState(self.leg_state)))
        
        self.leg_state[0][HP] = -pi / 6.0
        self.assertTrue(arraysAreEqual(
            array([(l.YAW_LEN + (l.THIGH_LEN + l.CALF_LEN) * 3.0**0.5/2.0) / 2**0.5,
                   (l.YAW_LEN + (l.THIGH_LEN + l.CALF_LEN) * 3.0**0.5/2.0) / 2**0.5,
                   (l.THIGH_LEN + l.CALF_LEN) / 2.0]),
            l.footPosFromLegState(self.leg_state)))
        
        self.leg_state[0][KP] = pi / 6.0
        self.assertTrue(arraysAreEqual(
            array([(l.YAW_LEN + l.THIGH_LEN * 3.0**0.5/2.0 + l.CALF_LEN) / 2**0.5,
                   (l.YAW_LEN + l.THIGH_LEN * 3.0**0.5/2.0 + l.CALF_LEN) / 2**0.5,
                   l.THIGH_LEN / 2.0]),
            l.footPosFromLegState(self.leg_state)))
            
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
