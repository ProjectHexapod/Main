from glLibLocals import *
from glLibMath import *
from glLibObjects import glLibTexFullScreenQuad,glLibGrid2D,glLibGrid2DMesh,glLibDoubleGrid3DMesh
from glLibFBO import *
from glLibTexturing import glLibTexture2D
from glLibMisc import glLibPushView,glLibPopView,glLibSceneToTexture
from glLibShader import *
from glLibView import *
class glLibHair:
    def __init__(self,pos_length_surf,grow_surf,length_scale,max_length,density):
        #Size
        self.size = list(pos_length_surf.get_size())

        #Misc.
        self.view_2d = glLibView2D((0,0,self.size[0],self.size[1]))
        self.update_pingpong = 1
        
        #Hair Parameters
        self.scale = 1.0
        self.trans = [0.0,0.0,0.0]
        self.dampening = 0.98
        self.tensor = 1.0
        self.gravity = [0.0,0.0,0.0]
        self.steps = 1
        self.density = density
        self.max_length = max_length
        self.length_scale = length_scale
        self.time_step = 1.0

        #Physics
        self.forces = [0.0,0.0,0.0]

        #Geometry
        self.particles = glLibGrid2D(self.size)
##        self.particles_mesh = glLibGrid2DMesh(self.size)
        self.particles_mesh = glLibDoubleGrid3DMesh([self.density*self.size[0],self.density*self.size[1],self.max_length])
##        self.particles_mesh = glLibDoubleGrid3DMesh([3,4,5])
        self.draw_particles = glLibGrid2D(sc_vec(self.density,self.size))
        
        #Textures
        self.position_length_textures = [glLibTexture2D(pos_length_surf,(0,0,self.size[0],self.size[1]),GL_RGBA,filtering=GLLIB_FILTER,precision=32)]
        self.grow_tex = glLibTexture2D(grow_surf,(0,0,self.size[0],self.size[1]),GL_RGB,precision=32)
        
        #FBOs
        self.update_framebuffers1 = []
        self.update_framebuffers2 = []
        self.grow_framebuffers = []
        for hair_segment in xrange(self.max_length):
            update_framebuffer1 = glLibFBO(self.size)
            update_framebuffer1.add_render_target(1,precision=32,filter=GLLIB_FILTER,type=GLLIB_RGBA)
            update_framebuffer1.add_render_target(2,precision=32,filter=GLLIB_FILTER)
            self.update_framebuffers1.append(update_framebuffer1)
            update_framebuffer2 = glLibFBO(self.size)
            update_framebuffer2.add_render_target(1,precision=32,filter=GLLIB_FILTER,type=GLLIB_RGBA)
            update_framebuffer2.add_render_target(2,precision=32,filter=GLLIB_FILTER)
            self.update_framebuffers2.append(update_framebuffer2)
            grow_framebuffer = glLibFBO(self.size)
            grow_framebuffer.add_render_target(1,precision=32,type=GLLIB_RGBA)
            self.grow_framebuffers.append(grow_framebuffer)

        #Shaders
        self.grow_shader = glLibShader()
        self.grow_shader.use_prebuilt(GLLIB_HAIR_GROW)
        self.update_shader = glLibShader()
        self.update_shader.use_prebuilt(GLLIB_HAIR_UPDATE)
        self.draw_shader = glLibShader()
        self.draw_shader.use_prebuilt(GLLIB_HAIR_DRAW)

        #Grow Hair
        self.glLibInternal_grow()

        #Initialize Position
        self.glLibInternal_initialize_position()
    def __del__(self):
        try:
            self.particles.__del__()
            self.particles_mesh.__del__()
        except:pass

    def set_scale(self,value):
        self.scale = value
    def set_trans(self,trans):
        self.trans = list(self.trans)
    def set_dampening(self,value):
        self.dampening = value
    def set_tensor(self,value):
        self.tensor = value
##    def set_angle_tensor(self,value):
##        self.angle_tensor = value
##    def set_max_jitter_length(self,value):
##        self.max_jitter_length = value
    def set_gravity(self,gravity):
        self.gravity = list(gravity)
