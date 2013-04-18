from OpenGL.GL import *
from OpenGL.GLU import *


def viewport2D(rect, near, far):
    glViewport(*rect)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    glOrtho(rect[0], rect[2], rect[1], rect[3], near, far)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def viewport3D(rect, angle, near, far):
    glViewport(*rect)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(angle, float(rect[2]) / float(rect[3]), near, far)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
