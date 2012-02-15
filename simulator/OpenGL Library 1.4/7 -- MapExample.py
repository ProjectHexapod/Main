import pygame
from pygame.locals import *
import sys
from OpenGLLibrary import *

pygame.init()

Screen = (800,600)
Window = glLibWindow(Screen,caption="Map Mesh Test")
View3D = glLibView3D((0,0,Screen[0],Screen[1]),45)
View3D.set_view()

glLibTexturing(True)

Camera = glLibCamera([3,12,18],[3,0,0])

glLibLighting(True)
Sun = glLibLight([3.5,3,3.5],Camera,color=(255,255,255))
Sun.enable()

Mesh = [[0.0,0.1,0.2,0.3,0.2,0.2,0.3,0.2,0.1],
        [0.1,0.2,0.3,0.4,0.5,0.4,0.3,0.2,0.1],
        [0.1,0.1,0.2,0.2,0.3,0.2,0.3,0.2,0.1],
        [0.0,0.0,0.1,0.1,0.2,0.1,0.2,0.1,0.1],
        [0.1,0.0,0.1,0.2,0.2,0.3,0.3,0.2,0.0],
        [0.0,0.1,0.2,0.3,0.2,0.2,0.3,0.2,0.1],
        [0.0,0.1,0.2,0.3,0.2,0.2,0.3,0.2,0.1],
        [0.2,0.3,0.2,0.3,0.3,0.4,0.3,0.2,0.0],
        [0.4,0.5,0.3,0.4,0.2,0.2,0.5,0.2,0.1]]

Texture = glLibTexture("ExamplesData/fugu.png")
Map1 = glLibObjMap(Mesh,texturing=Texture,normals=GLLIB_FACE_NORMALS,heightscalar=2.5)
Map2 = glLibObjMap(Mesh,texturing=Texture,normals=GLLIB_VERTEX_NORMALS,heightscalar=2.5)

rot = [0,0]
drawing = 1
def GetInput():
    global drawing
    key = pygame.key.get_pressed()
    mpress = pygame.mouse.get_pressed()
    mrel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RETURN:
                drawing = 1-(drawing-1)+1
    if   key[K_LEFT]: Camera.set_target_pos([-15,12,3])
    elif key[K_RIGHT]: Camera.set_target_pos([21,12,3])
    else: Camera.set_target_pos([3,12,18])
    if mpress[0]:
        current_pos = Sun.get_pos()
        new_pos = [current_pos[0]+(mrel[0]*0.05),current_pos[1],current_pos[2]+(mrel[1]*0.05)]
        Sun.change_pos(new_pos)
    if mpress[2]:rot[1] += mrel[0]
def Update():
    Camera.update()
def Draw():
    Window.clear()
    
    Camera.set_camera()

    Sun.draw()
    Sun.draw_as_point()
    
    if drawing == 1: Map1.draw([0,0,0],[[0,rot[1],0]])
    if drawing == 2: Map2.draw([0,0,0],[[0,rot[1],0]])
    
    Window.flip()
def main():
    while True:
        GetInput()
        Update()
        Draw()
if __name__ == '__main__': main()
