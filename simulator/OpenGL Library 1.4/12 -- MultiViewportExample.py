import pygame
from pygame.locals import *
import sys
from OpenGLLibrary import *

pygame.init()

Screen = (800,600)
Window = glLibWindow(Screen,caption="MultiViewport Test")
ViewBottomLeft = glLibView3D((0,0,Screen[0]/2,Screen[1]/2),45)
ViewTopLeft = glLibView3D((0,Screen[1]/2,Screen[0]/2,Screen[1]/2),45)
ViewRight = glLibView3D((Screen[0]/2,0,Screen[0]/2,Screen[1]),45)

glLibTexturing(True)

TopLeftCamera = glLibCamera([4.5,3,12],[4.5,0,4.5])
BottomLeftCamera = glLibCamera([0,0.5,4],[0,0,0])
RightCamera = glLibCamera([27,28,65],[12,0,0])

glLibLighting(True)
TopLeftSun = glLibLight([0,100,0],TopLeftCamera)
TopLeftSun.enable()
BottomLeftSun = glLibLight([0,100,0],TopLeftCamera)
BottomLeftSun.enable()
RightSun = glLibLight([0,15,0],TopLeftCamera)
RightSun.enable()

glLibShadowInit([[512,5]])

texsph = glLibObjTexSphere(0.5,32)
spikey = glLibObjFromFile("ExamplesData/Spikey.obj")

Mesh = [[0.0,0.1,0.2,0.3,0.2,0.2,0.3,0.2,0.1],[0.1,0.2,0.3,0.4,0.5,0.4,0.3,0.2,0.1],[0.1,0.1,0.2,0.2,0.3,0.2,0.3,0.2,0.1],[0.0,0.0,0.1,0.1,0.2,0.1,0.2,0.1,0.1],[0.1,0.0,0.1,0.2,0.2,0.3,0.3,0.2,0.0],[0.0,0.1,0.2,0.3,0.2,0.2,0.3,0.2,0.1],[0.0,0.1,0.2,0.3,0.2,0.2,0.3,0.2,0.1],[0.2,0.3,0.2,0.3,0.3,0.4,0.3,0.2,0.0],[0.4,0.5,0.3,0.4,0.2,0.2,0.5,0.2,0.1]]
Texture = glLibTexture("ExamplesData/fugu.png")
Map = glLibObjMap(Mesh,texturing=Texture,normals=GLLIB_FACE_NORMALS,heightscalar=2.5)

Mesh = []
heightmap = pygame.image.load(os.path.join("ExamplesData","heightmap.jpg"))
for x in xrange(heightmap.get_height()):
    xrow = []
    for y in xrange(heightmap.get_height()):
        xrow.append(heightmap.get_at((x,y))[0]*0.01)
    Mesh.append(xrow)
Map2 = glLibObjMap(Mesh,texturing=False,normals=GLLIB_VERTEX_NORMALS,heightscalar=2.5)

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
    if   key[K_LEFT]:
        TopLeftCamera.set_target_pos([0,3,12])
        BottomLeftCamera.set_target_pos([-2,-0.5,2])
        RightCamera.set_target_pos([-3,28,65])
    elif key[K_RIGHT]:
        TopLeftCamera.set_target_pos([9,3,12])
        BottomLeftCamera.set_target_pos([2,-0.5,2])
        RightCamera.set_target_pos([54,28,65])
    elif key[K_UP]:
        TopLeftCamera.set_target_pos([4.5,6,7])
        BottomLeftCamera.set_target_pos([0,1,2])
        RightCamera.set_target_pos([27,56,50])
    elif key[K_DOWN]:
        TopLeftCamera.set_target_pos([4.5,-1,10])
        BottomLeftCamera.set_target_pos([0,-5,2])
        RightCamera.set_target_pos([18,14,35])
    else:
        TopLeftCamera.set_target_pos([4.5,3,12])
        BottomLeftCamera.set_target_pos([0,0.5,4])
        RightCamera.set_target_pos([27,28,65])
def Update():
    TopLeftCamera.update()
    BottomLeftCamera.update()
    RightCamera.update()
spikeypos = [15,5,17]
def Draw():
    #Clear
    Window.clear()
    #Right View
    lightpos = RightSun.get_pos()
    dist = sqrt(((spikeypos[0]-lightpos[0])**2)+((spikeypos[1]-lightpos[1])**2)+((spikeypos[2]-lightpos[2])**2))
    lightangle = degrees(2*asin((2.9*1.0)/dist))
    near = dist - 2.9
    far = dist + 2.9
    glLibTexturing(False)
    RightSun.enable()
    glLibCreateShadowBefore(GLLIB_SHADOW_MAP1,lightpos,spikeypos,lightviewangle=lightangle,near=near,far=far)
    spikey.draw(spikeypos)
    glLibCreateShadowAfter(GLLIB_SHADOW_MAP1)
    Window.clear()
    ViewRight.set_view()
    RightCamera.set_camera()
    RightSun.change_color((153,153,153))
    RightSun.change_diffuse_color((255,255,255))
    RightSun.draw()
    RightSun.draw_as_point()
    spikey.draw(spikeypos)
    Map2.draw()
    glLibRenderShadowCompareBefore(GLLIB_SHADOW_MAP1)
    RightSun.change_diffuse_color((128,128,128))
    spikey.draw(spikeypos)
    Map2.draw()
    glLibRenderShadowCompareAfter()
    RightSun.disable()
    glLibTexturing(True)
    #Top Left View
    ViewTopLeft.set_view()
    TopLeftCamera.set_camera()
    TopLeftSun.enable()
    TopLeftSun.draw()
    Map.draw()
    TopLeftSun.disable()
    #Bottom Left View
    ViewBottomLeft.set_view()
    BottomLeftCamera.set_camera()
    BottomLeftSun.enable()
    BottomLeftSun.draw()
    for x in range(-1,1+1,2):
        for y in range(-1,1+1,2):
            for z in range(-1,1+1,2):
                texsph.draw([x*0.6,y*0.6,z*0.6])
    BottomLeftSun.disable()
    
    #Flip
    Window.flip()
def main():
    while True:
        GetInput()
        Update()
        Draw()
if __name__ == '__main__': main()
