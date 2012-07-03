from math import *
from SimulationKit.helpers import *

# Convenience multipliers...
deg2rad    = pi/180
psi2pascal = 6894.76
inch2meter = 2.54e-2
pound2kilo = 0.455
gallon2cmps = 1/15850.4

class ActuatorCharacteristics(object):
    """
    This describes the placement of a linear actuator relative to the joint it
    is controlling.  It also provides convenience trig functions for figuring
    out things like joint limits based on actuator extension.
    """
    def __init__(self):
        self.BORE_DIAMETER          = 0.0
        self.ROD_DIAMETER           = 0.0
        self.ACT_RETRACTED_LEN      = 0.1
        self.ACT_EXTENDED_LEN       = 0.1
        self.PIVOT1_DIST_FROM_JOINT = 0.1
        self.PIVOT2                 = (0.0,0.0)
        self.AXIS                   = (0,0,1)
        self.ANG_OFFSET             = 0.0
        self.SYSTEM_PRESSURE        = 2000*psi2pascal
    def getRangeOfMotion( self ):
        """Returns an angle in radians"""
        assert abs(len2(self.PIVOT2)-self.PIVOT1_DIST_FROM_JOINT) <\
            self.ACT_RETRACTED_LEN, 'You can retract in to singularity'
        retracted_angle = thetaFromABC(\
            self.PIVOT1_DIST_FROM_JOINT,\
            len2(self.PIVOT2),\
            self.ACT_RETRACTED_LEN)
        assert len2(self.PIVOT2)+self.PIVOT1_DIST_FROM_JOINT >\
            self.ACT_EXTENDED_LEN, 'You can extend in to singularity'
        extended_angle = thetaFromABC(\
            self.PIVOT1_DIST_FROM_JOINT,\
            len2(self.PIVOT2),\
            self.ACT_EXTENDED_LEN)
        assert extended_angle>retracted_angle, \
            "This actuator placement breaks sign conventions\
            ... actuator extend should increase joint angle"
        return extended_angle - retracted_angle
    def getExtensionCrossSectionM2( self ):
        """Returns piston cross sectional area in m^2 on the extend side of the
        piston"""
        return ((self.BORE_DIAMETER/2)**2)*pi
    def getRetractionCrossSectionM2( self ):
        """Returns piston cross sectional area in m^2 on the extend side of the
        piston"""
        return ((self.BORE_DIAMETER/2)**2-(self.ROD_DIAMETER/2)**2)*pi
    def getMaxExtensionForceNewtons( self ):
        """Pressure is in Newtons/sq. meter.  Returned force is in Newtons"""
        return self.getExtensionCrossSectionM2()*self.SYSTEM_PRESSURE
    def getMaxRetractionForceNewtons( self, pressure = 0.0 ):
        """Pressure is in Newtons/sq. meter.  Returned force is in Newtons"""
        return self.getRetractionCrossSectionM2()*self.SYSTEM_PRESSURE

