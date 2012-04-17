import sys, random, threading
from math import *
import ode
import pygame
from OpenGLLibrary import *

from pubsub import *
from helpers import *

class Paver:
    def __init__( self, center, sim ):
        """
        center is the initial center of the pavement
        space is the ODE space in which to place our pavement tiles
        """
        self.center = list(center)
        self.sim    = sim
        self.pavement = {}
        for x in range(center[0]-5,center[0]+6):
            for y in range(center[1]-5,center[1]+6):
                self.pave(x,y)
    def recenter( self, new_center ):
        """
        Figure out if we need to shift our pavement tiles.
        """
        if new_center[0] + .5 < self.center[0]:
            self.center[0] -= 1
            x = self.center[0]-5
            for y in range( self.center[1]-5,self.center[1]+6):
                self.unpave(x+11, y)
                self.pave(  x,   y)
        elif new_center[0] - .5 > self.center[0]:
            self.center[0] += 1
            x = self.center[0]+5
            for y in range( self.center[1]-5,self.center[1]+6):
                self.unpave(x-11, y)
                self.pave(  x,   y)

        if new_center[1] + .5 < self.center[1]:
            self.center[1] -= 1
            y = self.center[1]-5
            for x in range( self.center[0]-5,self.center[0]+6):
                self.unpave(     x, y+11)
                self.pave(       x, y)
        elif new_center[1] - .5 > self.center[1]:
            self.center[1] += 1
            y = self.center[1]+5
            for x in range(self.center[0]-5,self.center[0]+6):
                self.unpave(    x, y-11)
                self.pave(      x, y)
    def pave(self,x,y):
        """Put down a pavement tile"""
        g = self.sim.createBoxGeom((0.99,0.99,0.99))
        g.color = (0,128,0,255)
        pos = (x,y,random.uniform(-0.5, -0.3))
        rand_unit = tuple([random.uniform(-1,1) for i in range(3)])
        rand_unit = div3(rand_unit, len3(rand_unit))
        rot = calcRotMatrix(rand_unit, random.uniform(0,0*2*pi/120))
        g.setPosition(pos)
        g.setRotation(rot)
        self.pavement[(x,y)]=g
    def unpave(self,x,y):
        """Pull up a pavement tile"""
        g = self.pavement[(x,y)]
        self.sim.space.remove(g)
        del self.pavement[(x,y)]
        del g
    def getGeoms(self):
        return self.pavement.values()

