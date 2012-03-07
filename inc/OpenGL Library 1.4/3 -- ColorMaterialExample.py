import pygame
from pygame.locals import *
import sys
from OpenGLLibrary import *

pygame.init()

Screen = (800,600)
Window = glLibWindow(Screen,caption="Color Material Test")
View3D = glLibView3D((0,0,Screen[0],Screen[1]),45)
View3D.set_view()

glLibColorMaterial(True)

drawing = 0
Objects = [glLibObjCube(),glLibObjTeapot(),glLibObjSphere(64),glLibObjCylinder(0.5,1.0,64),glLibObjCone(0.5,1.8,64)]

yrot = 0
xrot = 0
while True:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RETURN:
                drawing += 1
                if drawing == 5:
                    drawing = 0
            if event.key == K_1: glLibColor((255,255,255))
            if event.key == K_2: glLibColor((255,0,0))
            if event.key == K_3: glLibColor((255,128,0))
            if event.key == K_4: glLibColor((255,255,0))
            if event.key == K_5: glLibColor((0,255,0))
            if event.key == K_6: glLibColor((0,0,255))
            if event.key == K_7: glLibColor((128,0,255))
            
    Window.clear()
    Objects[drawing].draw([0,-0.5,-6],[[0,yrot,0],[xrot,0,0]])
    Window.flip()

    yrot += 1
    yrot = yrot % 360
    xrot += 0.5
    xrot = xrot % 360
