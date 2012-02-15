from glLibLocals import *
class glLibView2D():
    def __init__(self,rect):
        self.rect = list(rect)
    def set_view(self):
        glViewport(*self.rect)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(self.rect[0],self.rect[0]+self.rect[2],self.rect[1],self.rect[1]+self.rect[3])
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
class glLibViewISO():
    def __init__(self,rect,near=0.1,far=1000.0):
        self.rect = list(rect)
        self.near = near
        self.far = far
        self.zoom = 1.0
    def set_near(self,value):
        self.near = value
    def set_far(self,value):
        self.far = value
    def set_zoom(self,value):
        self.zoom = value
    def set_view(self):
        glViewport(*self.rect)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0/self.zoom,1.0/self.zoom,-1.0/self.zoom,1.0/self.zoom,\
                self.near,self.far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
class glLibView3D():
    def __init__(self,rect,angle,near=0.1,far=1000.0):
        self.rect = list(rect)
        self.angle = angle
        self.near = near
        self.far = far
    def set_angle(self,angle):
        self.angle = angle
    def set_near(self,value):
        self.near = value
    def set_far(self,value):
        self.far = value
    def set_view(self):
        glViewport(*self.rect)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity() 
        gluPerspective(self.angle,float(self.rect[2])/float(self.rect[3]),self.near,self.far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
