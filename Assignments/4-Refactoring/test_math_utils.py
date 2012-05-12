import unittest
from scipy import array, pi

from math_utils import *


class MathUtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    def testArraysAreEqual(self):
        self.assertTrue(arraysAreEqual(array([.2, .5, -1e4]),
                                       array([.2, .5, -1e4])))
        self.assertTrue(arraysAreEqual(array([.2, .5+1e-10, -1e4]),
                                       array([.2, .5, -1e4])))
        self.assertTrue(arraysAreEqual(array([.2, .5-1e-10, -1e4]),
                                       array([.2, .5, -1e4])))
        self.assertTrue(arraysAreEqual(array([.2+1e-10, .5-1e-10, -1e4]),
                                       array([.2-1e-10, .5, -1e4])))
        
        self.assertFalse(arraysAreEqual(array([1e-8, 0.0, 0.0]),
                                        array([0.0, 0.0, 0.0])))
        self.assertFalse(arraysAreEqual(array([0.0, 1e-8, 0.0]),
                                        array([0.0, 0.0, 0.0])))
        self.assertFalse(arraysAreEqual(array([0.0, 0.0, 1e-8]),
                                        array([0.0, 0.0, 0.0])))
    
    def testRotateYChangesXToNegZ(self):
        self.assertTrue(arraysAreEqual(array([0.0, 0.0, -1.0]),
                                       rotateY(array([1.0, 0.0, 0.0]), pi/2.0)))
    def testRotateYDoesntChangeY(self):
        self.assertTrue(arraysAreEqual(array([0.0, 1.0, 0.0]),
                                       rotateY(array([0.0, 1.0, 0.0]), pi/2.0)))
    def testRotateYChangesZToX(self):
        self.assertTrue(arraysAreEqual(array([1.0, 0.0, 0.0]),
                                       rotateY(array([0.0, 0.0, 1.0]), pi/2.0)))
    def testRotateYOffAxis(self):
        self.assertTrue(arraysAreEqual(
                   array([(2.0 - 1.0)/2.0**0.5, -3.0, (2.0 + 1.0)/2.0**0.5]),
                   rotateY(array([2.0, -3.0, 1.0]), -pi/4.0)))

    def testRotateZChangesXToY(self):
        self.assertTrue(arraysAreEqual(array([0.0, 1.0, 0.0]),
                                       rotateZ(array([1.0, 0.0, 0.0]), pi/2.0)))
    def testRotateZChangesYToNegX(self):
        self.assertTrue(arraysAreEqual(array([-1.0, 0.0, 0.0]),
                                       rotateZ(array([0.0, 1.0, 0.0]), pi/2.0)))
    def testRotateZDoesntChangeZ(self):
        self.assertTrue(arraysAreEqual(array([0.0, 0.0, 1.0]),
                                       rotateZ(array([0.0, 0.0, 1.0]), pi/2.0)))
    def testRotateZOffAxis(self):
        self.assertTrue(arraysAreEqual(
                   array([(2.0 - 3.0)/2.0**0.5, (-2.0 - 3.0)/2.0**0.5, 1.0]),
                   rotateZ(array([2.0, -3.0, 1.0]), -pi/4.0)))


if __name__ == '__main__':
    unittest.main()

