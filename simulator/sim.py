import sys, os, random, time, collections
from math import *
from OpenGL.GLUT import *
import ode
import Image
import numpy
import pygame
from pygame.locals import *

from helpers import *

from OpenGLLibrary import *

# Simulation time 
t = 0
# Global timestep
global_dt = 2e-2
global_n_iterations = 0

# rotation directions are named by the third (z-axis) row of the 3x3 matrix,
#   because ODE capsules are oriented along the z-axis
#rightRot = (0.0, 0.0, -1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0)
#leftRot = (0.0, 0.0, 1.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0)
#upRot = (1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0)
#downRot = (1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0)
#bkwdRot = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)

# axes used to determine constrained joint rotations
rightAxis = (0.0,   1.0,    0.0)
leftAxis =  (0.0,   -1.0,   0.0)
upAxis =    (0.0,   0.0,    1.0)
downAxis =  (0.0,   0.0,    -1.0)
bkwdAxis =  (-1.0,  0.0,    0.0)
fwdAxis =   (1.0,   0.0,    0.0)

class Callback:
    def __init__( self, func, *args, **kwargs ):
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def call( self, *args, **kwargs ):
        l = []
        l.extend(self.args)
        l.extend(args)
        d = dict( self.kwargs.items() + kwargs.items() )
        return self.func( *l, **d )

class Controller():
    def __init__( self ):
        self.input_callbacks  = {}
        self.output_callbacks = {}
    def setInputCallback( self, name, callback ):
        if not (isinstance(callback, collections.Callable) \
             or isinstance(callback, Callback)):
            raise
        self.input_callbacks[name] = callback
    def setOutputCallback( self, name, callback ):
        if not (isinstance(callback, collections.Callable) \
             or isinstance(callback, Callback)):
            raise
        if self.output_callbacks.has_key(name):
            raise
        self.output_callbacks[name] = callback
    def getInput( self, name, *args, **kwargs ):
        callback = self.input_callbacks[name]
        if isinstance(callback, Callback):
            return callback.call( *args, **kwargs )
        # Assume it's a function
        return callback(*args, **kwargs)
    def setOutput( self, name, *args, **kwargs ):
        callback = self.output_callbacks[name]
        if isinstance( callback, Callback ):
            return callback.call( *args, **kwargs )
        # Assume it's a function
        return callback(*args, **kwargs)
    def update( self, dt ):
        pass

def calcAngularError( a1, a2 ):
    # Given two angles in radians what is the difference between them?
    error = (a1%(2*pi))-(a2%(2*pi))
    if error > pi:
        error -= 2*pi
    elif error <= -1*pi:
        error += 2*pi
    return error

class AngularPController( Controller ):
    def __init__( self, gain = 1.0 ):
        self.gain = gain
        Controller.__init__(self)
    def update(self, dt):
        target = self.getInput('target')
        actual = self.getInput('actual')
        error = calcAngularError( target, actual )
        output = error*self.gain
        self.setOutput('out', output)

class LegController( Controller ):
    """
    A leg controller takes a requested force vector in 3-space and attempts to deliver it.
    The force vector axes are:
    x: away from the body
    y: looking in the x direction with z pointing out of your head, turn right
    z: up
    If it finds it is approaching the end of its range of motion it will lift off and recycle.
    """
    def __init__( self ):
        self.knee_torque = 0.0
        self.hipy_torque = 0.0
        self.hipz_torque = 0.0
    def update( self, dt ):
        target_force = self.input_callbacks['force vector']()

class MultiBody():
    def __init__(self, world, space, density, offset = (0.0, 0.0, 0.0)):
        """Creates a ragdoll of standard size at the given offset."""

        self.world = world
        self.space = space
        self.density = density
        self.bodies = []
        self.geoms = []
        self.joints = []
        self.totalMass = 0.0

        # These are the inputs and outputs for our controller
        self.inputs  = {}
        self.outputs = {}

        self.offset = offset

        self.buildBody()

    def buildBody(self):
        """This is for the subclasses to define."""
        return

    def addBody(self, p1, p2, radius):
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

BODY_W = 1.0
BODY_T = 0.35
THIGH_L = 1.0
THIGH_W = 0.1
CALF_L = 1.0
CALF_W = 0.075