##    def set_kernel_size(self,size):
##        self.kernel_size = size
    def set_steps(self,steps):
        self.steps = steps
    def set_density(self,value):
        self.density = value
    def set_steps(self,steps):
        self.steps = steps
    def set_time_step(self,value):
        self.time_step = value
    
    def add_force(self,force):
        self.forces = vec_add(self.forces,force)
    def reset(self):
        self.glLibInternal_grow()
        self.glLibInternal_initialize_position()
    def update(self):
        self.glLibInternal_push()
        self.glLibInternal_use_update_shader()
        for step in xrange(self.steps):
            self.update_shader.pass_bool("end",False)
            for hair_segment in xrange(1,self.max_length+1,1):
                if self.update_pingpong == 1:
                    if self.get_new:
                        if hair_segment == 1:
                            self.update_shader.pass_texture(self.position_length_textures[0],1)
                        else:
                            self.update_shader.pass_texture(self.update_framebuffers2[hair_segment-2].get_texture(1),1)
                        self.update_shader.pass_texture(self.update_framebuffers2[hair_segment-1].get_texture(1),2)
                        if hair_segment < self.max_length:
                            self.update_shader.pass_texture(self.update_framebuffers2[hair_segment].get_texture(1),3)
                        self.update_shader.pass_texture(self.update_framebuffers2[hair_segment-1].get_texture(2),4)
                    else:
                        self.update_shader.pass_texture(self.position_length_textures[hair_segment-1],1)
                        self.update_shader.pass_texture(self.position_length_textures[hair_segment+0],2)
                        if hair_segment < self.max_length:
                            self.update_shader.pass_texture(self.position_length_textures[hair_segment+1],3)
                        self.update_shader.pass_texture(glLibTexture2D(None,(0,0,self.size[0],self.size[1]),GL_RGB,precision=32),4)
                    self.update_framebuffers1[hair_segment-1].enable([1,2])
                else:
                    if hair_segment == 1:
                        self.update_shader.pass_texture(self.position_length_textures[0],1)
                    else:
                        self.update_shader.pass_texture(self.update_framebuffers1[hair_segment-2].get_texture(1),1)
                    self.update_shader.pass_texture(self.update_framebuffers1[hair_segment-1].get_texture(1),2)
                    if hair_segment < self.max_length:
                        self.update_shader.pass_texture(self.update_framebuffers1[hair_segment].get_texture(1),3)
                    self.update_shader.pass_texture(self.update_framebuffers1[hair_segment-1].get_texture(2),4)
                    
                    self.update_framebuffers2[hair_segment-1].enable([1,2])
                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                glLoadIdentity()
                self.view_2d.set_view()
                self.particles.draw()
                if self.update_pingpong == 1: self.update_framebuffers1[hair_segment-1].disable()
                else:                         self.update_framebuffers2[hair_segment-1].disable()
                if hair_segment == self.max_length-1:
                    self.update_shader.pass_bool("end",True)
            self.update_pingpong = 3 - self.update_pingpong
        glLibUseShader(None)
        self.glLibInternal_pop()
        self.forces = [0.0,0.0,0.0]
    def glLibInternal_push(self):
        glLibPushView()
        glDisable(GL_BLEND)
    def glLibInternal_pop(self):
        glEnable(GL_BLEND)
        glLibPopView()
    def glLibInternal_grow(self):
        self.glLibInternal_push()
        starting_from__pos_length_tex = self.position_length_textures[0]
        for growth_stage in xrange(self.max_length):
            self.grow_framebuffers[growth_stage].enable([1])
            self.glLibInternal_use_grow_shader()
            self.grow_shader.pass_texture(starting_from__pos_length_tex,1)
            self.grow_shader.pass_texture(self.grow_tex,2)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            self.view_2d.set_view()
            self.particles.draw()
            glLibUseShader(None)
            self.grow_framebuffers[growth_stage].disable()
            
            starting_from__pos_length_tex = self.grow_framebuffers[growth_stage].get_texture(1)
            self.position_length_textures.append(starting_from__pos_length_tex)
        self.glLibInternal_pop()
    def glLibInternal_initialize_position(self):
        self.get_new = False
        temp_dampening = self.dampening
        temp_gravity = list(self.gravity)
        self.dampening = 0.0
        self.gravity = [0,0,0]
        self.update()
        self.dampening = temp_dampening
        self.gravity = list(temp_gravity)
        self.get_new = True
    def glLibInternal_use_grow_shader(self):
        glLibUseShader(self.grow_shader)
        self.grow_shader.pass_vec2("size",self.size)
        self.grow_shader.pass_float("length_scalar",self.length_scale)
    def glLibInternal_use_update_shader(self):
        glLibUseShader(self.update_shader)
        self.update_shader.pass_vec2("size",self.size)
        self.update_shader.pass_float("tensor",self.tensor*0.01)
        self.update_shader.pass_float("dampening",self.dampening)
        self.update_shader.pass_vec3("gravity",sc_vec(0.0001,vec_add(self.gravity,self.forces)))
        self.update_shader.pass_float("target_length",self.length_scale)
        self.update_shader.pass_float("time_step",self.time_step)
    def glLibInternal_use_draw_shader(self,camerapos,hair_size):
        glLibUseShader(self.draw_shader)
        self.draw_shader.pass_vec2("size",self.size)
        self.draw_shader.pass_float("scale",self.scale*2.0)
        self.draw_shader.pass_vec3("trans",self.trans)
        self.draw_shader.pass_int("hair_length",self.max_length)
        self.draw_shader.pass_vec3("camerapos",camerapos)
        self.draw_shader.pass_float("hair_size",hair_size)
        for hair_segment in xrange(self.max_length):
            if hair_segment == 0:
                self.draw_shader.pass_texture(self.position_length_textures[0],1)
            else:
                #flipped from as in .update() above, b/c .update() switches self.update_pingpong
                if self.update_pingpong == 1:
                    self.draw_shader.pass_texture(self.update_framebuffers2[hair_segment-1].get_texture(1),hair_segment+1)
                else:
                    self.draw_shader.pass_texture(self.update_framebuffers1[hair_segment-1].get_texture(1),hair_segment+1)
        
    #FOR TESTING ONLY
    def draw_texture(self,xpos,ypos,texture):
        glDisable(GL_LIGHTING)
        glDisable(GL_BLEND)
        rect = list(self.view_2d.rect)
        self.view_2d.rect = [xpos,ypos,100,100]
        self.view_2d.set_view()
        self.view_2d.rect = list(rect)
        glLibSelectTexture(texture)
        glLibTexFullScreenQuad()
        glEnable(GL_BLEND)
        glEnable(GL_LIGHTING)
    def draw_points(self,camerapos,hair_size,size):
        glPointSize(size)
        glPolygonMode(GL_FRONT_AND_BACK,GL_POINT)
        self.glLibInternal_use_draw_shader(camerapos,hair_size)
        self.particles_mesh.draw()
        glLibUseShader(None)
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glPointSize(1)
##        glPointSize(size)
##        self.glLibInternal_use_draw_shader()
##        for hair_segment in xrange(self.max_length+1):
##            #flipped from as in .update() above, b/c .update() switches self.update_pingpong
##            if hair_segment == 0:
##                self.draw_shader.pass_texture(self.position_length_textures[0],1)
##            else:
##                if self.update_pingpong == 1:
##                    self.draw_shader.pass_texture(self.update_framebuffers1[hair_segment-1].get_texture(1),1)
##                if self.update_pingpong == 2:
##                    self.draw_shader.pass_texture(self.update_framebuffers2[hair_segment-1].get_texture(1),1)
####            self.particles.draw()
##            self.draw_particles.draw()
##        glLibUseShader(None)
##        glPointSize(1)
    def draw_lines(self,camerapos,hair_size,size):
        glLineWidth(size)
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        self.glLibInternal_use_draw_shader(camerapos,hair_size)
        self.particles_mesh.draw()
        glLibUseShader(None)
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glLineWidth(1)
    def draw(self,camerapos,hair_size):
        self.glLibInternal_use_draw_shader(camerapos,hair_size)
        self.particles_mesh.draw(self.draw_shader,"quad_side")
        glLibUseShader(None)
