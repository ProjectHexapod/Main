#Tutorial by Ian Mallett

#Controls:
#ESC           - Return to menu
#LCLICK + DRAG - Rotate camera

#Theory:
#Loads an object from a .raw file.

import sys,os
sys.path.append(os.path.split(sys.path[0])[0])
from glLib import *

def init(Screen):
    global View3D, Spaceship, SpaceshipRotation, Light1
    View3D = glLibView3D((0,0,Screen[0],Screen[1]),45,0.1,20)

    #Loads a spaceship from:
    #data/objects/Spaceship.raw
    Spaceship = glLibObject("data/objects/Spaceship.raw")
    Spaceship.build_list()
    if GLLIB_VBO_AVAILABLE: Spaceship.build_vbo()

    SpaceshipRotation = [0,-90]

    #Don't enable lighting; .raw can't store
    #normals; lighting wouldn't be accurate.
##    glEnable(GL_LIGHTING) 
##    Light1 = glLibLight(1)
##    Light1.set_pos([0,100,0])
##    Light1.enable()

    pygame.mouse.get_rel()

def quit():
    global Spaceship
    if GLLIB_VBO_AVAILABLE: del Spaceship

def GetInput():
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT: quit(); pygame.quit(); sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE: return False
    if mpress[0]:
        SpaceshipRotation[0] += mrel[0]
        SpaceshipRotation[1] += mrel[1]

def Draw(Window):
    Window.clear()
    View3D.set_view()
    gluLookAt(0,3,5, 0,0,0, 0,1,0)

    glRotatef(SpaceshipRotation[0],0,1,0)
    glRotatef(SpaceshipRotation[1],1,0,0)
##    Spaceship.draw_arrays() #often slowest, but requires no other functions
##    Spaceship.draw_list() #often faster, but requires .build_list() (line 43)
    if GLLIB_VBO_AVAILABLE:
        Spaceship.draw_vbo() #often fastest, but requires .build_vbo() (line 45)
    else:
        Spaceship.draw_list()

    Window.flip()