class SixLegSpider(MultiBody):
    def buildBody( self ):
        """ Build an equilateral hexapod """
        # These are the rotation matrices we will use
        r_30z = calcRotMatrix( upAxis, pi/6.0 )
        r_60z = calcRotMatrix( upAxis, pi/3.0 )
        r_90z = calcRotMatrix( upAxis, pi/2.0 )
        # The structure of the spider is a hexagon... looks like a asterisk
        # p_hip is the point where the hip is located.
        # We want to start it 30 degrees into a rotation around Z
        p_hip = (BODY_W/2.0, 0, 0)
        #p_hip = rotate3( r_30z, p_hip )
        self.core = [0,0,0]
        #for i in range(3):
        #    self.core[i] = self.addBody( p_hip, mul3(p_hip, -1), BODY_T )
        #    p_hip = rotate3( r_60z, p_hip )
        self.core[0] = self.addBody( p_hip, mul3(p_hip, -1), BODY_T )
        # Glue the central spars together
        #self.addFixedJoint( self.core[0], self.core[1] )
        #self.addFixedJoint( self.core[1], self.core[2] )
        #self.addFixedJoint( self.core[2], self.core[0] )

        # The core of the body is now complete.  Now we start on the legs.
        # Start another rotation
        p = (1, 0, 0)
        p = rotate3( r_30z, p )
        self.thighs         = [0,0,0,0,0,0]
        self.calves         = [0,0,0,0,0,0]
        self.hip_pitch_controllers    = []
        self.hip_yaw_controllers    = []
        self.knee_controllers    = []
        self.knee_angles = [0,0,0,0,0,0]
        self.hip_pitch_angles = [0,0,0,0,0,0]
        self.hip_yaw_angles = [0,0,0,0,0,0]
        for i in range(6):
            hip_p = mul3( p, BODY_W/2.0 )
            knee_p = mul3( p, (BODY_W/2.0)+THIGH_L )
            foot_p = mul3( p, (BODY_W/2.0)+THIGH_L+CALF_L )
            self.thighs[i] = self.addBody(  hip_p, knee_p, THIGH_W )
            # Calculate the axis of rotation for our universal joint
            axis = rotate3( r_90z, p )
            hip = self.addUniversalJoint( self.core[0], self.thighs[i], hip_p,\
                axis, upAxis )
            # Set the max forces on the motors
            hip.setParam(ode.ParamFMax, 1600.0)
            hip.setParam(ode.ParamFMax2, 500.0)
            controller = AngularPController(  )
            controller.setInputCallback(  'actual', hip.getAngle1 )
            callback = Callback( self.getHipPitchAngle, i )
            controller.setInputCallback(  'target', callback )
            callback = Callback( hip.setParam, ode.ParamVel )
            controller.setOutputCallback( 'out',    callback )
            self.hip_pitch_controllers.append(controller)
            controller = AngularPController(  )
            controller.setInputCallback(  'actual', hip.getAngle2 )
            callback = Callback( self.getHipYawAngle, i )
            controller.setInputCallback(  'target', callback )
            callback = Callback( hip.setParam, ode.ParamVel2 )
            controller.setOutputCallback( 'out',    callback )
            self.hip_yaw_controllers.append(controller)

            self.calves[i] = self.addBody(  knee_p, foot_p, CALF_W )
            knee = self.addHingeJoint( self.thighs[i], self.calves[i], knee_p,\
                axis )
            knee.setParam(ode.ParamFMax, 1700.0)
            controller = AngularPController(  )
            controller.setInputCallback(  'actual', knee.getAngle )
            callback = Callback( self.getKneeAngle, i )
            controller.setInputCallback(  'target', callback )
            callback = Callback( knee.setParam, ode.ParamVel )
            controller.setOutputCallback( 'out',    callback )
            self.knee_controllers.append(controller)
            self.controllers = []
            self.controllers.extend( self.hip_pitch_controllers )
            self.controllers.extend( self.hip_yaw_controllers )
            self.controllers.extend( self.knee_controllers )
            p = rotate3( r_60z, p )
    
    def getKneeAngle(self, n):
        return self.knee_angles[n]
    def getHipPitchAngle(self, n):
        return self.hip_pitch_angles[n]
    def getHipYawAngle(self, n):
        return self.hip_yaw_angles[n]


    def setDesiredFootPositions( self, positions ):
        """
        positions should be an iterable of 6 positions relative to the body
        """
        # These are the rotation matrices we will use
        r_30z = calcRotMatrix( upAxis, pi/6.0 )
        r_60z = calcRotMatrix( upAxis, pi/3.0 )
        r_90z = calcRotMatrix( upAxis, pi/2.0 )
        hip_p = (BODY_W/2, 0, 0)
        hip_p = rotate3( r_30z, hip_p )

        i = 0


        for target_p in positions:
            #print target_p
            #print hip_p
            # Make relative to hip
            leg_l = dist3( target_p, hip_p )
            target_p = sub3( target_p, hip_p )
            #print target_p
            #calc knee angle with law of cosines
            #print leg_l
            knee_angle = pi-thetaFromABC( THIGH_L, CALF_L, leg_l )
            #calc hip offset from leg flexion
            hip_offset_angle = -thetaFromABC( THIGH_L, leg_l,  CALF_L )
            #print hip_offset_angle
            #calc hip depression angle
            hip_depression_angle = -atan2( target_p[2], len3((target_p[0], target_p[1], 0)) )
            #print hip_depression_angle
            hip_pitch_angle = hip_offset_angle + hip_depression_angle
            hip_yaw_offset_angle = atan2(hip_p[1], hip_p[0])
            hip_yaw_angle = atan2( target_p[1], target_p[0] ) - hip_yaw_offset_angle

            #print i

            self.knee_angles[i] =       -knee_angle
            self.hip_pitch_angles[i] =  -hip_pitch_angle
            self.hip_yaw_angles[i] =    -hip_yaw_angle

            hip_p = rotate3( r_60z, hip_p )
            i+=1

    def getBodyHeight( self ):
        return self.core[0].getPosition()[2]
    def getPosition( self ):
        return self.core[0].getPosition()

    def update( self ):
        global global_dt
        for controller in self.controllers:
            controller.update( global_dt )

