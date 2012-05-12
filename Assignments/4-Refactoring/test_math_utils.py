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
    

if __name__ == '__main__':
    unittest.main()

