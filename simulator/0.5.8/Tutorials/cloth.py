#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#v             - Cycles among solid, line, and point rendering of the cloth
#1             - Toggles the red light
#2             - Toggles the green light
#3             - Toggles the blue light
#LEFT          - Add a leftward (from the camera's perspective) force
#RIGHT         - Add a rightward (from the camera's perspective) force
#UP            - Add an upward (from the camera's perspective) force
#DOWN          - Add a downward (from the camera's perspective) force
#Any other key - Reset cloth
#LCLICK + DRAG - Rotate camera
#RCLICK + DRAG - Move mouse-moveable obstacle
#SROLL WHEEL   - Zoom

#Theory:
#Cloth is a fascinating effect.  OpenGL Library provides a built-in
#GPU cloth implementation.  All the updating and collision is done
#on the graphics card, meaning that very high detail is practical.
#The physics of the cloth are the "ball and spring" model, which
#defines a simulation based on using particles connected by
#"springs", which try to keep them a certain distance apart.
#Because the mesh is rectangular, on would normally use many quad
#strips.  The cloth, however, is drawn as a single quad strip for
#efficiency.  The different rows of the cloth are accomplished by
#"splitting" the quadstrip with a quadrilateral that has no area.
#The quadrilateral is called a "degenerate polygon".  This
#quadrilateral cannot be seen, so the appearance of a mesh is
#preserved.  You can see it in line mode, though.

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D
    global Cloth, ClothDrawStyle
    global CameraRotation, CameraRadius
    global Light1, Light2, Light3
    global box, sphere1, sphere2, collision_plane
    global LightsEnabled, mouse_obstacle_pos
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    #The size of the vertex grid is 80 by 80.
    #Thus, the cloth will be made of a mesh
    #of 79 polygons on a side.
    x_size,z_size = 80,80
    #The strength of the restitution force of
    #the cloth (strength with which the cloth
    #tries to go back to its old position.
    #Higher means more jitter between simulation
    #steps.  Lower means lower.  This is factored
    #into "steps" below.
    tensor = 1.0
    #The number of simulation steps per
    #Cloth.update() function.
    steps = rndint(tensor*2.0*(x_size/40.0))
    
    #Create a set of positional data for the
    #cloth.  Red channel stores x position.
    #Green channel stores height.  Blue
    #channel stores z position.  Alpha stores
    #whether the cloth is restrained.  (255
    #means the vertex is restrained, and so
    #it never moves.  
    pos_surf = pygame.Surface((x_size,z_size)).convert_alpha()
    pos_surf.lock()
    for x in xrange(x_size):
        for z in xrange(z_size):
            restrained = 0
            restrained_coordinates = []
            for coord in [[0,z_size-1],[x_size-1,0],[x_size-1,z_size-1]]: restrained_coordinates.append(coord)
            for coord in [[x_size/2,0],[0,z_size/2],[x_size-1,z_size/2]]: restrained_coordinates.append(coord)
            x_pos = rndint(255.0*(x/float(x_size-1.0)))
            y_pos = 255
            z_pos = rndint(255.0*(z/float(z_size-1.0)))
            if [x,z] in restrained_coordinates: restrained = 255
            pos_surf.set_at((x,z),(x_pos,y_pos,z_pos,restrained))
    pos_surf.unlock()
    
    #Create a cloth object
    Cloth = glLibCloth((x_size,z_size),pos_surf)
    #Sets the dampening of the cloth.  1.0
    #means 100% efficiency, and so things can
    #go out of control.  Default is 0.98.
    Cloth.set_dampening(0.99)
    #Sets the time each simulation step covers.
    Cloth.set_time_step(1.0/steps)
    #Sets the number of steps per call to
    #Cloth.update().
    Cloth.set_steps(steps)
    #Add a spherical obstacle at [0.0,0.4,0.0] of
    #radius 0.4.
    Cloth.add_obstacle("middle",[0,0.4,0],GLLIB_OBSTACLE_SPHERE,0.4)
    #Sets the gravity.  In actuality, this can be
    #any force that is applied every frame.
    Cloth.set_gravity([0.0,-1.0,0.0])
    #Loads a texture to map onto the cloth object.
    #The appearance of the cloth is a multiplication
    #of the current material and the texture.  If no
    #texture is set, the cloth is simply drawn like
    #the current material.
    texture = glLibTexture2D("data/cloth.png",GLLIB_ALL,GLLIB_RGB,GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    if GLLIB_ANISOTROPY_AVAILABLE:
        texture.anisotropy(GLLIB_MAX)
    #Sets the texture on the cloth
    Cloth.set_texture(texture)
    #Sets the number of times the texture is repeated
    #over the cloth object.
    Cloth.set_texture_repeat([1.0,1.0])
    #Set the tensor
    Cloth.set_tensor(tensor)

    #There is an obstacle that can be moved via
    #right click of the mouse.  mouse_obstacle_pos
    #stores this position
    mouse_obstacle_pos = [-0.2,0.6,-0.2]
    #Add an obstacle for the mouse-moveable obstacle
    Cloth.add_obstacle("mouse",mouse_obstacle_pos,GLLIB_OBSTACLE_SPHERE,0.2)
    
    CameraRotation = [-90,23]
    CameraRadius = 4.0
    ClothDrawStyle = 1

    #A reference bounding box of size 1x1x1.
    box = glLibRectangularSolid([0.5]*3)
    #Middle obstacle (for drawing)
    sphere1 = glLibSphere(0.399,32)
    #Mouse-moveable obstacle object (for drawing)
    sphere2 = glLibSphere(0.18,32)
    #Used for moving the mouse_moveable object see
    #GetInput() below for more info.
    collision_plane = glLibPlane(100,[0,1,0])

    glEnable(GL_LIGHTING)
    #Variable to store whether the light is turned on
    LightsEnabled = [True,False,False]
    #Set the lights
    SetLights()

    pygame.mouse.get_rel()
def SetLights():
    global Light1, Light2, Light3
    #Set the lights (turn them all on).
    Light1 = glLibLight(1)
    Light1.set_pos([-0.5,1,-0.5])
    Light1.set_diffuse([1.0,0.5,0.5])
    Light1.set_specular([1.0,0.5,0.5])
    Light1.set_atten(1,4,4)
    Light1.set_type(GLLIB_POINT_LIGHT)
    Light1.enable()

    Light2 = glLibLight(2)
    Light2.set_pos([0,1,0])
    Light2.set_diffuse([0.5,0.5,1.0])
    Light2.set_specular([0.5,0.5,1.0])
    Light2.set_atten(1,4,4)
    Light2.set_type(GLLIB_POINT_LIGHT)
    Light2.enable()
    
    Light3 = glLibLight(3)
    Light3.set_pos([0.5,1,0.5])
    Light3.set_diffuse([0.5,1.0,0.5])
    Light3.set_specular([0.5,1.0,0.5])
    Light3.set_atten(1,4,4)
    Light3.set_type(GLLIB_POINT_LIGHT)
    Light3.enable()
    
    #Zero the ones that are off (make them
    #have no effect).  
    if not LightsEnabled[0]: Light1.zero()
    if not LightsEnabled[1]: Light2.zero()
    if not LightsEnabled[2]: Light3.zero()

def quit():
    global Light1, Light2, Light3, Cloth
    glDisable(GL_LIGHTING)
    
    #Reset default material
    glLibUseMaterial(GLLIB_MATERIAL_DEFAULT)

    del Light1, Light2, Light3
    del Cloth
def GetInput():
    global mouse_obstacle_pos, LightsEnabled
    global CameraRadius, ClothDrawStyle
    mrel = pygame.mouse.get_rel()
    mpos = pygame.mouse.get_pos()
    mpress = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4: CameraRadius -= 0.3
            elif event.button == 5: CameraRadius += 0.3
        elif event.type == KEYDOWN:
            #If ESCAPE, quit.
            if event.key == K_ESCAPE: return False
            #If LEFT, RIGHT, UP or DOWN are pressed, ignore, handle below
            elif event.key in [K_LEFT,K_RIGHT,K_UP,K_DOWN]: pass
            #If "v" is pressed, cycle among solid, line, and point renderings
            elif event.key == K_v:
                ClothDrawStyle += 1
                if ClothDrawStyle == 4: ClothDrawStyle = 1
            #If "1" is pressed, toggle the first light's effect, and set all the lights
            elif event.key in [K_1,K_KP1]:
                LightsEnabled[0] = not LightsEnabled[0]
                SetLights()
            #If "2" is pressed, toggle the second light's effect, and set all the lights
            elif event.key in [K_2,K_KP2]:
                LightsEnabled[1] = not LightsEnabled[1]
                SetLights()
            #If "3" is pressed, toggle the third light's effect, and set all the lights
            elif event.key in [K_3,K_KP3]:
                LightsEnabled[2] = not LightsEnabled[2]
                SetLights()
            #Any other key resets the cloth
            else: Cloth.reset()
    #If left mouse button, rotate the camera by the mouse's movement.
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]
    #If right mouse button, move the move-movable obstacle by the mouse's movement.
    if mpress[2]:
        #This is a separate pass that makes a new scene, then draws a plane at the
        #height of the obstacle.  The mouse can then be tested against this plane to
        #determine the position of the mouse in 3D space.  The mouse-movable object
        #is then moved to that position (note that because the plane is at a certain
        #height, the move-movable obstacle moves in the XZ plane).  All this
        #effectively places the obstacle directly below the mouse for the user's
        #convenience.  Don't move the obstacle too quickly, or the simulation won't
        #be able to keep up!  Also, don't sandwich the cloth between obstacles, or
        #the cloth will get confused and have issues rearranging itself.
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        View3D.set_view()
        SetCamera()
        glPushMatrix()
        glTranslatef(0.0,0.6,0.0)
        collision_plane.draw()
        glPopMatrix()
        mouse_obstacle_pos = glLibGetPosAt(mpos)
        #Keep the obstacle inside the bounding box
        mouse_obstacle_pos = clamp(mouse_obstacle_pos,-1.0,1.0)
        #Move the obstacle to this position
        Cloth.move_obstacle("mouse",mouse_obstacle_pos)
    #Adds a force for one round of simulation only.  In this case, a force in the XZ
    #plane.  The force is defined from the camera's perspective for the user's convenience.
    simulation_move = 0.0
    angle = 0.0
    if key[K_LEFT ]: simulation_move = 1.0; angle = 90.0
    if key[K_RIGHT]: simulation_move = 1.0; angle = -90.0
    if key[K_UP   ]: simulation_move = 1.0; angle = 180.0
    if key[K_DOWN ]: simulation_move = 1.0; angle = 0.0
    if simulation_move == 1.0:
        x_part = simulation_move*cos(radians(CameraRotation[0]+angle))
        z_part = simulation_move*sin(radians(CameraRotation[0]+angle))
        Cloth.add_force([x_part,0.0,z_part])