def createCapsule(world, space, density, length, radius):
    """Creates a capsule body and corresponding geom."""
    body = ode.Body(world)
    m = ode.Mass()
    m.setCappedCylinder(density, 3, radius, length)
    body.setMass(m)

    # set parameters for drawing the body
    body.shape = "capsule"
    body.length = length
    body.radius = radius

    # create a capsule geom for collision detection
    geom = ode.GeomCCylinder(space, radius, length)
    geom.setBody(body)

    return body, geom

def createBoxGeom( space, sizes=(1.0,1.0,1.0) ):
    return ode.GeomBox(space, sizes)

def near_callback(args, geom1, geom2):
    """
    Callback function for the collide() method.

    This function checks if the given geoms do collide and creates contact
    joints if they do.
    """
    global static_geoms

    if geom1 in static_geoms and geom2 in static_geoms:
        return

    if (ode.areConnected(geom1.getBody(), geom2.getBody())):
        return

    # check if the objects collide
    contacts = ode.collide(geom1, geom2)

    # create contact joints
    world, contactgroup = args
    for c in contacts:
        c.setBounce(0.2)
        c.setMu(500) # 0-5 = very slippery, 50-500 = normal, 5000 = very sticky
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

world_xpos = world_ypos = world_zpos = 0.0;
global_robot_pos = (0,0,0)

def simMainLoop():
    global Paused, lasttime, global_n_iterations, exit_flag, t, global_dt, global_robot_pos
    global space

    # Walk away!
    gait_cycle=10.0
    foot_positions = []
    x_off =  0.75*cos(2*pi*t/gait_cycle)
    z_off =  0.75*(1.0-sin(4*pi*t/gait_cycle))
    if z_off<0:
        z_off *= -1
    for i in range(6):
        z = -1.0
        if (i%2) ^ (t%gait_cycle<(gait_cycle/2.0)):
            z += z_off
        p = ( sign(i%2)*x_off + 1.5*cos(pi/6 + (i*pi/3)), 1.5*sin(pi/6 + (i*pi/3)), z )
        foot_positions.append(p)
    robot.setDesiredFootPositions( foot_positions )

    # Detect collisions and create contact joints
    space.collide((world, contactgroup), near_callback)

    # Simulation step (with slo motion)
    world.step(global_dt)
    t += global_dt

    global_n_iterations += 1

    # apply internal robot forces
    robot.update()

    # Remove all contact joints
    contactgroup.empty()

# polygon resolution for capsule bodies
CAPSULE_SLICES = 8
CAPSULE_STACKS = 8

def draw_body(body):
    """Draw an ODE body."""
    p = body.getPosition()
    r = body.getRotation()
    offset = rotate3(r, (0,0,body.length/2.0))
    p = sub3(p,offset)
    rot = makeOpenGLMatrix(r, p)

    if body.shape == "capsule":
        cylHalfHeight = body.length / 2.0
        c = glLibObjCapsule( body.radius, body.length, CAPSULE_SLICES )
        c.myDraw( rot )
def draw_geom(geom):
    if isinstance(geom, ode.GeomBox):
        p = geom.getPosition()
        r = geom.getRotation()
        rot = makeOpenGLMatrix(r, p)
        c = glLibObjCube( geom.getLengths() )
        c.myDraw( rot )

