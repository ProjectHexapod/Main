import unittest

from math_utils import *


class MathUtilsTestCase(unittest.TestCase):

    def setUp(self):
        installArrayTypeEqualityFunction(self)        

    def tearDown(self):
        pass
    
    def testSymmetricSaturatePassesThrough(self):
        limit = 10.0
        for x in [-9.9, -5.0, 0.0, 2.0, 9.999]:
            self.assertEqual(x, saturate(x, limit))
            
    def testSymmetricSaturateLimitsLowValues(self):
        limit = 10.0
        for x in [-10.1, -11.0, -9e9]:
            self.assertEqual(-limit, saturate(x, limit))
            
    def testSymmetricSaturateLimitsHighValues(self):
        limit = 10.0
        for x in [10.1, 12.3, 5.3e6]:
            self.assertEqual(limit, saturate(x, limit))

    def testAsymmetricSaturatePassesThrough(self):
        l_limit = -5.0
        u_limit = 7.0
        for x in [-4.9, -1.0, 0.0, 2.0, 6.999]:
            self.assertEqual(x, saturate(x, l_limit, u_limit))
            
    def testAsymmetricSaturateLimitsLowValues(self):
        l_limit = -5.0
        u_limit = 7.0
        for x in [-5.1, -11.0, -9e9]:
            self.assertEqual(l_limit, saturate(x, l_limit, u_limit))
            
    def testAsymmetricSaturateLimitsHighValues(self):
        l_limit = -5.0
        u_limit = 7.0
        for x in [7.1, 12.3, 5.3e6]:
            self.assertEqual(u_limit, saturate(x, l_limit, u_limit))
    
    def testArraysAreEqual(self):
        self.assertTrue(arraysAreEqual(array([.2, .5, -1e4]),
                                       array([.2, .5, -1e4])))
        self.assertTrue(arraysAreEqual(array([.2, .5 + 1e-10, -1e4]),
                                       array([.2, .5, -1e4])))
        self.assertTrue(arraysAreEqual(array([.2, .5 - 1e-10, -1e4]),
                                       array([.2, .5, -1e4])))
        self.assertTrue(arraysAreEqual(array([.2 + 1e-10, .5 - 1e-10, -1e4]),
                                       array([.2 - 1e-10, .5, -1e4])))
        
        self.assertFalse(arraysAreEqual(array([1e-8, 0.0, 0.0]),
                                        array([0.0, 0.0, 0.0])))
        self.assertFalse(arraysAreEqual(array([0.0, 1e-8, 0.0]),
                                        array([0.0, 0.0, 0.0])))
        self.assertFalse(arraysAreEqual(array([0.0, 0.0, 1e-8]),
                                        array([0.0, 0.0, 0.0])))
    
    def testRotateXDoesntChangeX(self):
        self.assertEqual(array([1.0, 0.0, 0.0]),
                         rotateX(array([1.0, 0.0, 0.0]), pi_2))
        
    def testRotateXChangesYToZ(self):
        self.assertEqual(array([0.0, 0.0, 1.0]),
                         rotateX(array([0.0, 1.0, 0.0]), pi_2))
        
    def testRotateXChangesZToNegY(self):
        self.assertEqual(array([0.0, -1.0, 0.0]),
                         rotateX(array([0.0, 0.0, 1.0]), pi_2))
        
    def testRotateXOffAxis(self):
        self.assertEqual(
                   array([2.0, (-3.0 + 1.0) / 2.0 ** 0.5, (3.0 + 1.0) / 2.0 ** 0.5]),
                   rotateX(array([2.0, -3.0, 1.0]), -pi_4))
    
    def testRotateYChangesXToNegZ(self):
        self.assertEqual(array([0.0, 0.0, -1.0]),
                         rotateY(array([1.0, 0.0, 0.0]), pi_2))
        
    def testRotateYDoesntChangeY(self):
        self.assertEqual(array([0.0, 1.0, 0.0]),
                         rotateY(array([0.0, 1.0, 0.0]), pi_2))
        
    def testRotateYChangesZToX(self):
        self.assertEqual(array([1.0, 0.0, 0.0]),
                         rotateY(array([0.0, 0.0, 1.0]), pi_2))
        
    def testRotateYOffAxis(self):
        self.assertEqual(
                   array([(2.0 - 1.0) / 2.0 ** 0.5, -3.0, (2.0 + 1.0) / 2.0 ** 0.5]),
                   rotateY(array([2.0, -3.0, 1.0]), -pi_4))

    def testRotateZChangesXToY(self):
        self.assertEqual(array([0.0, 1.0, 0.0]),
                         rotateZ(array([1.0, 0.0, 0.0]), pi_2))
        
    def testRotateZChangesYToNegX(self):
        self.assertEqual(array([-1.0, 0.0, 0.0]),
                         rotateZ(array([0.0, 1.0, 0.0]), pi_2))
        
    def testRotateZDoesntChangeZ(self):
        self.assertEqual(array([0.0, 0.0, 1.0]),
                         rotateZ(array([0.0, 0.0, 1.0]), pi_2))
        
    def testRotateZOffAxis(self):
        self.assertEqual(
                   array([(2.0 - 3.0) / 2.0 ** 0.5, (-2.0 - 3.0) / 2.0 ** 0.5, 1.0]),
                   rotateZ(array([2.0, -3.0, 1.0]), -pi_4))


if __name__ == '__main__':
    unittest.main()
