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
        body_COM = self.getBody(1).getPosition()
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
    def getAngleError( self ):
        return calcAngularError( self.angle_target, self.getAngle() )
    def setTorqueLimit( self, limit ):
        self.setParam(ode.ParamFMax,    limit)
    def getTorqueLimit( self ):
        return self.getParam(ode.ParamFMax)
    def setGain( self, gain ):
        self.gain = gain
    def getGain( self ):
        return self.gain
    def update( self ):
        """Do control"""
        error = self.getAngleError()
        self.setParam( ode.ParamVel, error*self.gain )

class LinearActuatorControlledHingeJoint(ControlledHingeJoint):
    """This simulates a hinge joint driven by a linear actuator.
    It is computationally much more efficient than using a hinge, slider
    and 2 sphere joints."""
    def __init__( self, world ):
        """
        The origin in the anchor specification coordinate system is the hinge anchor
        The anchor specification coordinate system is 2D and in the plane normal
        to the hinge axis
        a1_x is the placement of anchor 1 on the x axis 
        (y axis placement assumed to be 0)
        a2_x and a2_y are the placement of anchor 2
        """
        ode.HingeJoint.__init__(self, world)
        self.setFeedback(True)
        self.setAngleTarget(0.0)
        self.setGain(1.0)
    def setActuatorAnchors( self, a1_x, a2_x, a2_y ):
        self.a1_x = a1_x
        self.a2_x = a2_x
        self.a2_y = a2_y
        self.neutral_angle = atan2(a2_y, a2_x)
    def getLength( self ):
        a = self.getActPath()
        return len2(a)
    def getLengthRate( self ):
        arate = self.getAngleRate()
        link_ang = self.neutral_angle + self.getAngle()
        link_len = len2((self.a2_x, self.a2_y))
        act = self.getActPath()
        act_ang = atan2(act[1],act[0])
        return arate*link_len*sin( link_ang + act_ang )
    def getHydraulicFlow( self ):
        return self.getLengthRate()*self.cross_section
    def getHydraulicFlowGPM( self ):
        return self.getLengthRate()*self.cross_section*15850.3
    def getActPath( self ):
        """
        Return the path of the actuator in the hinge plane
        """
        # Apply joint rotation to one anchor
        ang = self.neutral_angle + self.getAngle()
        # Get the angle of the actuator with the horizontal
        act = (self.a2_x*cos(ang) - self.a1_x, self.a2_y*sin(ang))
        return act
    def __get_lever_arm( self ):
        act = self.getActPath()
        h_ang = atan2(act[1], act[0])
        # Get the lever arm
        l_arm = sin(h_ang)*self.a1_x
        return l_arm
    def __force_to_torque( self, force ):
        """
        Give the max applicable torque at the present orientation
        given an actuator force
        """
        return self.__get_lever_arm()*force
    def __torque_to_force( self, torque ):
        return torque/self.__get_lever_arm()
    def setForceLimit( self , f ):
        self.force_limit = f
    def setTorqueLimit( self, l ):
        print 'Cannot set torque limit on linear actuator controlled hinge'
    def getTorqueLimit( self ):
        return abs(self.__get_lever_arm()*self.force_limit)
    def update( self ):
        limit = self.getTorqueLimit()
        self.setParam(ode.ParamFMax,    limit)
        ControlledHingeJoint.update(self)

class LinearVelocityActuatedHingeJoint(LinearActuatorControlledHingeJoint):
    """This simulates a hinge joint driven by a linear actuator that accepts a
    velocity command."""

    def __init__(self, world):
        super(LinearVelocityActuatedHingeJoint, self).__init__(world)
        #LinearActuatorControlledHingeJoint.__init__(self, world)
	self.lenrate = 0

    def getAngRate( self ):
        link_ang = self.neutral_angle + self.getAngle()
        link_len = len2((self.a2_x, self.a2_y))
        act = self.getActPath()

        act_ang = atan2(act[1],act[0])
        ang_vel = self.lenrate / (link_len*sin( link_ang + act_ang ))
	return ang_vel
 
    def setLengthRate(self, vel_mps):
	self.lenrate = vel_mps
        
    def update(self):
        self.setParam(ode.ParamFMax, self.getTorqueLimit())
        self.setParam(ode.ParamVel, self.getAngRate() )

