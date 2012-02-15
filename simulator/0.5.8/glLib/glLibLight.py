from glLibLocals import *
from glLibShader import glLibUseShader
class glLibLight:
    def __init__(self,number):
        self.number = number-1
        self.light = GL_LIGHT0+self.number
        self.pos = [0.0,0.0,0.0]
        self.atten = [1.0,0.0,0.0]
        self.ambient_color = list(glGetLightfv(self.light,GL_AMBIENT))[:3]
        self.diffuse_color = list(glGetLightfv(self.light,GL_DIFFUSE))[:3]
        self.specular_color = list(glGetLightfv(self.light,GL_SPECULAR))[:3]
        self.type = 0.0
        self.spot = [[0.,0.,-1.],0.,180.]
    def __del__(self):
        try:
            self.default()
            self.disable()
        except:pass
    def set_ambient(self,ambient_color):
        self.ambient_color = list(ambient_color)
        glLightfv(self.light,GL_AMBIENT,[self.ambient_color[0],self.ambient_color[1],self.ambient_color[2],1.0])
    def set_diffuse(self,diffuse_color):
        self.diffuse_color = list(diffuse_color)
        glLightfv(self.light,GL_DIFFUSE,[self.diffuse_color[0],self.diffuse_color[1],self.diffuse_color[2],1.0])
    def set_specular(self,specular_color):
        self.specular_color = list(specular_color)
        glLightfv(self.light,GL_SPECULAR,[self.specular_color[0],self.specular_color[1],self.specular_color[2],1.0])
    def set_pos(self,pos):
        self.pos = list(pos)
        self.set()
    def set_atten(self,const,lin,quad):
        self.const_atten = const
        self.lin_atten = lin
        self.quad_atten = quad
        glLightfv(self.light,GL_CONSTANT_ATTENUATION,[const])
        glLightfv(self.light,GL_LINEAR_ATTENUATION,[lin])
        glLightfv(self.light,GL_QUADRATIC_ATTENUATION,[quad])
    def set_spot_dir(self,direction):
        self.spot[0] = direction
        glLightfv(self.light,GL_SPOT_DIRECTION,self.spot[0])
    def set_spot_ex(self,exponent):
        self.spot[1] = exponent
        glLightf(self.light,GL_SPOT_EXPONENT,self.spot[1])
    def set_spot_angle(self,angle):
        if angle == None: angle = 360.0
        self.spot[2] = angle/2.0
        glLightf(self.light,GL_SPOT_CUTOFF,self.spot[2])
    def enable(self):
        glEnable(self.light)
    def disable(self):
        glDisable(self.light)
    def get_number(self):
        return self.number+1
    def get_ambient_color(self):
        return self.ambient_color
    def get_diffuse_color(self):
        return self.diffuse_color
    def get_specular_color(self):
        return self.specular_color
    def get_pos(self):
        return self.pos
    def get_atten(self):
        return [self.const_atten,self.lin_atten,self.quad_atten]
##    def push_attrib(self):
##        self.past_diffuses.append(self.diffuse_color)
##        self.past_colors.append(self.color)
##        self.past_pos.append(self.pos)
##    def pop_attrib(self):
##        self.diffuse_color = self.past_diffuses[-1]
##        self.color = self.past_colors[-1]
##        self.pos = self.past_pos[-1]
##        self.past_diffuses = self.past_diffuses[:-1]
##        self.past_colors = self.past_colors[:-1]
##        self.past_pos = self.past_pos[:-1]
##        self.change_diffuse_color(self.diffuse_color)
##        self.change_color(self.color)
##        self.change_pos(self.pos)
    def set(self):
        glLightfv(self.light,GL_POSITION,[self.pos[0],self.pos[1],self.pos[2],self.type])
    def set_type(self,type):
        if type == GLLIB_POINT_LIGHT: self.type = 1.0
        elif type == GLLIB_DIRECTIONAL_LIGHT: self.type = 0.0
    def zero(self):
        self.set_pos([0,0,0])
        self.set_ambient([0,0,0])
        self.set_diffuse([0,0,0])
        self.set_specular([0,0,0])
        self.set_atten(1,0,0)
    def default(self):
        self.set_pos([0,0,1])
        self.set_type(GLLIB_DIRECTIONAL_LIGHT)
        self.set_ambient([0,0,0])
        if self.light == GL_LIGHT0:
            self.set_diffuse([1,1,1])
            self.set_specular([1,1,1])
        else:
            self.set_diffuse([0,0,0])
            self.set_specular([0,0,0])
        self.set_spot_dir([0,0,-1])
        self.set_spot_ex(0)
        self.set_spot_angle(360.0)
        self.set_atten(1,0,0)
    def draw_as_point(self,size=3):
        glLibUseShader(None)
        lighting = glGetBooleanv(GL_LIGHTING)
        texturing = glGetBooleanv(GL_TEXTURE_2D)
        r,g,b,a = glGetFloatv(GL_CURRENT_COLOR)
        ptsize = glGetFloatv(GL_POINT_SIZE)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glPointSize(size)
        glColor3f(*self.diffuse_color)
        glBegin(GL_POINTS)
        glVertex3f(*self.pos)
        glEnd()
        glPointSize(ptsize)
        glColor4f(r,g,b,a)
        if lighting: glEnable(GL_LIGHTING)
        if texturing: glEnable(GL_TEXTURE_2D)
        return self
    def draw_as_sphere(self,size=0.05,detail=10):
        glLibUseShader(None)
        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)
        glPushMatrix()
        glTranslatef(*self.pos)
        Sphere = gluNewQuadric()
        gluSphere(Sphere,size,detail,detail)
        glPopMatrix()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
