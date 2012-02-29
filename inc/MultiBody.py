import ode
from math import *
from helpers import *

def calcAngularError( a1, a2 ):
    """Given two angles in radians what is 
	the difference between them?"""
    error = (a1%(2*pi))-(a2%(2*pi))
    if error > pi:
        error -= 2*pi
    elif error <= -1*pi:
        error += 2*pi
    return error

class ControlledHingeJoint(ode.HingeJoint):
    """ControlledHingeJoint lets you set target positions and gives you
    torque feedback"""
    def __init__(self, world=None):
        ode.HingeJoint.__init__(self, world)
        self.setFeedback(True)
        self.setAngleTarget(0.0)
        self.setTorqueLimit(0.0)
        self.setGain(1.0)
    def getTorque( self ):
        """Return the torque being exerted by the motor
        Funny enough, this is not easy to obtain."""
        # feedback is 
        # ( body1Forces, body1torque, body2forces, body2torque )
        feedback = self.getFeedback()
        forces = feedback[0]
        torque = feedback[1]
        axis   = self.getAxis()
        body_COM = self.getBody(0).getPosition()
        anchor = sub3( body_COM, self.getAnchor() )
        # Figure out the torque due to the 
        # force contribution of the joint
        t_force = cross( forces, anchor )
        # Subtract the torque due to force contribution 
        # of joint from torque @ COM
        # to get joint torque
        t_joint = sub3(torque, t_force)
        # Figure out the projection of the torque on the axis
        return dot3( t_joint, norm3(axis) )
    def setAngleTarget( self, target ):
        self.angle_target = target
    def getAngleTarget( self ):
        return self.angle_target
    def setTorqueLimit( self, limit ):
        self.setParam(ode.ParamFMax, limit)
    def getTorqueLimit( self ):
        return self.getParam(ode.ParamFMax, limit)
    def setGain( self, gain ):
        self.gain = gain
    def getGain( self ):
        return self.gain
    def update( self ):
        """Do control"""
        error = calcAngularError( self.angle_target, self.getAngle() )
        self.setParam( ode.ParamVel, error*self.gain )