class LinearActuator:
    """Give LinearActuator two anchor points and a radius and it will create a body
    with controllable slider joint.  This requires a universal joint on each end."""
    def __init__(self, world, body1, body2, p1, p2, hinge=None):
        # Cap on one side
        cap1 = ode.Body( world )
        cap1.color = (0,128,0,255)
        m = ode.Mass()
        m.setCappedCylinderTotal(1.0, 3, 0.01, 0.01)
        cap1.setMass(m)
        # set parameters for drawing the body
        cap1.shape = "capsule"
        cap1.length = .05
        cap1.radius = .05
        cap1.setPosition(p1)

        # Attach the cap to the body
        u1 = ode.BallJoint(world)
        u1.attach(body1, cap1)
        u1.setAnchor(p1)
        u1.style = "ball"

        # Cap on other side
        cap2 = ode.Body( world )
        cap2.color = (0,128,0,255)
        m = ode.Mass()
        m.setCappedCylinderTotal(1.0, 3, 0.01, 0.01)
        cap2.setMass(m)
        # set parameters for drawing the body
        cap2.shape = "capsule"
        cap2.length = .05
        cap2.radius = .05
        cap2.setPosition(p2)

        # Attach the cap to the body
        u2 = ode.BallJoint(world)
        u2.attach(body2, cap2)
        u2.setAnchor(p2)
        u2.style = "ball"
       
        # The all-important slider joint
        s = ode.SliderJoint( world )
        s.attach( cap1, cap2 )
        s.setAxis( sub3(p1, p2) )
        s.setFeedback(True)

        self.body1 = body1
        self.body2 = body2
        self.cap1 = cap1
        self.cap2 = cap2
        self.u1 = u1
        self.u2 = u2
        self.slider = s
        self.gain = 1.0
        self.neutral_length = dist3(p1,p2)
        self.length_target  = dist3(p1,p2)
        if hinge != None:
            # Hinge is the joint this linear actuator controls
            # This allows angular control
            self.hinge=hinge
            # Store these for later to save on math.
            # TODO:  I am being lazy and assuming u1->u2
            # is orthogonal to the hinge axis
            self.h_to_u1 = dist3( self.hinge.getAnchor(), self.u1.getAnchor() )
            self.h_to_u2 = dist3( self.hinge.getAnchor(), self.u2.getAnchor() )
            self.neutral_angle = thetaFromABC(self.h_to_u1, self.h_to_u2, self.neutral_length )

    def getAngle( self ):
        return self.hinge.getAngle()
    def setAngleTarget( self, t ):
        """Figure out the length of actuator that corresponds to
        the angle."""
        self.angle_target = t
        #self.length_target = cFromThetaAB( self.neutral_angle+t, self.h_to_u1, self.h_to_u2 )
        self.length_target = cFromThetaAB( t - self.neutral_angle, self.h_to_u1, self.h_to_u2 )
    def getAngleTarget( self ):
        return self.angle_target
    def getVel( self ):
        return self.slider.getPositionRate()
    def getForce( self ):
        f1, t1, f2, t2 = self.slider.getFeedback()
        return len3(f1)
    def setForceLimit( self, f ):
        self.slider.setParam(ode.ParamFMax,    f)
    def getForceLimit( self ):
        return self.slider.getParam(ode.ParamFMax)
    def setLengthTarget( self, t ):
        self.length_target = t
    def getLengthTarget( self ):
        return self.length_target
    def getLength( self ):
        return self.neutral_length + self.slider.getPosition()
    def setGain( self, gain ):
        self.gain = gain
    def getGain( self ):
        return self.gain
    def update( self ):
        """Do control"""
        #f = self.getForce()
        #TODO set color
        error = self.length_target - self.getLength()
        self.slider.setParam( ode.ParamVel, error*self.gain )
    def setMaxLength( self, l ):
        self.slider.setParam(ode.ParamLoStop, self.neutral_length - l)
    def setMinLength( self, l ):
        self.slider.setParam(ode.ParamHiStop, self.neutral_length - l)

