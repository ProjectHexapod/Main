##from OpenGL.GL import glColor3f, glColor4f, glEnable, glDisable, GL_COLOR_MATERIAL
from OpenGL.GL import *
from OpenGL.GLU import gluUnProject
import pygame
def glLibNormalize(value):
    if value:
        glEnable(GL_NORMALIZE)
    else:
        glDisable(GL_NORMALIZE)
def glLibColor(color):
    if   len(color) == 3: glColor3f(color[0]/255.0,color[1]/255.0,color[2]/255.0)
    elif len(color) == 4: glColor4f(color[0]/255.0,color[1]/255.0,color[2]/255.0,color[3]/255.0)
def glLibColorMaterial(value):
    if value:glEnable(GL_COLOR_MATERIAL)
    else:glDisable(GL_COLOR_MATERIAL)
def glLibSaveScreenshot(path):
    x,y,width,height = glGetIntegerv(GL_VIEWPORT)
    glPixelStorei(GL_PACK_ALIGNMENT, 4)
    glPixelStorei(GL_PACK_ROW_LENGTH, 0)
    glPixelStorei(GL_PACK_SKIP_ROWS, 0)
    glPixelStorei(GL_PACK_SKIP_PIXELS, 0)
    data = glReadPixels(0,0,width,height,GL_RGB,GL_UNSIGNED_BYTE)
    data = data.tostring()
    surface = pygame.image.fromstring(data,(width,height),'RGB',1)
    pygame.image.save(surface,path)
def glLibUnProject(mouse_pos):
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    winX = mouse_pos[0]
    winY = float(viewport[3])-mouse_pos[1]
    winZ = glReadPixels(winX,winY,1,1,GL_DEPTH_COMPONENT,GL_FLOAT)
    if type(winZ) != float:
        # On windows glReadPixels returns a weird array
        winZ = winZ[0][0]
    cursor_pos = gluUnProject(winX,winY,winZ,modelview,projection,viewport)
    return cursor_pos
