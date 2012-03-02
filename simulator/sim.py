import sys, random, time, threading
from math import *
import ode
import pygame
from OpenGLLibrary import *

sys.path.append('../inc')
from pubsub import *
from helpers import *
from MultiBody import ControlledHingeJoint
from MultiBody import LinearActuator
#from SixLegSpider import SixLegSpider
from SpiderWHydraulics import SpiderWHydraulics

# Simulation time 
t = 0
# Global timestep
#global_dt = 1.5*2.5e-4
global_dt = 1e-2
global_n_iterations = 0

# This is the publisher where we make data available
publisher = Publisher(5055)

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

def createCapsule(world, space, mass, length, radius):
    """Creates a capsule body and corresponding geom."""
    body = ode.Body(world)
    m = ode.Mass()
    m.setCappedCylinderTotal(mass, 3, radius, length)
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

def naiveWalk():
    global t
    # Walk away!
    gait_cycle=5.0
    foot_positions = []
    x_off =  1.00*cos(2*pi*t/gait_cycle)
    #z_off =  0.75*(1.0-sin(4*pi*t/gait_cycle))
    #if z_off<0:
    #    z_off *= -1
    z_off =  1.5*sin(2*pi*t/gait_cycle)
    if z_off<0:
        z_off *= -1
    for i in range(6):
        z = -2.0
        if (i%2) ^ (t%gait_cycle<(gait_cycle/2.0)):
            z += z_off
        p = ( sign(i%2)*x_off + 2.29*cos(pi/6 + (i*pi/3)), 2.29*sin(pi/6 + (i*pi/3)), z )
        foot_positions.append(p)
    return foot_positions

def standUp():
    """Don't walk, just sort of try to stand up"""
    global t
    # Walk away!
    gait_cycle      = 3.0     # time in seconds
    step_cycle      = gait_cycle/2.0
    neutral_r       = 2.5     # radius from body center or foot resting, m
    stride_length   = 2.00    # length of a stride, m
    body_h          = 2.20    # height of body off the ground, m
    foot_lift_h     = 1.00     # how high to lift feet in m

    foot_positions = []
    z_off        =  foot_lift_h*sin(2*pi*t/gait_cycle)
    if z_off<0:
        z_off *= -1
    for i in range(6):
        x = neutral_r*cos(pi/6 + (i*pi/3))
        y = neutral_r*sin(pi/6 + (i*pi/3))
        z = -body_h
        if (i%2) ^ (t%gait_cycle<(step_cycle)):
            z += z_off
        p = ( x, y, z )
        foot_positions.append(p)
    return foot_positions

def constantSpeedWalk():
    global t
    # Walk away!
    gait_cycle      = 3.0     # time in seconds
    step_cycle      = gait_cycle/2.0
    swing_overshoot = 1.00
    neutral_r       = 2.5     # radius from body center or foot resting, m
    stride_length   = 2.00    # length of a stride, m
    body_h          = 2.20    # height of body off the ground, m
    foot_lift_h     = 0.25     # how high to lift feet in m

    #gait_cycle      = 1.8     # time in seconds
    #step_cycle      = gait_cycle/2.0
    #swing_overshoot = 1.00
    #neutral_r       = 1.7     # radius from body center or foot resting, m
    #stride_length   = 1.4     # length of a stride, m
    #body_h          = 1.5     # height of body off the ground, m
    #foot_lift_h     = 0.1     # how high to lift feet in m
    foot_positions = []
    x_off_swing  =  swing_overshoot*(stride_length/2.0)*cos(2*pi*(t%step_cycle)/gait_cycle)
    x_off_stance =  stride_length*(((t%step_cycle)/step_cycle)-0.5)
    z_off        =  foot_lift_h*sin(2*pi*t/gait_cycle)
    if z_off<0:
        z_off *= -1
    for i in range(6):
        x = neutral_r*cos(pi/6 + (i*pi/3))
        y = neutral_r*sin(pi/6 + (i*pi/3))
        z = -body_h
        if (i%2) ^ (t%gait_cycle<(step_cycle)):
            x += x_off_swing
            z += z_off
        else:
            x += x_off_stance
        p = ( x, y, z )
        foot_positions.append(p)
    return foot_positions

def simMainLoop():
    global Paused, lasttime, global_n_iterations, exit_flag, t, global_dt, global_robot_pos
    global space

    #print len(ode._geom_c2py_lut)

    if(t < 5):
        robot.setDesiredFootPositions( standUp() )
    else:
        robot.setDesiredFootPositions( constantSpeedWalk() )

    # Detect collisions and create contact joints
    space.collide((world, contactgroup), near_callback)

    # Simulation step
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
        glLibColor(body.color)
        cylHalfHeight = body.length / 2.0
        if not hasattr(body,'glObj'):
            body.glObj = glLibObjCapsule( body.radius, body.length, CAPSULE_SLICES )
        #c = glLibObjCylinder( body.radius, body.length, CAPSULE_SLICES )
        body.glObj.myDraw( rot )
        #del c
