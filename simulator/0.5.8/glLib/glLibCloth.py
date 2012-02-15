from glLibLocals import *
from glLibMath import *
from glLibObjects import glLibTexFullScreenQuad,glLibGrid2D,glLibGrid2DMesh
from glLibFBO import *
from glLibTexturing import glLibTexture2D
from glLibMisc import glLibPushView,glLibPopView
from glLibShader import *
from glLibView import *
class glLibCloth:
    def __init__(self,size,pos_data,rip_texture=None,stretched=1.0):
        #TODO: Make kernel size work!
        #Angle limiting forces
        
        #Size
        if type(size) in [type([]),type(())]:
            self.size = list(size)
        else:
            self.size = [size,size]

        #Misc.
        self.view_2d = glLibView2D((0,0,self.size[0],self.size[1]))

        #Physics
        self.forces = [0.0,0.0,0.0]
        
        #Cloth Parameters
        self.scale = 1.0
        self.trans = [0.0,0.0,0.0]
        self.dampening = 0.98
        self.tensor = 1.0
        self.angle_tensor = 0.0#1.0
        self.max_jitter_length = 1.0
        self.gravity = [0.0,0.0,0.0]
        self.kernel_size = 1
        self.steps = 1
        self.normal_flip = False
        self.loop = [False,False]
        self.time_step = 1.0

        #Collision Objects
        self.num_obstacles = 0
        self.collidable = {}
        self.is_garment = False

        #Geometry
        self.particles = glLibGrid2D(self.size)
        self.particles_mesh = glLibGrid2DMesh(self.size)
        
        #Textures
        self.pos_restrained_tex = glLibTexture2D(pos_data,(0,0,self.size[0],self.size[1]),GL_RGBA,precision=32)
##        self.
        self.original_pos_restrained_tex = self.pos_restrained_tex
        self.velocity_tex = glLibTexture2D(None,(0,0,self.size[0],self.size[1]),GL_RGB,precision=32)
        self.vec_tex = None
        self.normal_tex = None
        self.dist_edges_tex = None
        self.dist_corners_tex = None
        self.diffuse_texture = None
        self.obstacles_tex = None
        self.obstacles_aux_param_tex = None
        self.texture_repeat = [1.0,1.0]
        
        #FBOs
        self.update_framebuffer = glLibFBO(self.size)
        self.update_framebuffer.add_render_target(1,precision=32,type=GLLIB_RGBA)
        self.update_framebuffer.add_render_target(2,precision=32)
        self.update_framebuffer.add_render_target(3,precision=8)
        self.collision_framebuffer = glLibFBO(self.size)
        self.collision_framebuffer.add_render_target(1,precision=32,type=GLLIB_RGBA)
        self.collision_framebuffer.add_render_target(2,precision=32)
        self.collision_framebuffer.add_render_target(3,precision=8)
        self.normal_framebuffer = glLibFBO(self.size)
        self.normal_framebuffer.add_render_target(1)
        self.dist_angle_framebuffer = glLibFBO(self.size)
        self.dist_angle_framebuffer.add_render_target(1,precision=32,type=GLLIB_RGBA)
        self.dist_angle_framebuffer.add_render_target(2,precision=32,type=GLLIB_RGBA)
        self.set_loop(*self.loop)

        #Shaders
##        print "Compiling Update Shader"
        self.update_shader = glLibShader()
        self.update_shader.use_prebuilt(GLLIB_CLOTH_UPDATE)
##        print "Compiling Collision Shader"
        self.collision_shader = glLibShader()
        self.collision_shader.use_prebuilt(GLLIB_CLOTH_COLLIDE)
##        print "Compiling Normal Shader"
        self.normal_shader = glLibShader()
        self.normal_shader.use_prebuilt(GLLIB_CLOTH_NORMAL)
##        print "Compiling Draw Shader"
        self.draw_shader = glLibShader()
        self.draw_shader.use_prebuilt(GLLIB_CLOTH_DRAW)
##        print "Compiling Distance Shader"
        self.dist_shader = glLibShader()
        self.dist_shader.use_prebuilt(GLLIB_CLOTH_DISTANCE)
