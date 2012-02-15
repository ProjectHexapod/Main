from OpenGL.GL import *
from OpenGL.GLU import *
import glLibViewport
import glLibInit
from glLibLocals import *
import pygame
from pygame.locals import *
pygame.init()
class glLibWindow:
    def __init__(self,size,fullscreen=False,icon=None,caption="glLib Window",multisample=False):
        self.size = size
        if icon == None:icon = pygame.Surface((1,1)); icon.set_alpha(0)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(caption)
        self.multisample = multisample
        self.fullscreen = fullscreen
        if self.multisample:pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS,1)
        else:pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS,0)
        self.set_fullscreen(self.fullscreen)
        self.clear_color = (0,0,0)
        glLibInit.glLibInitialize()
    def clear(self,color=(0,0,0)):
        if self.clear_color != color:
            glClearColor(color[0]/255.0,color[1]/255.0,color[2]/255.0,1.0)
            self.clear_color = (color[0],color[1],color[2])
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
    def flip(self):
        pygame.display.flip()
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.set_fullscreen(self.fullscreen)
    def set_fullscreen(self,value):
        if value:self.screenflags = OPENGL|DOUBLEBUF|FULLSCREEN; self.fullscreen = True
        else:self.screenflags = OPENGL|DOUBLEBUF; self.fullscreen = False
        pygame.display.set_mode(self.size,self.screenflags)
class glLibView2D():
    def __init__(self,rect,near=-10,far=10.0):
        self.rect = rect
        self.near = near
        self.far = far
    def set_near(self,value):
        self.near = value
    def set_far(self,value):
        self.far = value
    def set_view(self):
        glLibViewport.viewport2D(self.rect,self.near,self.far)
class glLibView3D():
    def __init__(self,rect,angle,near=0.1,far=1000.0):
        self.rect = rect
        self.angle = angle
        self.type = type
        self.near = near
        self.far = far
    def set_angle(self,value):
        self.angle = angle
    def set_near(self,value):
        self.near = value
    def set_far(self,value):
        self.far = value
    def set_view(self):
        glLibViewport.viewport3D(self.rect,self.angle,self.near,self.far)