class Simulator:
    """
    The simulator class is responsible for starting ODE,
    starting OpenGL (if requested), instantiating the robot
    and running for a specified period of time.
    """
    def __init__(self, dt=1e-2, end_t=0, graphical=True, pave=True, plane=False,\
                    publish_int=5, robot=None, robot_kwargs={}, start_paused = True):
        """If dt is set to 0, sim will try to match realtime
        if end_t is set to 0, sim will run indefinitely
        if graphical is set to true, graphical interface will be started
        pave turns on uneven pavement
        plane turns on a smooth plane to walk on
        publish_int is the interval between data publishes in timesteps"""
        self.sim_t             = 0
        self.dt                = dt
        self.graphical         = graphical
        self.pave              = pave
        self.plane             = plane
        self.publish_int       = publish_int
        self.n_iterations      = 0
        self.real_t_laststep   = 0
        self.real_t_lastrender = 0
        self.real_t_start      = getSysTime()
        self.paused            = start_paused
        
        # ODE space object: handles collision detection
        self.space = ode.Space()
        # ODE world object: handles body dynamics
        self.world = ode.World()
        self.world.setGravity((0.0, 0.0, -9.81))
        # Sponginess of the universe.  These numbers are empirical
        self.world.setERP(0.8)
        self.world.setCFM(1E-6)
        # Joint group for the contact joints generated during collisions
        self.contactgroup = ode.JointGroup()

        self.geoms  = []
        self.bodies = []

        if self.plane:
            g = self.createBoxGeom((1e2,1e2,1))
            g.color = (0,128,0,255)
            pos = (0,0,-0.5)
            g.setPosition(pos)
            self.geoms.append(g)
            #self.plane = ode.GeomPlane(self.space, (0, 0, 1), 0)

        if self.pave:
            self.paver = Paver( (0,0), self )

        # This is the publisher where we make data available
        self.publisher = Publisher(5055)
        self.publisher.start()

        # These are the bodies and geoms that are in the universe
        self.robot  = robot(self, publisher=self.publisher, **robot_kwargs)

        # Start populating the publisher
        self.publisher.addToCatalog( 'time', self.getSimTime )
        self.publisher.addToCatalog( 'body.height', lambda: self.robot.getPosition()[2] )
        self.publisher.addToCatalog( 'body.distance', lambda: len3(self.robot.getPosition()) )
        self.publisher.addToCatalog( 'body.velocity', lambda: len3(self.robot.getVelocity()) )

        if self.graphical:
            # initialize pygame
            pygame.init()
            # create the program window
            Screen = (800,600)
            self.window = glLibWindow(Screen,caption="Robot Simulator")
            View3D = glLibView3D((0,0,Screen[0],Screen[1]),45)
            View3D.set_view() 
            self.camera = glLibCamera( pos=(0, 10, 10), center=(0,0,0), upvec=(0,0,1) )
            glLibColorMaterial(True) 
            glLibLighting(True)
            Sun = glLibLight([400,200,250],self.camera)
            Sun.enable()
            self.cam_pos = (0,10,10)
    def getSimTime(self):
        return self.sim_t
    def near_callback(self, args, geom1, geom2):
        """
        Callback function for the collide() method.

        This function checks if the given geoms do collide and creates contact
        joints if they do.
        """
        # Are both geoms static?  We don't care if they touch.
        if geom1 in self.geoms and geom2 in self.geoms:
            return

        # Are both geoms connected?
        if (ode.areConnected(geom1.getBody(), geom2.getBody())):
            return

        # check if the objects collide
        contacts = ode.collide(geom1, geom2)

        # create contact joints
        world, contactgroup = args
        for c in contacts:
            c.setBounce(0.2)
            c.setMu(50) # 0-5 = very slippery, 50-500 = normal, 5000 = very sticky
            j = ode.ContactJoint(self.world, contactgroup, c)
            j.attach(geom1.getBody(), geom2.getBody())
    def step( self ):
        real_t_present = getSysTime()
        if not self.paused:
            # Try to lock simulation to realtime by controlling the timestep
            if self.dt == 0:
                step_dt = real_t_present - self.real_t_laststep
                self.real_t_laststep = real_t_present
                step_dt = min(1e-2,step_dt)
                step_dt = max(1e-4,step_dt)
            else:
                step_dt = self.dt
            
            # Detect collisions and create contact joints
            self.space.collide((self.world, self.contactgroup), self.near_callback)

            # Simulation step
            self.world.step(step_dt)
            self.sim_t += step_dt

            self.n_iterations += 1

            # apply internal robot forces
            self.robot.update()

            if not self.n_iterations % self.publish_int:
                self.publisher.publish()

            # Remove all contact joints
            self.contactgroup.empty()

            # repave the road
            if self.pave:
                self.paver.recenter(self.robot.getPosition())
        real_t_elapsed = max(getSysTime()-real_t_present, 0.0001)
        # TODO: this is hardcoded 10fps
        if real_t_present - self.real_t_lastrender >= 0.1:
            if not self.paused:
                print ""
                print "Sim time:       %.3f"%self.sim_t
                print "Realtime ratio: %.3f"%(step_dt/real_t_elapsed)
                print "Timestep:       %f"%(step_dt)
                print "Steps per sec:  %.0f"%(1./real_t_elapsed)
		pass
            # Render if graphical
            if self.graphical:
                self.handleInput()
                self.render()
            else:
                self.real_t_lastrender = real_t_present
    def handleInput( self ):
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
                elif event.key == K_p:
                    self.paused = not self.paused
                    print 'Pause toggled'
                elif event.key == K_EQUALS:
                    self.dt *= 1.2
                elif event.key == K_MINUS:
                    self.dt /= 1.2
            if event.type == MOUSEBUTTONDOWN:
                click_pos = glLibUnProject( event.pos )
                if event.button == 1:
                    b,g = self.createCapsule( mass=1.0e2, length=1.3, radius=0.3, pos=add3(click_pos, (0,0,1.5)))
                    #b,g = self.createSphere( mass=1.0e2, radius=0.3, pos=add3(click_pos, (0,0,1.5)))
                elif event.button == 3:
                    g = self.createBoxGeom((1.0,1.0,0.25))
                    g.color = (128,0,0,255)
                    g.setPosition( add3(click_pos,(0,0,0.125)) )
                    self.geoms.append(g)
                elif event.button == 4:
                    self.cam_pos = div3( self.cam_pos, 1.05 )
                elif event.button == 5:
                    self.cam_pos = mul3( self.cam_pos, 1.05 )
            if event.type == MOUSEMOTION:
                if event.buttons[1]:
                    # z axis rotation
                    az = -event.rel[0]/(60*pi)
                    self.cam_pos = ( self.cam_pos[0]*cos(az)-self.cam_pos[1]*sin(az), self.cam_pos[0]*sin(az)+self.cam_pos[1]*cos(az), self.cam_pos[2] )
                    # pitch rotation
                    ay = event.rel[1]/(60*pi)
                    # find pitch axis
                    axis = norm3(cross( self.cam_pos, (0,0,1) ))
                    self.cam_pos = rotateAxisAngle( self.cam_pos, axis, ay )
    def render( self ):
        """
        This method is responsible for drawing to the screen
        The camera is always pointed at robot center
        self.cam_pos holds the position of the camera relative to robot
        """
        self.real_t_lastrender = getSysTime()
        p = self.robot.getPosition()
        self.camera.center = add3(p, (0,0,0.3))
        self.camera.pos = add3(p,self.cam_pos)
        self.window.clear()
        self.camera.set_camera()

        # FIXME: This should be hooked in through some sort of callback system... it does not belong here
        # Thu 22 Mar 2012 07:30:51 PM EDT
        self.robot.colorTorque()

        if self.pave:
            for g in self.paver.getGeoms():
                self.draw_geom(g)
        for g in self.geoms:
            self.draw_geom(g)
        prune = []
        for b in self.bodies:
            tp = b.getPosition()
            if tp[2] < -5.0:
                # We've fallen off the world
                prune.append(b)
            self.draw_body(b)
        for b in prune:
            self.bodies.remove(b)
            del b
        for b in self.robot.bodies:
            self.draw_body(b)
        self.window.flip()
    def draw_body(self, body):
        """Draw an ODE body."""

        if body.shape == "capsule":
            CAPSULE_SLICES = 6
            CAPSULE_STACKS = 6
            p = body.getPosition()
            r = body.getRotation()
            offset = rotate3(r, (0,0,body.length/2.0))
            p = sub3(p,offset)
            rot = makeOpenGLMatrix(r, p)
            glLibColor(body.color)
            cylHalfHeight = body.length / 2.0
            if not hasattr(body,'glObj'):
                body.glObj = glLibObjCapsule( body.radius, body.length, CAPSULE_SLICES )
            body.glObj.myDraw( rot )
        if body.shape == "sphere":
            DETAIL=8
            p = body.getPosition()
            glLibColor(body.color)
            if not hasattr(body,'glObj'):
                body.glObj = glLibObjSphere( body.radius, DETAIL )
            body.glObj.draw( p )
    def draw_geom(self, geom):
        if isinstance(geom, ode.GeomBox):
            glLibColor(geom.color)
            p = geom.getPosition()
            r = geom.getRotation()
            rot = makeOpenGLMatrix(r, p)
            if not hasattr(geom,'glObj'):
                geom.glObj = glLibObjCube( geom.getLengths() )
            geom.glObj.myDraw( rot )
    def createSphere( self, mass=100, radius=1, pos=(0,0,0) ):
        """Creates a capsule body and corresponding geom."""
        body = ode.Body(self.world)
        m = ode.Mass()
        m.setSphereTotal(mass, radius)
        body.setMass(m)

        # set parameters for drawing the body
        body.shape = "sphere"
        body.radius = radius

        # create a capsule geom for collision detection
        geom = ode.GeomSphere(self.space, radius)
        geom.setBody(body)

        body.color = (128,0,0,255)
        body.setPosition( pos )
        self.bodies.append(body)

        return body, geom
    def createCapsule( self, mass=100, length=1, radius=1, pos=(0,0,0) ):
        """Creates a capsule body and corresponding geom."""
        body = ode.Body(self.world)
        m = ode.Mass()
        m.setCappedCylinderTotal(mass, 3, radius, length)
        body.setMass(m)

        # set parameters for drawing the body
        body.shape = "capsule"
        body.length = length
        body.radius = radius

        # create a capsule geom for collision detection
        geom = ode.GeomCCylinder(self.space, radius, length)
        geom.setBody(body)

        body.color = (128,0,0,255)
        body.setPosition( pos )
        self.bodies.append(body)

        return body, geom
    def createBoxGeom( self, sizes=(1.0,1.0,1.0) ):
        return ode.GeomBox(self.space, sizes)

def getPower( l ):
    return abs(l.getVel()*l.getForceLimit())

