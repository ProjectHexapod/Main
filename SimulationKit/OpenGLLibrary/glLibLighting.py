from OpenGL.GL import *
from OpenGL.GLU import *


def glLibLighting(value):
    if value:
        glEnable(GL_LIGHTING)
    else:
        glDisable(GL_LIGHTING)


class glLibLight:
    def __init__(self, pos, camera, color=(255, 255, 255), diffusecolor=(255, 255, 255)):
        self.pos = pos
        self.can_be_represented = True
        self.color = color
        self.diffuse_color = diffusecolor
        if not glGetBooleanv(GL_LIGHT0):
            self.light = GL_LIGHT0
        elif not glGetBooleanv(GL_LIGHT1):
            self.light = GL_LIGHT1
        elif not glGetBooleanv(GL_LIGHT2):
            self.light = GL_LIGHT2
        elif not glGetBooleanv(GL_LIGHT3):
            self.light = GL_LIGHT3
        elif not glGetBooleanv(GL_LIGHT4):
            self.light = GL_LIGHT4
        elif not glGetBooleanv(GL_LIGHT5):
            self.light = GL_LIGHT5
        elif not glGetBooleanv(GL_LIGHT6):
            self.light = GL_LIGHT6
        elif not glGetBooleanv(GL_LIGHT7):
            self.light = GL_LIGHT7
        else:
            self.can_be_represented = False
        camera.set_camera()
        self.change_color(self.color)
        self.change_diffuse_color(self.diffuse_color)
        self.change_pos(self.pos)

    def disable(self):
        if self.can_be_represented:
            glDisable(self.light)

    def enable(self):
        if self.can_be_represented:
            glEnable(self.light)

    def get_color(self):
        return self.color

    def get_pos(self):
        return self.pos

    def change_diffuse_color(self, newcolor):
        if self.can_be_represented:
            self.diffuse_color = newcolor
            glLightfv(self.light, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
            glLightfv(self.light, GL_DIFFUSE, [self.diffuse_color[0] / 255.0, self.diffuse_color[1] / 255.0, self.diffuse_color[2] / 255.0, 1.0])

    def change_color(self, newcolor):
        if self.can_be_represented:
            self.color = newcolor
            glLightfv(self.light, GL_SPECULAR, [self.color[0] / 255.0, self.color[1] / 255.0, self.color[2] / 255.0, 1.0])

    def draw(self):
        self.change_pos(self.get_pos())

    def change_pos(self, newpos):
        self.pos = newpos
        if self.can_be_represented:
            glLightfv(self.light, GL_POSITION, [self.pos[0], self.pos[1], self.pos[2], 1.0])

    def draw_as_point(self, size=3):
        lighting = glGetBooleanv(GL_LIGHTING)
        texturing = glGetBooleanv(GL_TEXTURE_2D)
        r, g, b, a = glGetFloatv(GL_CURRENT_COLOR)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glPointSize(size)
        glColor3f(self.color[0] / 255.0, self.color[1] / 255.0, self.color[2] / 255.0)
        glBegin(GL_POINTS)
        glVertex3f(*self.pos)
        glEnd()
        glColor4f(r, g, b, a)
        if lighting:
            glEnable(GL_LIGHTING)
        if texturing:
            glEnable(GL_TEXTURE_2D)
