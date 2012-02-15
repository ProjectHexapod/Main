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

Window = glLibWindow(Screen,caption="MultiShadowing Test",multisample=True)
View3D = glLibView3D((0,0,Screen[0],Screen[1]),65)
View3D.set_view()

numlights = 3
ShadowMapSize = 512

brightness = 255.0/numlights
shadowcolor = 100.0/numlights

LightColor = (brightness,brightness,brightness)
ShadowColor = (shadowcolor,shadowcolor,shadowcolor)

Camera = glLibCamera([22,28,-18],[0,0,0])

glLibTexturing(True)
glLibLighting(True)

Lights = []
for l in xrange(numlights):
    Light = glLibLight([2,20.0,-4+(l*1)],Camera,color=LightColor,diffusecolor=ShadowColor)
    Light.enable()
    Lights.append(Light)
shadowmaps = []
for l in xrange(len(Lights)):
    shadowmaps.append([ShadowMapSize,5])
glLibShadowInit(shadowmaps)

Spikey = glLibObjFromFile("ExamplesData/Spikey.obj")

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

def RenderFloor():
    Map.draw([12,0,30],[[0,150,0]])
objpos = [2,10,2]
def RenderObj():
    Spikey.draw([objpos[0],objpos[1],objpos[2]],scalar=1.0)
dragging = []
def GetInput():
    global objpos, dragging
    mpress = pygame.mouse.get_pressed()
    mrel = pygame.mouse.get_rel()
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key[K_ESCAPE]:
            pygame.quit(); sys.exit()
    got = False
    if mpress[0]:
        cursor_pos = glLibUnProject(pygame.mouse.get_pos())
        lnum = 0
        if dragging != []: got = True
        for l in Lights:
            light_pos = l.get_pos()
            if sqrt(((cursor_pos[0]-light_pos[0])**2)+((cursor_pos[1]-light_pos[1])**2)+((cursor_pos[2]-light_pos[2])**2)) < 0.2:
                dragging.append(lnum)
                got = True
            lnum += 1
    if not got:
        dragging = []
    if dragging != []:
        for lnum in dragging:
            light = Lights[lnum]
            light_pos = light.get_pos()
            light.change_pos([light_pos[0]-0.02*mrel[0],light_pos[1],light_pos[2]-0.02*mrel[1]])
    if mpress[2]:
        objpos[0] -= 0.1*mrel[0]
        objpos[2] -= 0.1*mrel[1]
def Update():
    Camera.update()
def Draw():
    glLibLighting(False)
    for i in xrange(len(Lights)):
        light = Lights[i]
        #Clear
        Window.clear()
        #glLib step 1
        LightPosition = light.get_pos()
        LightFocus = [objpos[0],objpos[1],objpos[2]]
        dist = sqrt(((LightFocus[0]-LightPosition[0])**2)+((LightFocus[1]-LightPosition[1])**2)+((LightFocus[2]-LightPosition[2])**2))
        lightangle = degrees(2*asin((2.9*1.0)/dist))
        near = dist - 2.9
        far = dist + 2.9
        glLibCreateShadowBefore(GLLIB_SHADOW_MAP1+i,LightPosition,LightFocus,lightviewangle=lightangle,near=near,far=far)
        #Render all objects that should cast shadows
        RenderObj()
        #glLib step 2
        glLibCreateShadowAfter(GLLIB_SHADOW_MAP1+i)
    glLibLighting(True)

    #Clear
    Window.clear()
    #Position the camera
    View3D.set_view()
    Camera.set_camera()
    #Set the lights
    for l in Lights:
        l.change_color(LightColor)
        l.draw_as_point(4)
        l.change_color(ShadowColor)
        l.change_diffuse_color(LightColor)
        l.draw()
    #Render everything
    RenderObj()
    RenderFloor()
    #Set light color to shadow color
    for l in Lights:
        l.change_diffuse_color(ShadowColor)
        l.disable()
    
    #glLib step 3
    glLibEnableShadowShading()
    lightnumber = 0
    for l in Lights:
        l.enable()
        glLibRenderShadowCompareBefore(GLLIB_SHADOW_MAP1+lightnumber)
        RenderObj()
        RenderFloor()
        l.disable()
        lightnumber += 1
        
    for l in Lights:
        l.enable()

    glLibDisableShadowShading()
    
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