def SetCamera():
    position = [0.0 + CameraRadius*cos(radians(CameraRotation[0]))*cos(radians(CameraRotation[1])),
                0.4 + CameraRadius*sin(radians(CameraRotation[1])),
                0.0 + CameraRadius*sin(radians(CameraRotation[0]))*cos(radians(CameraRotation[1]))]
    gluLookAt(position[0],position[1],position[2], 0.0,0.4,0.0, 0,1,0)
def Draw(Window):
    Cloth.update()
    
    Window.clear()
    View3D.set_view()

    SetCamera()
    Light1.set()
    Light2.set()
    Light3.set()
    
    #Box, for reference
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glColor3f(0.1,0.1,0.1)
    for x in [-0.5,0.5]:
        for y in [-0.5,0.5]:
            for z in [-0.5,0.5]:
                glTranslatef(x,y,z)
                box.draw()
                glTranslatef(-x,-y,-z)
    glColor3f(1,1,1)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    glEnable(GL_LIGHTING)

    #Spherical (middle) obstacle
    glPushMatrix()
    glTranslatef(0.0,0.4,0.0)
    sphere1.draw()
    glPopMatrix()

    #Spherical mouse-moveable object
    glPushMatrix()
    glTranslatef(*mouse_obstacle_pos)
    sphere2.draw()
    glPopMatrix()
    glEnable(GL_TEXTURE_2D)

    #Draw the lights as points
    if LightsEnabled[0]: Light1.draw_as_point(10)
    if LightsEnabled[1]: Light2.draw_as_point(10)
    if LightsEnabled[2]: Light3.draw_as_point(10)

    #Cloth
    if ClothDrawStyle == 1:
        glLibUseMaterial(GLLIB_MATERIAL_DEFAULT)
        Light1.set_ambient([0.2,0.2,0.2])
        #Draws the cloth, using instructions for Light1, Light2, and Light3.
        Cloth.draw(numlights=3)
    elif ClothDrawStyle == 2:
        #Because lines are harder to see, just make the ambient 100% (i.e., just
        #draw the texture only.
        glLibUseMaterial(GLLIB_MATERIAL_FULL)
        Light1.set_ambient([1.0,1.0,1.0])
        #Draws the cloth as lines of thickness 2, using instructions for Light1, Light2, and Light3.
        Cloth.draw_lines(2,numlights=3)
    elif ClothDrawStyle == 3:
        #Because points are harder to see, just make the ambient 100% (i.e., just
        #draw the texture only.
        glLibUseMaterial(GLLIB_MATERIAL_FULL)
        Light1.set_ambient([1.0,1.0,1.0])
        #Draws the cloth as points of size 3, using instructions for Light1, Light2, and Light3.
        Cloth.draw_points(3,numlights=3)

    Window.flip()
