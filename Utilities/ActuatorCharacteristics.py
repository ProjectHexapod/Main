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
    def __init__(self, bore_diameter, rod_diameter, act_retracted_len, act_extended_len, pivot1_dist_from_joint, pivot2, axis, ang_offset, system_pressure):
        self.BORE_DIAMETER          = bore_diameter
        self.ROD_DIAMETER           = rod_diameter
        self.ACT_RETRACTED_LEN      = act_retracted_len
        self.ACT_EXTENDED_LEN       = act_extended_len
        # The placement of these pivots indicate the placement of the actuator anchors
        # when the joint is in the fully retracted position.  This makes ACT_RETRACTED_LEN
        # redundant
        self.PIVOT1_DIST_FROM_JOINT = pivot1_dist_from_joint
        self.PIVOT2                 = pivot2
        self.AXIS                   = axis
        self.ANG_OFFSET             = ang_offset
        self.SYSTEM_PRESSURE        = system_pressure
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


class ActuatorMathHelper(ActuatorCharacteristics):
    def __init__(self, *args, **kwargs):
        super(ActuatorMathHelper, self).__init__(*args, **kwargs)
        self.setActuatorAnchors( self.PIVOT1_DIST_FROM_JOINT, self.PIVOT2[0], self.PIVOT2[1] )
        self.setExtendCrossSection(  pi *  (self.BORE_DIAMETER/2)**2 )
        self.setRetractCrossSection( pi * ((self.BORE_DIAMETER/2)**2 - (self.ROD_DIAMETER/2)**2) )
    def setActuatorAnchors( self, a1_x, a2_x, a2_y ):
        self.a1_x = a1_x
        self.a2_x = a2_x
        self.a2_y = a2_y
    def setAngle( self, ang ):
        """
        Set the angle from which we are calculating our lengths
        """
        self.ang_from_max_retraction = ang - self.ANG_OFFSET
    def setAngleRate( self, rate ):
        self.ang_rate = rate
    def getLength( self ):
        a = self.getActPath()
        return len2(a)
    def getLengthRate( self ):
        arate = self.ang_rate
        larm  = self.getLeverArm()
        return arate*larm
    def setCrossSection( self, area ):
        self.setExtendCrossSection(area)
        self.setRetractCrossSection(area)
    def setMaxHydraulicFlow( self, new_max ):
        self.max_extend_rate  = new_max/self.extend_cross_section
        self.max_retract_rate = -new_max/self.retract_cross_section
    def setExtendCrossSection( self, area ):
        self.extend_cross_section = area
    def setRetractCrossSection( self, area ):
        self.retract_cross_section = area
    def getActPath( self ):
        """
        Return the path of the actuator in the hinge plane
        """
        # Apply joint rotation to one anchor
        ang = self.ang_from_max_retraction
        # Get the angle of the actuator with the horizontal
        act = rot2( (self.a2_x, self.a2_y), ang )
        act = (act[0] - self.a1_x, act[1])
        return act
    def getLeverArm( self ):
        act = self.getActPath()
        h_ang = pi-atan2(act[1], act[0])
        # Get the lever arm
        l_arm = sin(h_ang)*self.a1_x
        return l_arm
    def __force_to_torque( self, force ):
        """
        Give the max applicable torque at the present orientation
        given an actuator force
        """
        return self.getLeverArm()*force
    def __torque_to_force( self, torque ):
        return torque/self.getLeverArm()
    def setForceLimit( self, f ):
        self.setExtendForceLimit( f )
        self.setRetractForceLimit( f )
    def setExtendForceLimit( self, f ):
        self.extend_force_limit = f
    def getExtendForceLimit( self ):
        return self.extend_force_limit
    def getRetractForceLimit( self ):
        return self.retract_force_limit
    def setRetractForceLimit( self, f ):
        self.retract_force_limit = f
    def setTorqueLimit( self, l ):
        print 'Cannot set torque limit on linear actuator controlled hinge'
    def getTorqueLimit( self ):
        """The torque limit is directional depending on what side of the piston
        is being driven.  This is dependent on which way we are pressurizing the
        piston, not which way it's presently moving"""
        #FIXME: THIS ASSUMES WE ARE USING THE JOINT'S ANG_TARGET PARAMETER,
        # WHICH WE OFTEN ARE NOT
        if self.getAngleError()>0:
            return abs(self.getLeverArm()*self.extend_force_limit)
        else:
            return abs(self.getLeverArm()*self.retract_force_limit)