class MultiBody():
    def __init__(self, world, space, density, offset = (0.0, 0.0, 0.0)):
        """Creates a ragdoll of standard size at the given offset."""

        self.world            = world
        self.space            = space
        self.density          = density
        self.bodies           = []
        self.geoms            = []
        self.joints           = []
        self.totalMass        = 0.0
        self.update_callbacks = []

        # These are the inputs and outputs for our controller
        self.inputs  = {}
        self.outputs = {}

        self.offset = offset


        self.buildBody()

    def update( self ):
        for f,a,ka in self.update_callbacks:
            f(*a,**ka)

    def buildBody(self):
        """This is for the subclasses to define."""
        return

    def addBody(self, p1, p2, radius, mass=None):
        """
        Adds a capsule body between joint positions p1 and p2 and with given
        radius to the ragdoll.
        """

        p1 = add3(p1, self.offset)
        p2 = add3(p2, self.offset)

        # cylinder length not including endcaps, make capsules overlap by half
        #   radius at joints
        cyllen = dist3(p1, p2) - radius

        body = ode.Body(self.world)
        # This is our own stupid shit
        body.color = (0,128,0,255)
        m = ode.Mass()
        if mass == None:
            m.setCappedCylinder(self.density, 3, radius, cyllen)
        else:
            m.setCappedCylinderTotal(mass, 3, radius, cyllen)
        body.setMass(m)

        # set parameters for drawing the body
        body.shape = "capsule"
        body.length = cyllen
        body.radius = radius

        # create a capsule geom for collision detection
        geom = ode.GeomCCylinder(self.space, radius, cyllen)
        geom.setBody(body)

        # define body rotation automatically from body axis
        za = norm3(sub3(p2, p1))
        if (abs(dot3(za, (1.0, 0.0, 0.0))) < 0.7): xa = (1.0, 0.0, 0.0)
        else: xa = (0.0, 1.0, 0.0)
        ya = cross(za, xa)
        xa = norm3(cross(ya, za))
        ya = cross(za, xa)
        rot = (xa[0], ya[0], za[0], xa[1], ya[1], za[1], xa[2], ya[2], za[2])

        body.setPosition(mul3(add3(p1, p2), 0.5))
        body.setRotation(rot)

        self.bodies.append(body)
        self.geoms.append(geom)
        
        self.totalMass += body.getMass().mass

        return body

    def addSpringyCappedCylinder(self, p1, p2, radius, n_members=2, k_bend=1e5, k_torsion=1e5):
        """
        Adds a capsule body between joint positions p1 and p2 and with given
        radius to the ragdoll.
        Along the axis of the capsule distribute n_joints ball joints
        With spring constants given by k_bend and k_torsion
        TODO: FUNCTION NOT FINISHED  Wed 14 Dec 2011 06:06:24 PM EST   
        """

        p_start = p1 = add3(p1, self.offset)
        p_end = add3(p2, self.offset)
        iteration_jump = div3( sub3( p_end, p_start ), n_members )
        p2 = add3(p1, iteration_jump)

        for i in range(n_members):
            # cylinder length not including endcaps, make capsules overlap by half
            #   radius at joints
            cyllen = dist3(p1, p2) - radius

            body = ode.Body(self.world)
            m = ode.Mass()
            m.setCappedCylinder(self.density, 3, radius, cyllen)
            body.setMass(m)

            # set parameters for drawing the body
            body.shape = "capsule"
            body.length = cyllen
            body.radius = radius

            # create a capsule geom for collision detection
            geom = ode.GeomCCylinder(self.space, radius, cyllen)
            geom.setBody(body)

            # define body rotation automatically from body axis
            za = norm3(sub3(p2, p1))
            if (abs(dot3(za, (1.0, 0.0, 0.0))) < 0.7): xa = (1.0, 0.0, 0.0)
            else: xa = (0.0, 1.0, 0.0)
            ya = cross(za, xa)
            xa = norm3(cross(ya, za))
            ya = cross(za, xa)
            rot = (xa[0], ya[0], za[0], xa[1], ya[1], za[1], xa[2], ya[2], za[2])

            body.setPosition(mul3(add3(p1, p2), 0.5))
            body.setRotation(rot)

            self.bodies.append(body)
            self.geoms.append(geom)
            
            self.totalMass += body.getMass().mass

            if i != n_members:
                p1 = p2
                p2 = add3(p1, iteration_jump)


        return body

    def addFixedJoint(self, body1, body2):
        joint = ode.FixedJoint(self.world)
        joint.attach(body1, body2)
        joint.setFixed()

        joint.style = "fixed"
        self.joints.append(joint)

        return joint

    def addControlledHingeJoint(self, body1, body2, anchor, axis, loStop = -ode.Infinity,
        hiStop = ode.Infinity, torque_limit = 0.0, gain = 1.0):

        anchor = add3(anchor, self.offset)

        joint = ControlledHingeJoint( world = self.world )
        joint.setTorqueLimit( torque_limit )
        joint.setGain( gain )
        joint.attach(body1, body2)
        joint.setAnchor(anchor)
        joint.setAxis(axis)
        joint.setParam(ode.ParamLoStop, loStop)
        joint.setParam(ode.ParamHiStop, hiStop)

        joint.style = "hinge"
        self.joints.append(joint)

        return joint

    def addHingeJoint(self, body1, body2, anchor, axis, loStop = -ode.Infinity,
        hiStop = ode.Infinity):

        anchor = add3(anchor, self.offset)

        joint = ode.HingeJoint(self.world)
        joint.attach(body1, body2)
        joint.setAnchor(anchor)
        joint.setAxis(axis)
        joint.setParam(ode.ParamLoStop, loStop)
        joint.setParam(ode.ParamHiStop, hiStop)

        joint.style = "hinge"
        self.joints.append(joint)
        self.update_callbacks.append( (joint.update,[joint],{}) )

        return joint

    def addUniversalJoint(self, body1, body2, anchor, axis1, axis2,
        loStop1 = -ode.Infinity, hiStop1 = ode.Infinity,
        loStop2 = -ode.Infinity, hiStop2 = ode.Infinity):

        anchor = add3(anchor, self.offset)

        joint = ode.UniversalJoint(self.world)
        joint.attach(body1, body2)
        joint.setAnchor(anchor)
        joint.setAxis1(axis1)
        joint.setAxis2(axis2)
        joint.setParam(ode.ParamLoStop, loStop1)
        joint.setParam(ode.ParamHiStop, hiStop1)
        joint.setParam(ode.ParamLoStop2, loStop2)
        joint.setParam(ode.ParamHiStop2, hiStop2)

        joint.style = "univ"
        self.joints.append(joint)

        return joint

    def addBallJoint(self, body1, body2, anchor, baseAxis, baseTwistUp,
        flexLimit = pi, twistLimit = pi, flexForce = 0.0, twistForce = 0.0):

        anchor = add3(anchor, self.offset)

        # create the joint
        joint = ode.BallJoint(self.world)
        joint.attach(body1, body2)
        joint.setAnchor(anchor)

        # store the base orientation of the joint in the local coordinate system
        #   of the primary body (because baseAxis and baseTwistUp may not be
        #   orthogonal, the nearest vector to baseTwistUp but orthogonal to
        #   baseAxis is calculated and stored with the joint)
        joint.baseAxis = getBodyRelVec(body1, baseAxis)
        tempTwistUp = getBodyRelVec(body1, baseTwistUp)
        baseSide = norm3(cross(tempTwistUp, joint.baseAxis))
        joint.baseTwistUp = norm3(cross(joint.baseAxis, baseSide))

        # store the base twist up vector (original version) in the local
        #   coordinate system of the secondary body
        joint.baseTwistUp2 = getBodyRelVec(body2, baseTwistUp)

        # store joint rotation limits and resistive force factors
        joint.flexLimit = flexLimit
        joint.twistLimit = twistLimit
        joint.flexForce = flexForce
        joint.twistForce = twistForce

        joint.style = "ball"
        self.joints.append(joint)

        return joint

    def update(self):
        pass