class MultiBody():
    def __init__(self, sim, density=500, offset = (0.0, 0.0, 0.0), publisher=None, pub_prefix=""):
        """Creates a ragdoll of standard size at the given offset."""

        self.sim              = sim
        self.density          = density
        self.bodies           = []
        self.geoms            = []
        self.joints           = []
        self.totalMass        = 0.0
        self.update_objects   = []
        self.publisher        = publisher
        self.pub_prefix       = pub_prefix

        # These are the inputs and outputs for our controller
        self.inputs  = {}
        self.outputs = {}

        self.offset = offset


        self.buildBody()
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

        body = ode.Body(self.sim.world)
        # This is our own stupid shit
        body.color = (128,128,40,255)
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
        geom = ode.GeomCCylinder(self.sim.space, radius, cyllen)
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

            body = ode.Body(self.sim.world)
            m = ode.Mass()
            m.setCappedCylinder(self.density, 3, radius, cyllen)
            body.setMass(m)

            # set parameters for drawing the body
            body.shape = "capsule"
            body.length = cyllen
            body.radius = radius

            # create a capsule geom for collision detection
            geom = ode.GeomCCylinder(self.sim.space, radius, cyllen)
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
        joint = ode.FixedJoint(self.sim.world)
        joint.attach(body1, body2)
        joint.setFixed()

        joint.style = "fixed"
        self.joints.append(joint)

        return joint
    def addLinearActuator(self, body1, body2, p1, p2, hinge=None):
        p1 = add3(p1, self.offset)
        p2 = add3(p2, self.offset)
        # TODO: This breaks some class assumptions... think of a nicer way to do this
        joint = LinearActuator( self.sim.world, body1, body2, p1, p2, hinge )
        self.joints.append(joint)
        self.bodies.append(joint.cap1)
        self.bodies.append(joint.cap2)
        self.update_objects.append( joint )

        return joint
    def addLinearControlledHingeJoint(self, body1, body2, anchor, axis, a1x, a2x, a2y, loStop = -ode.Infinity,
        hiStop = ode.Infinity, force_limit = 0.0, gain = 1.0):

        anchor = add3(anchor, self.offset)

        joint = LinearActuatorControlledHingeJoint( world = self.sim.world )
        joint.setActuatorAnchors( a1x, a2x, a2y )
        joint.setForceLimit( force_limit )
        joint.setGain( gain )
        joint.attach(body1, body2)
        joint.setAnchor(anchor)
        joint.setAxis(axis)
        joint.setParam(ode.ParamLoStop, loStop)
        joint.setParam(ode.ParamHiStop, hiStop)

        joint.style = "hinge"
        self.joints.append(joint)
        self.update_objects.append(joint)

        return joint
    def addLinearVelocityActuatedHingeJoint(self, body1, body2, anchor, axis, a1x, a2x, a2y, loStop = -ode.Infinity,
        hiStop = ode.Infinity, force_limit = 0.0, gain = 1.0):

        anchor = add3(anchor, self.offset)

        joint = LinearVelocityActuatedHingeJoint( world = self.sim.world )
        joint.setActuatorAnchors( a1x, a2x, a2y )
        joint.setForceLimit( force_limit )
        joint.setGain( gain )
        joint.attach(body1, body2)
        joint.setAnchor(anchor)
        joint.setAxis(axis)
        joint.setParam(ode.ParamLoStop, loStop)
        joint.setParam(ode.ParamHiStop, hiStop)

        joint.style = "hinge"
        self.joints.append(joint)
        self.update_objects.append(joint)

        return joint
    def addControlledHingeJoint(self, body1, body2, anchor, axis, loStop = -ode.Infinity,
        hiStop = ode.Infinity, torque_limit = 0.0, gain = 1.0):

        anchor = add3(anchor, self.offset)

        joint = ControlledHingeJoint( world = self.sim.world )
        joint.setTorqueLimit( torque_limit )
        joint.setGain( gain )
        joint.attach(body1, body2)
        joint.setAnchor(anchor)
        joint.setAxis(axis)
        joint.setParam(ode.ParamLoStop, loStop)
        joint.setParam(ode.ParamHiStop, hiStop)

        joint.style = "hinge"
        self.joints.append(joint)
        self.update_objects.append(joint)

        return joint
    def addHingeJoint(self, body1, body2, anchor, axis, loStop = -ode.Infinity,
        hiStop = ode.Infinity):

        anchor = add3(anchor, self.offset)

        joint = ode.HingeJoint(self.sim.world)
        joint.attach(body1, body2)
        joint.setAnchor(anchor)
        joint.setAxis(axis)
        joint.setParam(ode.ParamLoStop, loStop)
        joint.setParam(ode.ParamHiStop, hiStop)

        joint.style = "hinge"
        self.joints.append(joint)

        return joint
    def addUniversalJoint(self, body1, body2, anchor, axis1, axis2,
        loStop1 = -ode.Infinity, hiStop1 = ode.Infinity,
        loStop2 = -ode.Infinity, hiStop2 = ode.Infinity):

        anchor = add3(anchor, self.offset)

        joint = ode.UniversalJoint(self.sim.world)
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
    def addBallJoint(self, body1, body2, anchor ):
        anchor = add3(anchor, self.offset)

        # create the joint
        joint = ode.BallJoint(self.sim.world)
        joint.attach(body1, body2)
        joint.setAnchor(anchor)

        joint.style = "ball"
        self.joints.append(joint)

        return joint
    def update(self):
        for o in self.update_objects:
            o.update()