def pave(x,y):
    """Put down a pavement tile"""
    global static_geoms, pavement, space
    g = createBoxGeom(space, (1.0,1.0,1.0))
    pos = (x,y,random.uniform(0.0, 0.50))
    rand_unit = tuple([random.uniform(-1,1) for i in range(3)])
    rand_unit = div3(rand_unit, len3(rand_unit))
    rot = calcRotMatrix(rand_unit, random.uniform(0,2*pi/120))
    g.setPosition(pos)
    g.setRotation(rot)
    static_geoms.add(g)
    pavement[(x,y)]=g

def unpave(x,y):
    """Pull up a pavement tile"""
    global static_geoms, pavement, space
    g = pavement[(x,y)]
    if not g:
        print 'FAIL'
    space.remove(g)
    static_geoms.remove(g)
    del g

# initialize pygame
pygame.init()

# create an ODE space object
space = ode.Space()

time.sleep(0.1)

# create an ODE world object
world = ode.World()
world.setGravity((0.0, 0.0, -9.81))
world.setERP(0.8)
world.setCFM(1E-4)

# create a plane geom to simulate a floor
#floor = ode.GeomPlane(space, (0, 0, 1), 0)

# create a list to store any ODE bodies which are not part of the robot (this
#   is needed to avoid Python garbage collecting these bodies)
bodies = []
static_geoms  = set([])

# create a joint group for the contact joints generated during collisions
#   between two bodies collide
contactgroup = ode.JointGroup()

# set the initial simulation loop parameters
lasttime = time.time()

# create the robot
#ragdoll = RagDoll(world, space, 500, (0.0, 0.9, 0.0))
robot = SixLegSpider(world, space, 500, (0.0, 0.0, 3.0))
print "total mass is %.1f kg (%.1f lbs)" % (robot.totalMass, robot.totalMass * 2.2)

# initialize GLUT
#glutInit()

# create the program window
x = 0
y = 0
width = 800
height = 600

Screen = (width,height)
Window = glLibWindow(Screen,caption="Physics Simulator")
View3D = glLibView3D((0,0,Screen[0],Screen[1]),45)
View3D.set_view() 

cam = glLibCamera( pos=(0, 10, 10), center=(0,0,0), upvec=(0,0,1) )

#glLibColorMaterial(True) 
glLibTexturing(True)
glLibLighting(True)
Sun = glLibLight([10,10,40],cam)
Sun.enable()

#dictionary of all pavement tiles by position
pavement = {}

for x in range(-3,4):
    for y in range(-3,4):
        pave(x,y)

pavement_center = [0,0]

while True:
    simMainLoop()

    # Do we need to repave the road?
    p = robot.getPosition()

    # Do we need to move x-wise?
    if p[0] + .5 < pavement_center[0]:
        pavement_center[0] -= 1
        x = pavement_center[0]-3
        for y in range( pavement_center[1]-3,pavement_center[1]+4):
            unpave(x+7, y)
            pave(  x,   y)
    elif p[0] - .5 > pavement_center[0]:
        pavement_center[0] += 1
        x = pavement_center[0]+3
        for y in range( pavement_center[1]-3,pavement_center[1]+4):
            unpave(x-7, y)
            pave(  x,   y)

    if p[1] + .5 < pavement_center[1]:
        pavement_center[1] -= 1
        y = pavement_center[1]-3
        for x in range( pavement_center[0]-3,pavement_center[0]+4):
            unpave(     x, y+7)
            pave(       x, y)
    elif p[1] - .5 > pavement_center[1]:
        pavement_center[1] += 1
        y = pavement_center[1]+3
        for x in range(pavement_center[0]-3,pavement_center[0]+4):
            unpave(    x, y-7)
            pave(      x, y)
        

    if(time.time()-lasttime < 0.05):
        continue

    lasttime = time.time()
    key = pygame.key.get_pressed()
    mpress = pygame.mouse.get_pressed()
    mrel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_flag = 1
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    if mpress[0]:
        current_pos = Sun.get_pos()
        new_pos = [current_pos[0]+(mrel[0]*0.05),current_pos[1],current_pos[2]+(mrel[1]*0.05)]
        Sun.change_pos(new_pos)
    cam.center = p
    cam.pos = add3(p,(0,10,10))
    #cam.update()
    Window.clear()
    cam.set_camera()

    for g in static_geoms:
        draw_geom(g)
    for b in bodies:
        draw_body(b)
    for b in robot.bodies:
        draw_body(b)
    #Map.draw([-3,3,-2],[[90,0,0]])
    Window.flip()
