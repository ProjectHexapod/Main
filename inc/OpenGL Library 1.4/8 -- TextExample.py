import pygame
from pygame.locals import *
import sys,os
from OpenGLLibrary import *
from OpenGL.GL import *

pygame.init()

Screen = (800,600)
Window = glLibWindow(Screen,caption="Text Test")
View3D = glLibView3D((0,0,Screen[0],Screen[1]),45)
View3D.set_view()

Font = pygame.font.Font(os.path.join("ExamplesData","Lucida Console.ttf"),72)

glLibTexturing(True)

Camera = glLibCamera([0,0,16],[0,0,0])

Hello = glLibObjText("Hello!",Font,(255,255,255))

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
    if   key[K_LEFT]: Camera.set_target_pos([-16,0,0])
    elif key[K_RIGHT]: Camera.set_target_pos([16,0,0])
    else: Camera.set_target_pos([0,0,16])
def Update():
    Camera.update()
def Draw():
    Window.clear()
    Camera.set_camera()
    Hello.draw()
    Window.flip()
def main():
    while True:
        GetInput()
        Update()
        Draw()
if __name__ == '__main__': main()
