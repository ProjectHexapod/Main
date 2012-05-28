import unittest
from math_utils import *
import math
from time_sources import global_time, resetTimeSourceForTestingPurposes

from pid_controller import HystereticPeakDetector

class PeakDetectorTestCase(unittest.TestCase):
    def setUp(self):
        installArrayTypeEqualityFunction(self)
        
        resetTimeSourceForTestingPurposes(global_time)
        self.hpd = HystereticPeakDetector(0.0, -1.0, 1.0, 2.0)
    def tearDown(self):
        pass
    
    def testRisingEdgeDetectionFromInit(self):
        risingsequence=[float(i)/10 for i in range(25)]
        for element in risingsequence:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertEquals(self.hpd.getEdgeType(), self.hpd.RISING_EDGE)
    
    def testFallingEdgeDetection(self):
        fallingsequence=[-float(i)/10 for i in range(25)]
        for element in fallingsequence:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertEquals(self.hpd.getEdgeType(), self.hpd.FALLING_EDGE)
    
    def testRisingEdgeDetectionComplex(self):
        #sin from 0 to 6.5 pi
        sinEndsRising=[2.5*sin(math.pi*float(i)/4) for i in range(27)]
        for element in sinEndsRising:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertEquals(self.hpd.getEdgeType(), self.hpd.RISING_EDGE)
    
    def testFallingEdgeDetectionComplex(self):
        #-sin from 0 to 6.5 pi
        sinEndsFalling=[-2.5*sin(math.pi*float(i)/4) for i in range(27)]
        for element in sinEndsFalling:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertEquals(self.hpd.getEdgeType(), self.hpd.FALLING_EDGE)
    
    def testRisingEdgeHysteresis(self):
        #tests that a falling edge which does not hit hysteretic
        #limits is not detected
        two_cycle_rising=[-2.5*sin(math.pi*float(i)/10 ) for i in range(16)]
        short_falling_edge=[ (2.5-float(i)/20) for i in range(10)]
        two_cycle_rising.extend(short_falling_edge)
        for element in two_cycle_rising:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertEquals(self.hpd.getEdgeType(), self.hpd.RISING_EDGE)
    
    def testFallingEdgeHysteresis(self):
        #tests that a rising edge which does not hit hysteretic
        #limits is not detected
        
        #sine with falling edge at end
        two_cycle_falling=[2.5*sin(math.pi*float(i)/10 ) for i in range(16)]
        short_rising_edge=[ -(2.5-float(i)/20) for i in range(10)]
        two_cycle_falling.extend(short_rising_edge)
        for element in two_cycle_falling:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertEquals(self.hpd.getEdgeType(), self.hpd.FALLING_EDGE)
    
    def testConvergingDetection(self):
        converging_sequence=[(11-float(i)/4)*sin(math.pi*float(i)/10) 
                    for i in range(41)]
        for element in converging_sequence:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertTrue( self.hpd.isConverging() )
    
    def testLimitCycleDetection(self):
        lc_sequence=[2.5*sin(math.pi*float(i)/10) 
                    for i in range(41)]
        for element in lc_sequence:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertTrue( self.hpd.isLimitCycle() )
    
    def testInstabilityDetection(self):
        unstable_sequence=[float(i)/4*sin(math.pi*float(i)/10) 
                    for i in range(41)]
        for element in unstable_sequence:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertTrue( self.hpd.isUnstable() )
    
    def testConvergenceDetection(self):
        convergent_sequence=[(2.5-float(i)/50)*sin(math.pi*float(i)/10) 
                    for i in range(101) ]
        for element in convergent_sequence:
            global_time.updateDelta(0.1)
            self.hpd.update(element)
        self.assertTrue( self.hpd.hasConverged() )
