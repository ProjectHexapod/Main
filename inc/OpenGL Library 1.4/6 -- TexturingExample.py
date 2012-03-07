import pygame
from pygame.locals import *
import sys
from OpenGLLibrary import *
from OpenGL.GLUT import *

pygame.init()
glutInit()

Screen = (800,600)
Window = glLibWindow(Screen,caption="Texturing Test")
View3D = glLibView3D((0,0,Screen[0],Screen[1]),45)
View3D.set_view()

glLibTexturing(True)

Camera = glLibCamera([0,0.5,6],[0,0,0])

glLibLighting(True)
Sun = glLibLight([0,100,0],Camera)
Sun.enable()

drawing = 0
Objects = [glLibObjTexSphere(0.5,64),glLibObjTexCylinder(0.5,1.0,64),glLibObjTexCone(0.5,1.0,64)]

Texture = glLibTexture("ExamplesData/fugu.png")

def GetInput():
    global drawing
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
                if drawing == 3:
                    drawing = 0
    if   key[K_LEFT]: Camera.set_target_pos([-6,0.5,0])
    elif key[K_RIGHT]: Camera.set_target_pos([6,0.5,0])
    elif key[K_UP]: Camera.set_target_pos([0,6,2])
    elif key[K_DOWN]: Camera.set_target_pos([0,-6,2])
    else: Camera.set_target_pos([0,0.5,6])
def Update():
    Camera.update()
def Draw():
    Window.clear()
    Camera.set_camera()
    Sun.draw()
    for x in xrange(-2,2+1,2):
        for y in xrange(-2,2+1,2):
            for z in xrange(-2,2+1,2):
                Objects[drawing].draw([x,y,z])
    Window.flip()
def main():
    while True:
        GetInput()
        Update()
        Draw()
if __name__ == '__main__': main()
