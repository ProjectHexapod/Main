from OpenGL.GL import *
from OpenGL.GLU import *
import os
import pygame
from pygame.locals import *
from math import *
pygame.init()
def glLibTexturing(value):
    if value:glEnable(GL_TEXTURE_2D)
    else:glDisable(GL_TEXTURE_2D)
def glLibTexture(surface,filters=[],size="automatic"):
    if type(surface) == type(""):
        surface = pygame.image.load(os.path.join(*surface.split("/"))).convert_alpha()
    if surface == None:
        data = surface
    else:
        data = pygame.image.tostring(surface,"RGBA",True)
    if size == "automatic":
        width,height = surface.get_size()
    else:
        width = size[0]
        height = size[1]
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,texture)
    #Format
    InternalFormat = GL_RGBA
    if "depthtex" in filters:
        InternalFormat = GL_DEPTH_COMPONENT
    #Mag filter
    if "filter" in filters: glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    else:                   glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    #Min filter
    if "mipmap" in filters:
        if "mipmap blend" in filters:
            if "filter" in filters: mipmap_param = GL_LINEAR_MIPMAP_LINEAR
            else:                   mipmap_param = GL_NEAREST_MIPMAP_LINEAR
        else:
            if "filter" in filters: mipmap_param = GL_LINEAR_MIPMAP_NEAREST
            else:                   mipmap_param = GL_NEAREST_MIPMAP_NEAREST
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,mipmap_param)
        glPixelStoref(GL_UNPACK_ALIGNMENT,1)
        gluBuild2DMipmaps(GL_TEXTURE_2D,3,width,height,InternalFormat,GL_UNSIGNED_BYTE,data)
    else:
        if "filter" in filters: glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        else:                   glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D,0,InternalFormat,width,height,0,InternalFormat,GL_UNSIGNED_BYTE,data)
    #Misc.
    if "clamp" in filters:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    #Return
    return texture
def glLibSelectTexture(texture):
    glBindTexture(GL_TEXTURE_2D,texture)
