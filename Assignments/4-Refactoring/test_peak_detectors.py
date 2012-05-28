import unittest
from math_utils import *
import math
from time_sources import global_time, resetTimeSourceForTestingPurposes

from leg_controller import LegController


class PeakDetectorTestCase(unittest.TestCase):
    def setUp(self):
        installArrayTypeEqualityFunction(self)
        
        self.pd = HystereticPeakDetector(0.0, 0.0, 0.0, 1)
    def tearDown(self):
        pass
	
	def testRisingEdgeDetection(self):
		pass
	
	def testFallingEdgeDetection(self):
		pass
	
	def testRisingEdgeHysteresis(self):
		pass
	
	def testFallingEdgeHysteresis(self):
		pass
	
	def testConvergingDetection(self):
		pass
	
	def testLimitCycleDetection(self):
		pass
	
	def testInstabilityDetection(self):
		pass
	
	def testConvergenceDetection(self):
		pass