def draw_geom(geom):
    if isinstance(geom, ode.GeomBox):
        glLibColor(geom.color)
        p = geom.getPosition()
        r = geom.getRotation()
        rot = makeOpenGLMatrix(r, p)
        if not hasattr(geom,'glObj'):
            geom.glObj = glLibObjCube( geom.getLengths() )
        geom.glObj.myDraw( rot )

def pave(x,y):
    """Put down a pavement tile"""
    global static_geoms, pavement, space
    g = createBoxGeom(space, (0.99,0.99,0.99))
    g.color = (0,128,0,255)
    pos = (x,y,random.uniform(-1.1, -0.9))
    rand_unit = tuple([random.uniform(-1,1) for i in range(3)])
    rand_unit = div3(rand_unit, len3(rand_unit))
    rot = calcRotMatrix(rand_unit, random.uniform(0,0*2*pi/120))
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
# This is the sponginess of the universe
world.setERP(0.8)
world.setCFM(1E-6)
#world.setERP(0.0)
#world.setCFM(0.0)

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
#robot = SixLegSpider(world, space, 500, (0.0, 0.0, 3.0))
robot = SpiderWHydraulics(world, space, 500, (0.0, 0.0, 0.3))
print "total mass is %.1f kg (%.1f lbs)" % (robot.totalMass, robot.totalMass * 2.2)

#g = createBoxGeom(space, (1.0,1.0,1.0))
#g.setPosition( (-5, 1, 1) )
#static_geoms.add(g)
#b,g = createCapsule(world, space, 1.0e2, 1.0, 0.5)
#b.color = (128,0,0,255)
#bodies.append(b)
#b.setPosition( (-5, 1, 3) )

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

glLibColorMaterial(True) 
glLibTexturing(True)
glLibLighting(True)
Sun = glLibLight([400,200,250],cam)
Sun.enable()

#dictionary of all pavement tiles by position
pavement = {}

for x in range(-5,6):
    for y in range(-5,6):
        pave(x,y)

pavement_center = [0,0]

# Populate the publisher
publisher.addToCatalog( 'time', lambda: t )
publisher.addToCatalog( 'body.height', lambda: robot.getPosition()[2] )
publisher.addToCatalog( 'body.distance', lambda: len3(robot.getPosition()) )
publisher.addToCatalog( 'body.velocity', lambda: len3(robot.getVelocity()) )

def getPower( l ):
    return abs(l.getVel()*l.getForceLimit())

for i in range(6):
    c = ( ControlledHingeJoint.getTorque, robot.legs[i]['hip_pitch'] )
    publisher.addToCatalog( 'leg%d.hip.pitch.torque'%i, c)
    c = ( ControlledHingeJoint.getTorque, robot.legs[i]['hip_yaw'] )
    publisher.addToCatalog( 'leg%d.hip.yaw.torque'%i, c )
    c = ( ControlledHingeJoint.getTorque, robot.legs[i]['knee_pitch'] )
    publisher.addToCatalog( 'leg%d.knee.pitch.torque'%i, c )

    c = ( LinearActuator.getVel, robot.legs[i]['hip_pitch'] )
    publisher.addToCatalog( 'leg%d.hip.pitch.vel'%i, c )
    c = ( LinearActuator.getVel, robot.legs[i]['hip_yaw'] )
    publisher.addToCatalog( 'leg%d.hip.yaw.vel'%i, c )
    c = ( LinearActuator.getVel, robot.legs[i]['knee_pitch'] )
    publisher.addToCatalog( 'leg%d.knee.pitch.vel'%i, c )

    c = ( getPower, robot.legs[i]['hip_pitch'] )
    publisher.addToCatalog( 'leg%d.hip.pitch.power'%i, c )
    c = ( getPower, robot.legs[i]['hip_yaw'] )
    publisher.addToCatalog( 'leg%d.hip.yaw.power'%i, c )
    c = ( getPower, robot.legs[i]['knee_pitch'] )
    publisher.addToCatalog( 'leg%d.knee.pitch.power'%i, c )

    c = ( LinearActuator.getAngle, robot.legs[i]['hip_pitch'] )
    publisher.addToCatalog( 'leg%d.hip.pitch.angle.actual'%i, c)
    c = ( LinearActuator.getAngle, robot.legs[i]['hip_yaw'] )
    publisher.addToCatalog( 'leg%d.hip.yaw.angle.actual'%i, c )
    c = ( LinearActuator.getAngle, robot.legs[i]['knee_pitch'] )
    publisher.addToCatalog( 'leg%d.knee.pitch.angle.actual'%i, c )
    c = ( LinearActuator.getLength, robot.legs[i]['knee_pitch'] )
    publisher.addToCatalog( 'leg%d.knee.act.len.actual'%i, c )
    c = ( LinearActuator.getAngleTarget, robot.legs[i]['hip_pitch'] )
    publisher.addToCatalog( 'leg%d.hip.pitch.angle.target'%i, c)
    c = ( LinearActuator.getAngleTarget, robot.legs[i]['hip_yaw'] )
    publisher.addToCatalog( 'leg%d.hip.yaw.angle.target'%i, c )
    c = ( LinearActuator.getAngleTarget, robot.legs[i]['knee_pitch'] )
    publisher.addToCatalog( 'leg%d.knee.pitch.angle.target'%i, c )
    c = ( LinearActuator.getLengthTarget, robot.legs[i]['knee_pitch'] )
    publisher.addToCatalog( 'leg%d.knee.act.len.target'%i, c )

