from glLibLocals import *
from glLibShader import glLibShader, glLibUseShader
from glLibFBO import glLibFBO
from glLibTexturing import glLibTexture2D, glLibSelectTexture
from glLibObjects import glLibTexFullScreenQuad, glLibGrid2D
from glLibMisc import glLibPushView, glLibPopView
from glLibView import glLibView2D
class glLibParticleSystem:
    def __init__(self,n,precision=8):
        #self.n differs from n by a maximum of sqrt(n)+1
        self.size = [int(round(n**0.5))]*2
        self.n = self.size[0] * self.size[1]

        #Shader to update particles
        self.update_shader = glLibShader()
        self.update_shader.use_prebuilt(GLLIB_PARTICLE_UPDATE)
##        print self.update_shader.errors

        #Shader to draw particles
        self.draw_shader = glLibShader()
        self.draw_shader.use_prebuilt(GLLIB_PARTICLE_DRAW)
##        print self.draw_shader.errors

        #Particles as VBO
        self.particles = glLibGrid2D(self.size[0])

        #Parameters
        self.origin  = [0.0,0.0,0.0]
        self.initialspeed = [0.0,0.0,0.0]
        self.forces = [0.0,0.0,0.0]
        self.scale   = [1,1,1]
        self.density = 1.0
        self.step = 1.0/(self.n-1)
        self.density_constant = (1.0/64.0)*(4.0**log(self.size[0],2.0)) * self.step
        self.trans = [0.0,0.0,0.0]
        self.fade = 1.0
        self.jitter = [0.0,0.0,0.0]
        self.psize = 100.0
        #   Edge handling
        self.negx = 1.0
        self.negy = 1.0
        self.negz = 1.0
        self.posx = 1.0
        self.posy = 1.0
        self.posz = 1.0

        #Data Textures
        self.pos_time_texture = None
        self.velocity_texture = None

        self.view_2D = glLibView2D((0,0,self.size[0],self.size[1]))
        
        self.point_texture = glLibTexture2D(os.path.join("glLib","fireparticle.png"),(0,0,8,8),GLLIB_RGBA)
        self.point_texture.edge(GLLIB_CLAMP)

        self.precision = precision

        self.framebuffer1 = glLibFBO(self.size)
        self.framebuffer1.add_render_target(1,type=GLLIB_RGBA,precision=self.precision)
        self.framebuffer1.add_render_target(2,type=GLLIB_RGBA,precision=self.precision)

        self.framebuffer2 = glLibFBO(self.size)
        self.framebuffer2.add_render_target(1,type=GLLIB_RGBA,precision=self.precision)
        self.framebuffer2.add_render_target(2,type=GLLIB_RGBA,precision=self.precision)

        self.pingpong = 1

        xvalues = np.zeros(self.n)+0.5
        yvalues = np.zeros(self.n)+0.5
        zvalues = np.zeros(self.n)+0.5
        tvalues = np.arange(0.0, 1.0+(1.0/self.n), 1.0/(self.n-1.0)).astype(float)
        zeros = np.zeros(self.n)
        texarray = np.concatenate([xvalues,yvalues,zvalues,tvalues]).reshape(4,-1).T
        texarray = texarray.reshape((self.size[0],self.size[1],4))
        self.pos_time_texture = glLibTexture2D(texarray,(0,0,self.size[0],self.size[1]),GLLIB_RGBA)

        vecs = np.random.standard_normal(size=(self.size[0],self.size[1],3))
        magnitudes = np.sqrt((vecs*vecs).sum(axis=-1))
        uvecs = vecs / magnitudes[...,np.newaxis]
        randlen = np.random.random((self.size[0],self.size[1]))
        randvecs = uvecs*randlen[...,np.newaxis]
        rgb = ((randvecs+1.0)/2.0)*255.0
        surface = pygame.surfarray.make_surface(rgb)
        self.rand_tex = glLibTexture2D(surface,(0,0,self.size[0],self.size[1]),GLLIB_RGB)
        
        self.get_new = False
        self.update()
        self.get_new = True
    def set_origin(self,origin):
        self.origin = list(origin)
    def set_initial_speed(self,speed):
        self.initialspeed = list(speed)
    def set_forces(self,forces):
        self.forces = list(forces)
    def set_scale(self,scale):
        self.scale = list(scale)
    def set_trans(self,trans):
        self.trans = list(trans)
    def set_fade(self,fade):
        self.fade = fade
    def set_jitter(self,jitter):
        self.jitter = jitter
    def set_particle_size(self,size):
        self.psize = size
    def set_density(self,density):
        self.density = density
    def set_edge(self,negx,posx,negy,posy,negz,posz):
        self.negx = negx
        self.negy = negy
        self.negz = negz
        self.posx = posx
        self.posy = posy
        self.posz = posz
    def update(self):
        glLibPushView()
        glDisable(GL_BLEND)
        
        if self.pingpong == 1:
            if self.get_new:
                self.pos_time_texture = self.framebuffer2.get_texture(1)
            self.velocity_texture = self.framebuffer2.get_texture(2)
            self.framebuffer1.enable([1,2])
        else:
            if self.get_new:
                self.pos_time_texture = self.framebuffer1.get_texture(1)
            self.velocity_texture = self.framebuffer1.get_texture(2)
            self.framebuffer2.enable([1,2])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.view_2D.set_view()
        glLibUseShader(self.update_shader)
        self.update_shader.pass_texture(self.pos_time_texture,1)
        self.update_shader.pass_texture(self.velocity_texture,2)
        self.update_shader.pass_texture(self.rand_tex,3)
        self.update_shader.pass_vec3("initialpos",self.origin)
        self.update_shader.pass_vec3("initialspeed",self.initialspeed)
        self.update_shader.pass_vec3("forces",self.forces)
        self.update_shader.pass_vec3("scale",self.scale)
        self.update_shader.pass_vec3("trans",self.trans)
        self.update_shader.pass_vec3("jitter",self.jitter)
        self.update_shader.pass_float("size",float(self.size[0]))
        self.update_shader.pass_float("step",self.density_constant*self.density)
        self.update_shader.pass_vec2("xedge",[self.negx,self.posx])
        self.update_shader.pass_vec2("yedge",[self.negy,self.posy])
        self.update_shader.pass_vec2("zedge",[self.negz,self.posz])
        
        self.particles.draw()
        glLibUseShader(None)

        if self.pingpong == 1:
            self.framebuffer1.disable()
        else:
            self.framebuffer2.disable()

        self.pingpong = 3 - self.pingpong

        glEnable(GL_BLEND)
        glLibPopView()
    def draw(self):
        glLibUseShader(self.draw_shader)
        
        self.draw_shader.pass_texture(self.pos_time_texture,1)
        self.draw_shader.pass_texture(self.point_texture,2)
        self.draw_shader.pass_vec3("scale",map(lambda x:2.0*x,self.scale))
        self.draw_shader.pass_float("size",float(self.size[0]))
        self.draw_shader.pass_float("fade",self.fade)
        self.draw_shader.pass_float("point_size",self.psize)
        
        glDisable(GL_LIGHTING)

        glEnable(GL_POINT_SPRITE)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        
        self.particles.draw()
        
        glDisable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_POINT_SPRITE)
        
        glLibUseShader(None)

##        glDisable(GL_BLEND)
##        self.view_2D.set_view()
##        glLibSelectTexture(self.pos_time_texture)
##        glLibTexFullScreenQuad()
##        glEnable(GL_BLEND)

        glEnable(GL_LIGHTING)
    def __del__(self):
        try:
            self.particles.__del__()
        except:pass




        