##        self.update_shader.save_vertex()

        #Get Target Distances
        self.glLibInternal_push()
        self.dist_angle_framebuffer.enable([1,2])
        self.glLibInternal_use_dist_shader()
        self.dist_shader.pass_float("stretched",stretched)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.view_2d.set_view()
        self.particles.draw()
        glLibUseShader(None)
        self.dist_angle_framebuffer.disable()
        self.glLibInternal_pop()
        self.dist_edges_tex = self.dist_angle_framebuffer.get_texture(1)
        self.dist_corners_tex = self.dist_angle_framebuffer.get_texture(2)
        
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
    def set_angle_tensor(self,value):
        self.angle_tensor = value
    def set_max_jitter(self,value):
        self.max_jitter_length = value
    def set_gravity(self,gravity):
        self.gravity = list(gravity)
    def set_kernel_size(self,size):
        self.kernel_size = size
    def set_steps(self,steps):
        self.steps = steps
    def set_normal_flip(self,value):
        self.normal_flip = value
    def set_loop(self,x_value,y_value):
        self.loop = [x_value,y_value]
        self.particles_mesh.__del__()
        self.particles_mesh = glLibGrid2DMesh(self.size,self.loop)
    def set_time_step(self,value):
        self.time_step = value
    def set_texture(self,texture):
        self.diffuse_texture = texture
    def set_texture_repeat(self,repeat):
        if type(repeat) in [type([]),type(())]:
            self.texture_repeat = list(repeat)
        else:
            self.texture_repeat = [repeat,repeat]
    def add_force(self,force):
        self.forces = vec_add(self.forces,force)
            
    def reset(self):
        self.pos_restrained_tex = self.original_pos_restrained_tex
        self.glLibInternal_initialize_position()
        self.velocity_tex = glLibTexture2D(None,(0,0,self.size[0],self.size[1]),GL_RGB,precision=32)
        self.glLibInternal_initialize_position()

    def add_obstacle(self,id,pos,type,param):
        self.collidable[id] = [pos[0],pos[1],pos[2],[type,param]]
        self.num_obstacles += 1
        self.glLibInternal_calculate_obstacles()
    def move_obstacle(self,id,newpos):
        type,param = self.collidable[id][-1]
        self.collidable[id] = [newpos[0],newpos[1],newpos[2],[type,param]]
        self.glLibInternal_calculate_obstacles()
    def remove_obstacle(self,id):
        del self.collidable[id]
        self.num_obstacles -= 1
        self.glLibInternal_calculate_obstacles()
    def glLibInternal_calculate_obstacles(self):
        data1 = np.array(np.zeros((1,self.num_obstacles,4)),"f")
        data2 = np.array(np.zeros((1,self.num_obstacles,4)),"f")
        x = 0
        for obstacle in self.collidable.values():
            position = list(obstacle[:3])
            position_type = map(lambda num:0.5*((num+1.0)/2.0),position)
            type,param = obstacle[-1]
            if type == GLLIB_OBSTACLE_SPHERE:
                position_type[2] += 0.5
                color1 = [position_type[0],position_type[1],position_type[2],param/2.0]
                color2 = [0.0,0.0,0.0,0.0]
            elif type == GLLIB_OBSTACLE_BOX:
                position_type[1] += 0.5
                color1 = [position_type[0],position_type[1],position_type[2],param[0]]
                color2 = [param[1],param[2],(param[3]%360.0)/360.0,(param[4]%360.0)/360.0]
            data1[0][x] = np.array(color1,"f")
            data2[0][x] = np.array(color2,"f")
            x += 1
        self.obstacles_tex = glLibTexture2D(data1,(0,0,self.num_obstacles,1),GL_RGBA,precision=32)
        self.obstacles_aux_param_tex = glLibTexture2D(data2,(0,0,self.num_obstacles,1),GL_RGBA,precision=32)
    def update(self):
        self.glLibInternal_push()
        for step in xrange(self.steps):
            self.update_framebuffer.enable(GLLIB_ALL)
            self.glLibInternal_use_update_shader()
            self.glLibInternal_set_2D_view()
            self.particles.draw()
            self.update_framebuffer.disable()
            
            self.pos_restrained_tex = self.update_framebuffer.get_texture(1)
            self.velocity_tex = self.update_framebuffer.get_texture(2)
            self.vec_tex = self.update_framebuffer.get_texture(3)
            
            self.collision_framebuffer.enable(GLLIB_ALL)
            self.glLibInternal_use_collision_shader()
            self.glLibInternal_set_2D_view()
            self.particles.draw()
            self.collision_framebuffer.disable()

            self.pos_restrained_tex = self.collision_framebuffer.get_texture(1)
            self.velocity_tex = self.collision_framebuffer.get_texture(2)
        self.normal_framebuffer.enable([1])
        self.glLibInternal_use_normal_shader()
        self.glLibInternal_set_2D_view()
        self.particles.draw()
        self.normal_framebuffer.disable()
        self.normal_tex = self.normal_framebuffer.get_texture(1)
        glLibUseShader(None)
        self.glLibInternal_pop()
        self.forces = [0.0,0.0,0.0]
    def glLibInternal_push(self):
        glLibPushView()
        glDisable(GL_BLEND)
    def glLibInternal_pop(self):
        glEnable(GL_BLEND)
        glLibPopView()
    def glLibInternal_set_2D_view(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.view_2d.set_view()
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
    def glLibInternal_use_dist_shader(self):
        glLibUseShader(self.dist_shader)
        self.dist_shader.pass_vec2("size",self.size)
        self.dist_shader.pass_bool("repeat_x",self.loop[0])
        self.dist_shader.pass_bool("repeat_y",self.loop[1])
        self.dist_shader.pass_texture(self.pos_restrained_tex,1)
    def glLibInternal_use_update_shader(self):
        glLibUseShader(self.update_shader)
        self.update_shader.pass_texture(self.pos_restrained_tex,1)
        self.update_shader.pass_texture(self.velocity_tex,2)
        self.update_shader.pass_texture(self.dist_edges_tex,3)
        self.update_shader.pass_texture(self.dist_corners_tex,4)
        self.update_shader.pass_vec2("size",self.size)
        self.update_shader.pass_float("tensor",self.tensor*0.01)
        self.update_shader.pass_float("angle_tensor",self.angle_tensor*0.001)
        self.update_shader.pass_float("dampening",self.dampening)
        self.update_shader.pass_float("max_jitter",self.max_jitter_length*0.002)
        self.update_shader.pass_float("time_step",self.time_step)
        self.update_shader.pass_vec3("gravity",sc_vec(0.0001,vec_add(self.gravity,self.forces)))
        self.update_shader.pass_bool("repeat_x",self.loop[0])
        self.update_shader.pass_bool("repeat_y",self.loop[1])
        self.update_shader.pass_int("kernel_size",self.kernel_size)
    def glLibInternal_use_collision_shader(self):
        glLibUseShader(self.collision_shader)
        self.collision_shader.pass_texture(self.pos_restrained_tex,1)
        self.collision_shader.pass_texture(self.velocity_tex,2)
        self.collision_shader.pass_texture(self.vec_tex,3)
        self.collision_shader.pass_vec2("size",self.size)
        self.collision_shader.pass_int("num_obstacles",self.num_obstacles)
        if self.is_garment:
            self.collision_shader.pass_texture(self.obstacles_tex,4)
            self.collision_shader.pass_bool("is_garment",True)
            texture_size = self.obstacles_tex.width
            voxel_side = rndint(pow(texture_size**2.0,(1.0/3.0)))
            self.collision_shader.pass_vec3("voxel_size",[texture_size,voxel_side,texture_size/voxel_side])
        elif self.num_obstacles > 0:
            self.collision_shader.pass_texture(self.obstacles_tex,4)
            self.collision_shader.pass_texture(self.obstacles_aux_param_tex,5)
    def glLibInternal_use_normal_shader(self):
        glLibUseShader(self.normal_shader)
        self.normal_shader.pass_vec2("size",self.size)
        self.normal_shader.pass_bool("repeat_x",self.loop[0])
        self.normal_shader.pass_bool("repeat_y",self.loop[1])
        self.normal_shader.pass_bool("normal_flip",self.normal_flip)
    def glLibInternal_use_draw_shader(self):
        glLibUseShader(self.draw_shader)
        self.draw_shader.pass_vec2("size",self.size)
        self.draw_shader.pass_float("scale",self.scale*2.0)
        self.draw_shader.pass_vec3("trans",self.trans)
        self.draw_shader.pass_vec2("uv_repeat",self.texture_repeat)
        self.draw_shader.pass_texture(self.pos_restrained_tex,1)
        self.draw_shader.pass_int("numlights",1)
        if self.diffuse_texture != None:
            self.draw_shader.pass_bool("has_texture",True)
            self.draw_shader.pass_texture(self.diffuse_texture,2)
        else:
            self.draw_shader.pass_bool("has_texture",False)
        self.draw_shader.pass_texture(self.normal_tex,3)
        
    def draw_points(self,size,numlights=1):
        glPointSize(size)
        self.glLibInternal_use_draw_shader()
        self.draw_shader.pass_int("numlights",numlights)
        self.particles.draw()
        glLibUseShader(None)
        glPointSize(1)
    def draw_lines(self,size,numlights=1):
        glLineWidth(size)
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        self.glLibInternal_use_draw_shader()
        self.draw_shader.pass_int("numlights",numlights)
        self.particles_mesh.draw()
        glLibUseShader(None)
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        glLineWidth(1)
    def draw(self,numlights=1):
        self.glLibInternal_use_draw_shader()
        self.draw_shader.pass_int("numlights",numlights)
        self.particles_mesh.draw()
        glLibUseShader(None)

##        glDisable(GL_BLEND)
##        glDisable(GL_LIGHTING)
##        rect = list(self.view_2d.rect)
##        
##        self.view_2d.rect = [0,0,128,128]
##        self.view_2d.set_view()
##        self.view_2d.rect = list(rect)
##        glLibSelectTexture(self.collision_framebuffer.get_texture(3))
##        glLibTexFullScreenQuad()
##
####        self.view_2d.rect = [100,0,100,100]
####        self.view_2d.set_view()
####        self.view_2d.rect = list(rect)
####        glLibSelectTexture(self.pos_restrained_tex)
####        glLibTexFullScreenQuad()
##        
##        glEnable(GL_LIGHTING)
##        glEnable(GL_BLEND)
