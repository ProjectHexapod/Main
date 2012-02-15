#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#e             - Cycles among repeating, mirrored repeating, and clamped egdes
#a             - Toggles anisotropic filtering
#f             - Toggles bilinear filtering
#m             - Cycles among normal, mippmapped, and blended mipmap modes
#LCLICK + DRAG - Rotate camera
#SROLL WHEEL   - Zoom

#Theory:
#As you should already know, texturing maps images onto 3D objects.  The
#pattern on the spaceship in the first tutorial shows this.  Textures can
#be filtered and/or mipmapped to improve their appearance.  Textures'
#edges can be adjusted to change their effect.  OpenGL library provides
#access to all these features.

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, Plane, Plane2, FloorTexture, CameraRotation, CameraRadius, Light1, Shader
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,200)

    #Load a texture.  
    FloorTexture = glLibTexture2D("data/floor2.png",[0,0,512,512],GLLIB_RGBA)

    #Make a plane of size 6.  The normal points up,
    #so the plane will be horizontal.  It will be
    #textured with FloorTexture, tiled 3 times.
    Plane = glLibPlane(6,(0,1,0),FloorTexture,3)

    #Add variables for the camera's rotation and radius
    CameraRotation = [90,23]
    CameraRadius = 5.0

    glEnable(GL_LIGHTING)
    Light1 = glLibLight(1)
    Light1.set_pos([0,10,0])
    Light1.enable()

    pygame.mouse.get_rel()

def quit():
    global Light1
    glDisable(GL_LIGHTING)
    del Light1

filtering = False
mipmapping = False
anisotropy = None
edge = GLLIB_REPEAT
def GetInput():
    global CameraRadius, FloorTexture
    global edge, filtering, mipmapping, anisotropy
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_e:
                if edge == GLLIB_CLAMP: edge = GLLIB_REPEAT
                elif edge == GLLIB_REPEAT: edge = GLLIB_MIRROR_REPEAT
                elif edge == GLLIB_MIRROR_REPEAT: edge = GLLIB_CLAMP
                FloorTexture.edge(edge)
            elif event.key == K_a:
                if   anisotropy == None: anisotropy = GLLIB_MAX
                else                   : anisotropy = None
                FloorTexture.anisotropy(anisotropy)
            elif event.key == K_f:
                if   filtering == False: filtering = GLLIB_FILTER
                else                   : filtering = False
                FloorTexture.filtering(filtering,mipmapping)
            elif event.key == K_m:
                if   mipmapping == False             : mipmapping = GLLIB_MIPMAP
                elif mipmapping == GLLIB_MIPMAP      : mipmapping = GLLIB_MIPMAP_BLEND
                elif mipmapping == GLLIB_MIPMAP_BLEND: mipmapping = False
                FloorTexture.filtering(filtering,mipmapping)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 5: CameraRadius += .4
            if event.button == 4: CameraRadius -= .4
    #If the left mouse button is clicked,
    #rotate the camera.  
    if mpress[0]:
        CameraRotation[0] += mrel[0]
        CameraRotation[1] += mrel[1]

def Draw(Window):
    #Set the window's clear color
    Window.set_clear_color((0.5,0.5,0.5))
    #Clear the window
    Window.clear()
    #Reset the window's clear color for other tutorials
    Window.set_clear_color((0.0,0.0,0.0))
    
    View3D.set_view()
    #Calculate the camera's position using CameraRotation.
    #Basically just spherical coordinates.
    camerapos = [0 + CameraRadius*cos(radians(CameraRotation[0]))*cos((radians(CameraRotation[1]))),
                 0 + CameraRadius*sin((radians(CameraRotation[1]))),
                 0 + CameraRadius*sin(radians(CameraRotation[0]))*cos((radians(CameraRotation[1])))]
    gluLookAt(camerapos[0],camerapos[1],camerapos[2], 0,0,0, 0,1,0)
    Light1.set()
    
    #Draw the panels
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_NOTEQUAL,0.0)
    glTranslatef(0,-2.0,0)
    Plane.draw()
    glTranslatef(0,2.0,0)
    Plane.draw()
    glDisable(GL_ALPHA_TEST)

    #Draw the texture edges of the panels
    #   Draw as lines
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    #   Big lines
    glLineWidth(4)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glColor3f(0,0,0)
    for y in [-2.0,0.0]:
        for x in [-4.0,0.0,4.0]:
            for z in [-4.0,0.0,4.0]:
                glPushMatrix()
                glTranslatef(x,y,z)
                glScalef(*[1.0/3.0]*3)
                Plane.draw()
                glPopMatrix()
    glColor3f(1,1,1)
    glEnable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    #Reset line width
    glLineWidth(1)
    #   Draw as solid faces
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

##    glLibUseShader(None)

    Window.flip()