# Start publishing data
publisher.start()

#from guppy import hpy
#h=hpy()

import OpenGL.contextdata as contextdata

cam_pos = (0,10,10)

t_last = time.time()
t_present = None

while True:
    # hack to run real time
    t_present = time.time()
    global_dt = t_present - t_last
    if global_dt > 1e-2:
        global_dt = 1e-2
    t_last = t_present
    simMainLoop()

    # Do we need to repave the road?
    p = robot.getPosition()
    
    # Do we need to move x-wise?
    if p[0] + .5 < pavement_center[0]:
        pavement_center[0] -= 1
        x = pavement_center[0]-5
        for y in range( pavement_center[1]-5,pavement_center[1]+6):
            unpave(x+11, y)
            pave(  x,   y)
    elif p[0] - .5 > pavement_center[0]:
        pavement_center[0] += 1
        x = pavement_center[0]+5
        for y in range( pavement_center[1]-5,pavement_center[1]+6):
            unpave(x-11, y)
            pave(  x,   y)

    if p[1] + .5 < pavement_center[1]:
        pavement_center[1] -= 1
        y = pavement_center[1]-5
        for x in range( pavement_center[0]-5,pavement_center[0]+6):
            unpave(     x, y+11)
            pave(       x, y)
    elif p[1] - .5 > pavement_center[1]:
        pavement_center[1] += 1
        y = pavement_center[1]+5
        for x in range(pavement_center[0]-5,pavement_center[0]+6):
            unpave(    x, y-11)
            pave(      x, y)
    
    if not global_n_iterations % 5:
        publisher.publish()

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
        if event.type == MOUSEBUTTONDOWN:
            click_pos = glLibUnProject( event.pos )
            if event.button == 1:
                b,g = createCapsule(world, space, 1.0e2, 1.3, 0.3)
                b.color = (128,0,0,255)
                bodies.append(b)
                b.setPosition( add3(click_pos, (0,0,1.5)) )
            elif event.button == 3:
                g = createBoxGeom(space, (1.0,1.0,0.25))
                g.color = (128,0,0,255)
                g.setPosition( add3(click_pos,(0,0,0.125)) )
                static_geoms.add(g)
            elif event.button == 4:
                cam_pos = div3( cam_pos, 1.05 )
            elif event.button == 5:
                cam_pos = mul3( cam_pos, 1.05 )
        if event.type == MOUSEMOTION:
            if event.buttons[1]:
                # z axis rotation
                az = -event.rel[0]/(60*pi)
                cam_pos = ( cam_pos[0]*cos(az)-cam_pos[1]*sin(az), cam_pos[0]*sin(az)+cam_pos[1]*cos(az), cam_pos[2] )
                # pitch rotation
                ay = event.rel[1]/(60*pi)
                # find pitch axis
                axis = norm3(cross( cam_pos, (0,0,1) ))
                cam_pos = rotateAxisAngle( cam_pos, axis, ay )


    #if mpress[0]:
    #    pass
    cam.center = add3(p, (0,0,0.3))
    cam.pos = add3(p,cam_pos)
    Window.clear()
    cam.set_camera()

    for g in static_geoms:
        draw_geom(g)
    prune = []
    for b in bodies:
        tp = b.getPosition()
        if tp[2] < -5.0:
            # We've fallen off the world
            prune.append(b)
        draw_body(b)
    for b in prune:
        bodies.remove(b)
        del b
    for b in robot.bodies:
        draw_body(b)
    Window.flip()
