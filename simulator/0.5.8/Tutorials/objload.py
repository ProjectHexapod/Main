#Tutorial by Ian Mallett

#All tutorials will have the following functions:

#init() -> sets up the scene and any necessary variables
#quit() -> called at exit; cleans up
#GetInput() -> handle's the user's input
#Draw(Window) -> draws the scene


#The main file (Tutorial.py) runs all tutorials like:

#init()
#while True:
#    GetInput()
#    Draw(Window)
#quit()


#Each tutorial builds upon the last.  New or different
#lines will be commented.  Lines described in earlier
#tutorials will not.  Comments go directly above the
#lines they describe.  It is recommended that the
#tutorials be read in order.

#Every tutorial will also have a controls list.

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate spaceship

#Every tutorial will also have a theory section.

#Theory:
#glLibObject(...) loads a .obj file, which stores
#geometric data, returning an object.  The object can
#then be drawn via object.draw_arrays(...).  Calling
#object.build_list() and/or object.build_vbo() allows
#the object to be drawn with a display list or a vertex
#buffer object.

#Allow access to OpenGL Library
import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
#Import OpenGL Library
from glLib import *

#init() -> sets up the scene and any necessary variables
def init(Screen):
    global View3D, Spaceship, SpaceshipRotation, Light1
    #Creates a view.  This is a perspective view, with a viewport as big
    #as the Screen, an angle of 45 degrees, and some clipping planes.
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    #Loads a spaceship from:
    #data/objects/Spaceship.obj
    #data/objects/Spaceship.mtl
    Spaceship = glLibObject("data/objects/Spaceship.obj",GLLIB_FILTER,GLLIB_MIPMAP_BLEND)
    #Build a display list from the data
    Spaceship.build_list()
    #Build a vertex buffer object from the data
    if GLLIB_VBO_AVAILABLE: Spaceship.build_vbo()

    #After this tutorial, it is assumed
    #Vertex Buffer Objects are available.
    #Future tutorials will crash if it is
    #NOT available.  Install both NumPy
    #and Numeric for best results.

    #Variable for the spaceship's rotation
    SpaceshipRotation = [0,0]

    #Enable lighting
    glEnable(GL_LIGHTING)
    #Instance of a light.
    Light1 = glLibLight(1)
    #Set the position to be far overhead
    Light1.set_pos([0,100,0])
    #Enable the light
    Light1.enable()

    #Call the get_rel function to set it equal to
    #0 the next time it is called in GetInput()
    pygame.mouse.get_rel()

#quit() -> called at exit; cleans up
def quit():
    global Light1, Spaceship
    #Disable lighting
    glDisable(GL_LIGHTING)
    #Delete the light
    del Light1
    #Delete the spaceship's vertex buffer
    #objects so no exception is thrown
    if GLLIB_VBO_AVAILABLE: del Spaceship

#GetInput() -> handle's the user's input
def GetInput():
    #Get the relative motion and button state of the mouse
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        #Pressing the "X" on the window exits the demo
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        #ESCAPE returns to menu
        if event.type == KEYDOWN and event.key == K_ESCAPE: return False
    #If the mouse is pressed, rotate the spaceship
    #by the amount the mouse was moved
    if mpress[0]:
        SpaceshipRotation[0] += mrel[0]
        SpaceshipRotation[1] += mrel[1]

#Draw(Window) -> draws the scene
def Draw(Window):
    #Clear the window
    Window.clear()
    #Set the view
    View3D.set_view()
    #Set the camera to (0,3,5) looking at (0,0,0) with a "up" vector pointing up (0,1,0)
    gluLookAt(0,3,5, 0,0,0, 0,1,0)
    #Set the light into the scene
    Light1.set()

    #Rotate the spaceship by our rotation amount
    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
##    Spaceship.draw_arrays() #often slowest, but requires no other functions
##    Spaceship.draw_list() #often faster, but requires .build_list() (line 43)
    if GLLIB_VBO_AVAILABLE:
        Spaceship.draw_vbo() #often fastest, but requires .build_vbo() (line 45)
    else:
        Spaceship.draw_list()

    #Flip the buffer to the screen so that we see it
    Window.flip()
