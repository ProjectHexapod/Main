import sys, random, threading
from math import *
import ode
import pygame
from OpenGLLibrary import *

from pubsub import *
from helpers import *
from UI.send_one_command import sendCommandFromEventKey

#FIXME:  This belongs somewhere common...
import os.path as path
graphics_dir = path.dirname(path.realpath(__file__))+'/graphics'
terrain_dir  = path.dirname(path.realpath(__file__))+'/terrain'

class Simulator(object):
    """
    The simulator class is responsible for starting ODE,
    starting OpenGL (if requested), instantiating the robot
    and running for a specified period of time.
    """
    def __init__(self, dt=1e-2, end_t=0, graphical=True, pave=False, plane=True,\
                    ground_grade=0.0, ground_axis = (0,1,0), publish_int=5,\
                    robot=None, robot_kwargs={}, start_paused = True,\
                    print_updates = False, render_objs = False,
                    draw_contacts = False, draw_support = False,
                    draw_COM = False, height_map = None, terrain_scales=(1,1,1)):
        """
        if end_t is set to 0, sim will run indefinitely
        if graphical is set to true, graphical interface will be started
        plane turns on a smooth plane to walk on
        publish_int is the interval between data publishes in timesteps
        ground_grade slopes the ground around ground_axis by tan(ground_grade)
            degrees
        robot_kwargs get passed to the robot when it is instantiated
        """
        self.sim_t             = 0
        self.dt                = dt
        self.graphical         = graphical
        self.plane             = plane
        self.height_map        = height_map
        self.publish_int       = publish_int
        self.n_iterations      = 0
        self.real_t_laststep   = 0
        self.real_t_lastrender = 0
        self.real_t_start      = getSysTime()
        self.paused            = start_paused
        self.print_updates     = print_updates
        self.render_objs       = render_objs
        self.draw_contacts     = draw_contacts
        self.draw_support      = draw_support
        self.draw_COM          = draw_COM
        
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
        self.contactlist  = []

        # FIXME:  Poorly named lists.
        # bodies contains ode bodies that have mass and collision geometry
        self.bodies   = []
        self.geoms    = []
        self.graphics = []

        if self.plane:
            g = self.createBoxGeom((1e2,1e2,1))
            g.color = (0,128,0,255)
            pos = (0,0,-0.5)
            g.setPosition(pos)
            self.geoms.append(g)
            self.ground = g
            rot_matrix = calcRotMatrix(ground_axis, atan(ground_grade))
            self.ground.setRotation(rot_matrix)
            self.ground.texture = glLibTexture(TEXTURE_DIR+"dot.bmp")
        if self.height_map:
            # initialize pygame
            pygame.init()
            self.mesh = []
            surf = pygame.image.load(os.path.join(terrain_dir, self.height_map))
            dims = surf.get_size()
            self.ground_offset = (-dims[0]/2.0,-dims[1]/2.0,0.0)
            # Create a list of lists.  Map color to height.
            # Black = 0 height
            # Pure white = 1 meter height
            self.height_map = [[(terrain_scales[2]/(4*255.))*sum(surf.get_at((x,y))) for y in range(dims[1])] for x in range(dims[0])]
            max_height = 0
            # TODO: Verify height normalization correct in some other way
            for row in self.height_map:
                for h in row:
                    max_height = max(max_height, h)
            print "Max height: %f"%max_height
            verts = []
            faces = []
            for x in range(dims[0]):
                for y in range(dims[1]):
                    #verts.append((x+self.ground_offset[0],\
                    #              y+self.ground_offset[1],\
                    #              self.height_map[x][y]) )
                    verts.append((x+self.ground_offset[0],\
                                  y+self.ground_offset[1],\
                                  self.height_map[y][x]) )
            def i_from_xy(x,y):
                return dims[1]*x+y
            for x in range(dims[0]-1):
                for y in range(dims[1]-1):
                    faces.append( (i_from_xy(x,y),     i_from_xy(x+1,y), i_from_xy(x,y+1)) )
                    faces.append( (i_from_xy(x+1,y+1), i_from_xy(x,y+1), i_from_xy(x+1,y)) )
            tm = ode.TriMeshData()
            tm.build(verts, faces)
            self.ground_geom = ode.GeomTriMesh( tm, self.space )

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
            glLibTexturing(True)
            glLibLighting(True)
            glLibNormalize(True)
            Sun = glLibLight([400,200,250],self.camera)
            Sun.enable()
            self.cam_pos = (0,10,10)
            if self.height_map:
                self.ground_obj = glLibObjMap(self.height_map,normals=GLLIB_VERTEX_NORMALS,heightscalar=1.0)
    def getSimTime(self):
        return self.sim_t
    def getPaused( self ):
        return self.paused
    def setPaused( self, new_pause_bool ):
        self.paused = new_pause_bool
    def getPaused( self ):
        return self.paused
    def near_callback(self, args, geom1, geom2):
        """
        Callback function for the collide() method.

        This function checks if the given geoms do collide and creates contact
        joints if they do.
        """
        # Are both geoms static?  We don't care if they touch.
        if geom1.getBody() == None and geom2.getBody() == None:
            return

        # Are both geoms connected?
        if (ode.areConnected(geom1.getBody(), geom2.getBody())):
            return

        # check if the objects collide
        contacts = ode.collide(geom1, geom2)

        # create contact joints
        self.world, self.contactgroup = args
        for c in contacts:
            c.setBounce(0.2)
            # ode.ContactApprox1 makes maximum frictional force proportional to
            # normal force
            c.setMode(ode.ContactApprox1)
            # Friction coefficient: Max friction (tangent) force = Mu*Normal force
            c.setMu(0.5)

            j = ode.ContactJoint(self.world, None, c)
            # FIXME: Store the position of the contact
            j.position = c.getContactGeomParams()[0] 
            self.contactlist.append(j)
            j.attach(geom1.getBody(), geom2.getBody())
            j.setFeedback(True)
    def step( self ):
        real_t_present = getSysTime()
        if not self.paused:
            # Remove all contact joints
            self.contactgroup.empty()
            self.contactlist = []
            # Detect collisions and create contact joints
            self.space.collide((self.world, self.contactgroup), self.near_callback)

            # Simulation step
            self.world.step(self.dt)
            self.sim_t += self.dt

            self.n_iterations += 1

            # apply internal robot forces
            self.robot.update()

            if not self.n_iterations % self.publish_int:
                self.publisher.publish()


        real_t_elapsed = max(getSysTime()-real_t_present, 0.0001)
        # TODO: this is hardcoded 10fps
        if real_t_present - self.real_t_lastrender >= 0.1:
            if not self.paused and self.print_updates:
                print ""
                print "Sim time:       %.3f"%self.sim_t
                print "Realtime ratio: %.3f"%(self.dt/real_t_elapsed)
                print "Timestep:       %f"%(self.dt)
                print "Steps per sec:  %.0f"%(1./real_t_elapsed)
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
                else:
                    sendCommandFromEventKey(event.key)
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
        self.camera.center = add3(p, (0,-2,-0.6))
        self.camera.pos = add3(p,self.cam_pos)
        self.window.clear()
        self.camera.set_camera()

        # FIXME: This should be hooked in through some sort of callback system... it does not belong here
        # Thu 22 Mar 2012 07:30:51 PM EDT
        self.robot.colorTorque()

        if hasattr(self, "ground_obj"):
            self.ground_obj.draw(self.ground_offset)
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
        glLibColor( (0,0,200) )
        for g in self.graphics:
            self.draw_graphic(g)
            del g
        self.graphics = []
        if self.draw_contacts:
            for j in self.contactlist:
                self.draw_contact_force_vector(j)
        if self.draw_COM:
            center_of_mass = self.robot.getCOM()
            accel_vec = (0,0,-9.8)
            accel_vec = add3( accel_vec, \
                div3(self.robot.core.getForce(),self.robot.core.getMass().mass) )
            self.createCapsuleGraphic(\
                center_of_mass,\
                add3(center_of_mass,(0,0,-3) ))
        if self.draw_support:
            if len(self.contactlist) >= 3:
                for i in range(len(self.contactlist)):
                    self.createCapsuleGraphic(\
                        self.contactlist[i].position,\
                        self.contactlist[(i+1)%len(self.contactlist)].position )
        self.window.flip()

    def draw_contact_force_vector( self, joint ):
        forces1, torques1, forces2, torques2 = joint.getFeedback()
        offset = div3(forces1,2e3)
        p1 = sub3(joint.position, offset)
        p2 = add3(joint.position, offset)
        self.createCapsuleGraphic( p1, p2 )
    def draw_body(self, body):
        """Draw an ODE body."""

        if hasattr( body, 'glObjPath' ) and self.render_objs:
            p = body.getPosition()
            r = body.getRotation()
            rot = makeOpenGLMatrix(r, p)
            # We must apply both the offset built in to the object
            # and the offset from the world.  Multiply the matrices together
            # to get the compound move/rotation
            rot = mul4x4Matrices(rot, body.glObjOffset)
            glLibColor((255,255,255))
            if not hasattr(body,'glObjCustom'):
                body.glObjCustom = glLibObjFromFile( body.glObjPath )
            try:
                scalar = body.scalar
            except AttributeError:
                scalar = 1
            body.glObjCustom.myDraw( rot, scalar )
        elif body.shape == "capsule":
            CAPSULE_SLICES = 6
            CAPSULE_STACKS = 6
            p = body.getPosition()
            r = body.getRotation()
            # Since ODE and OpenGL define their capsules
            # differently, we must apply an offset.
            offset = rotate3(r, (0,0,body.length/2.0))
            p = sub3(p,offset)
            rot = makeOpenGLMatrix(r, p)
            glLibColor(body.color)
            if not hasattr(body,'glObj'):
                body.glObj = glLibObjCapsule( body.radius, body.length, CAPSULE_SLICES )
            body.glObj.myDraw( rot )
        elif body.shape == "sphere":
            DETAIL=8
            p = body.getPosition()
            glLibColor(body.color)
            if not hasattr(body,'glObj'):
                body.glObj = glLibObjSphere( body.radius, DETAIL )
            body.glObj.draw( p )
        elif body.shape == "box":
            p = body.getPosition()
            r = body.getRotation()
            rot = makeOpenGLMatrix(r, p)
            glLibColor(body.color)
            if not hasattr(body,'glObj'):
                body.glObj = glLibObjCube( (body.lx, body.ly, body.lz) )
            body.glObj.myDraw( rot )
    def draw_geom(self, geom):
        if isinstance(geom, ode.GeomBox):
            glLibColor(geom.color)
            if hasattr( geom, 'texture' ):
                glBindTexture(GL_TEXTURE_2D,geom.texture)
            p = geom.getPosition()
            r = geom.getRotation()
            rot = makeOpenGLMatrix(r, p)
            if not hasattr(geom,'glObj'):
                if hasattr(geom, 'texture'):
                    lengths = geom.getLengths()
                    geom.glObj = glLibObjTexCube( lengths, lengths[0] )
                else:
                    geom.glObj = glLibObjCube( geom.getLengths() )
            geom.glObj.myDraw( rot )
    def draw_graphic( self, graphic ):
        """
        """
        if isinstance(graphic, glLibObjCapsule):
            graphic.myDraw( graphic.gl_matrix )
        else:
            raise NotImplemented
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
        # create a reference to the body geom in case the user does not want to keep track of it.
        body.geom = geom

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
        # create a reference to the body geom in case the user does not want to keep track of it.
        body.geom = geom

        body.color = (128,0,0,255)
        body.glObjPath = graphics_dir+"/2003eclipse.obj"
        # This is the constant offset for aligning with the physics element
        # This is a 4x4 opengl style matrix, expressing an offset and a rotation
        offset = (0,0,0)
        rot    = calcRotMatrix( (0,0,1), 0 )
        body.glObjOffset = makeOpenGLMatrix( rot, offset, (1.0,1.0,1.0) )
        body.setPosition( pos )
        self.bodies.append(body)

        return body, geom
    def createBoxGeom( self, sizes=(1.0,1.0,1.0) ):
        return ode.GeomBox(self.space, sizes)
    def createCapsuleGraphic( self, p1, p2, radius=0.03, detail=3 ):
        """
        Creates a capsule graphic entity... does not exist in the physics
        engine, only graphical.
        """
        # define body rotation automatically from body axis
        relative_v = sub3(p2,p1)
        capsule_len = len3(relative_v)
        #Protect against someone feeding in the same point twice
        if capsule_len < 1e-5:
            return
        za = div3(relative_v, capsule_len)
        if (abs(dot3(za, (1.0, 0.0, 0.0))) < 0.7): xa = (1.0, 0.0, 0.0)
        else: xa = (0.0, 1.0, 0.0)
        ya = cross(za, xa)
        xa = norm3(cross(ya, za))
        ya = cross(za, xa)
        rot = (xa[0], ya[0], za[0], xa[1], ya[1], za[1], xa[2], ya[2], za[2])
        p = p1
        gl_matrix = makeOpenGLMatrix(rot, p)
        glLibColor((255,0,0))
        gl_obj = glLibObjCapsule( radius, capsule_len, detail )
        gl_obj.gl_matrix = gl_matrix
        self.graphics.append(gl_obj)

