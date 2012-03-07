from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from pygame.locals import *
import os, sys
from OpenGLLibrary import *

pygame.init()
glutInit([])

Screen = (800,600)

Window = glLibWindow(Screen,caption="Shadowing Test",multisample=True)
View3D = glLibView3D((0,0,Screen[0],Screen[1]),65)
View3D.set_view()

LightFocus = [0,0,0]
LightColor = (255,255,255)
ShadowColor = (153,153,153)
ShadowMapSize = 512

Camera = glLibCamera([22,28,-18],[0,0,0])

glLibTexturing(True)

glLibLighting(True)
Sun = glLibLight([0,20.0,10],Camera,color=LightColor,diffusecolor=ShadowColor)
Sun.enable()

Objects = [glLibObjFromFile("ExamplesData/Spikey.obj"),
           glLibObjFromFile("ExamplesData/UberBall.obj"),
           glLibObjTeapot(),
           glLibObjCylinder(0.5,1.0,64),
           glLibObjSphere(64),
           glLibObjCube()]

Mesh = []
heightmap = pygame.image.load(os.path.join("ExamplesData","heightmap.jpg"))
for x in xrange(heightmap.get_height()):
    xrow = []
    for y in xrange(heightmap.get_height()):
        color = heightmap.get_at((x,y))
        height = color[0]*0.01
        xrow.append(height)
    Mesh.append(xrow)

Map = glLibObjMap(Mesh,texturing=False,normals=GLLIB_VERTEX_NORMALS,heightscalar=2.5)

glLibShadowInit([[ShadowMapSize,5]])

def RenderFloor():
    Map.draw([12,0,30],[[0,150,0]])
objpos = [2,10,2]
objectdrawing = 0
def RenderObj():
    Objects[objectdrawing].draw([objpos[0],objpos[1],objpos[2]],scalar=1.0)
def GetInput():
    global CameraRotation, LightPosition, objpos, objectdrawing
    mpress = pygame.mouse.get_pressed()
    mrel = pygame.mouse.get_rel()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN:
            objectdrawing += 1
            if objectdrawing == 6:
                objectdrawing = 0
    if mpress[0]:
        objpos[0] -= 0.1*mrel[0]
        objpos[2] -= 0.1*mrel[1]
    if mpress[2]:
        formerpos = Sun.get_pos()
        Sun.change_pos([formerpos[0]-0.1*mrel[0],formerpos[1],formerpos[2]-0.1*mrel[1]])
def Update():
    Camera.update()
def Draw():
    global LightFocus
    #Clear
    Window.clear()
    #glLib step 1
    LightPosition = Sun.get_pos()
    LightFocus = [objpos[0],objpos[1],objpos[2]]
    dist = sqrt(((LightFocus[0]-LightPosition[0])**2)+((LightFocus[1]-LightPosition[1])**2)+((LightFocus[2]-LightPosition[2])**2))
    lightangle = degrees(2*asin((2.9*1.0)/dist))
    near = dist - 2.9
    far = dist + 2.9
    glLibCreateShadowBefore(GLLIB_SHADOW_MAP1,LightPosition,LightFocus,lightviewangle=lightangle,near=near,far=far)
    #Render all objects that should cast shadows
    RenderObj()
    #glLib step 2
    glLibCreateShadowAfter(GLLIB_SHADOW_MAP1)

    #Clear
    Window.clear()
    #Position the camera
    View3D.set_view()
    Camera.set_camera()
    #Set the light
    Sun.change_color((153,153,153))
    Sun.change_diffuse_color((255,255,255))
    Sun.draw()
    Sun.draw_as_point()
    #Render everything
    RenderObj()
    RenderFloor()
    
    #glLib step 3
    glLibRenderShadowCompareBefore(GLLIB_SHADOW_MAP1)
    #Set light color to shadow color
    Sun.change_diffuse_color(ShadowColor)
    #Render all objects where shadows should be cast
    RenderObj()
    RenderFloor()
    #glLib step 4
    glLibRenderShadowCompareAfter()
    
    #Flip
    Window.flip()
def main():
    while True:
        GetInput()
        Update()
        Draw()
if __name__ == '__main__': main()
