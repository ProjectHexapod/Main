from glLibLocals import *
from glLibTexturing import *
from glLibPrebuiltShaders import glLibInternal_shader
import shaderfunctions

##from ctypes import *

##def print_log(shader):
##    print "trying 1"
##    length = c_int()
##    glGetShaderiv(shader,GL_INFO_LOG_LENGTH,byref(length))
##    if length.value > 0:
##        log = create_string_buffer(length.value)
##        glGetShaderInfoLog(shader, length, byref(length), log)
##        print >> sys.stderr, log.value
def glLibInternal_CompileShader(source,shaderType):
    shader = glCreateShaderObjectARB(shaderType)
    #Crucial for ATI compatibility to have []
    glShaderSourceARB(shader,[source])
    glCompileShaderARB(shader)
    return shader
def glLibUseShader(shader):
    if shader != None:
        try:
            if not shader.compiled:
                raise glLibError("Shader not compiled!")
            else:
                shader = shader.program
        except:
            raise glLibError("Shader not a glLibShader object!")
    else:
        shader = 0
    glUseProgramObjectARB(shader)
class glLibShader:
    def __init__(self):
        self.errors = "Shader not yet compiled!"
        self.compiled = False
        self.renderequation = ""
        self.uservars = ""
        self.prevertex = ""
        self.verttrans = ""
        self.postvertex = ""
        self.uvtrans = ""
        self.extfuncvert = ""
        self.extfuncfrag = ""
        self.max1Dtextures = 0
        self.max2Dtextures = 8
        self.max3Dtextures = 0
        self.maxcubetextures = 0
        self.automaxtextures = False
        self.maxrendertargets = 1
        self.automaxrendertargets = False
        self.locations = {}
    def use_prebuilt(self,type,args=None):
        self.renderequation,\
        self.uservars,\
        self.prevertex,self.verttrans,self.postvertex,\
        self.uvtrans,\
        self.extfuncvert,self.extfuncfrag,\
        self.max1Dtextures,self.max2Dtextures,self.max3Dtextures,self.maxcubetextures,\
        self.maxrendertargets = glLibInternal_shader(type,args)
        self.compile()
        if self.errors != "": print self.errors
    def render_equation(self,render_equation):
        self.renderequation = render_equation
    def user_variables(self,user_vars):
        self.uservars = user_vars
    def pre_vertex(self,pre_vertex):
        self.prevertex = pre_vertex
    def vertex_transform(self,vertex_transform):
        self.verttrans = vertex_transform
    def post_vertex(self,post_vertex):
        self.postvertex = post_vertex
    def uv_transform(self,uv_transform):
        self.uvtrans = uv_transform
    def vertex_extension_functions(self,extension_functions):
        self.extfuncvert = extension_functions
    def fragment_extension_functions(self,extension_functions):
        self.extfuncfrag = extension_functions
    def render_targets(self,render_targets):
        self.maxrendertargets = render_targets
    def auto_render_targets(self,value):
        self.automaxrendertargets = value
    def max_textures_1D(self,number):
        self.max1Dtextures = number
    def max_textures_2D(self,number):
        self.max2Dtextures = number
    def max_textures_3D(self,number):
        self.max3Dtextures = number
    def max_textures_cube(self,number):
        self.maxcubetextures = number
    def auto_max_textures(self,value):
        self.automaxtextures = value
    def decompile(self):
        if not self.compiled: raise glLibError("Shader already not compiled!")
        glDeleteProgram(self.program)
        del self.source, self.program
        self.errors = "Shader not yet compiled!"
        self.compiled = False
        self.locations = {}
    def compile(self):
        if self.automaxtextures:
            for target in [["tex1D_",1],["tex2D_",2],["tex3D_",3],["texCube_",6]]:
                texnum = target[1]
                num = 0
                while True:
                    num += 1
                    str_target = target[0]+str(num)
                    if str_target in self.renderequation: continue
                    if str_target in self.prevertex: continue
                    if str_target in self.verttrans: continue
                    if str_target in self.postvertex: continue
                    if str_target in self.uvtrans: continue
                    if str_target in self.extfuncvert: continue
                    if str_target in self.extfuncfrag: continue
                    
                    if   texnum == 1: self.max1Dtextures   = num - 1
                    elif texnum == 2: self.max2Dtextures   = num - 1
                    elif texnum == 3: self.max3Dtextures   = num - 1
                    elif texnum == 6: self.maxcubetextures = num - 1
                    
                    break
        if self.automaxrendertargets:
            num = 1
            while True:
                num += 1
                target = "color"+str(num)
                if target in self.renderequation: continue
                self.maxrendertargets = num - 1
                break
        self.source = glLibInternal_ShaderSource(self.renderequation,\
                                                 self.uservars,\
                                                 self.prevertex,self.verttrans,self.postvertex,\
                                                 self.uvtrans,\
                                                 self.extfuncvert,self.extfuncfrag,\
                                                 self.max2Dtextures,self.max3Dtextures,self.maxcubetextures,self.maxrendertargets)
        
        self.program = glCreateProgramObjectARB()
        VertexShader = glLibInternal_CompileShader(self.source.vert,GL_VERTEX_SHADER_ARB)
##        try:print glGetShaderInfoLog(VertexShader)
##        except:print_log(VertexShader)
        FragmentShader = glLibInternal_CompileShader(self.source.frag,GL_FRAGMENT_SHADER_ARB)
##        try:print glGetShaderInfoLog(FragmentShader)
##        except:print_log(FragmentShader)
        glAttachObjectARB(self.program,VertexShader)
        glAttachObjectARB(self.program,FragmentShader)
        glDeleteObjectARB(VertexShader)
        glDeleteObjectARB(FragmentShader)
        glValidateProgramARB(self.program)
        glLinkProgramARB(self.program)
##        print glGetProgramInfoLog(self.program)
        
        self.errors = glGetInfoLogARB(self.program)
        self.compiled = True
        return self.errors
    def print_vertex(self):
        shader_lines = self.source.vert.split("\n")
        for string in self.glLibInternal_get_shader_strings(shader_lines,self.prevertex+self.verttrans+self.postvertex+self.uservars,True):
            print string
    def print_fragment(self):
        shader_lines = self.source.frag.split("\n")
        for string in self.glLibInternal_get_shader_strings(shader_lines,self.uvtrans+self.renderequation+self.uservars,True):
            print string
    def save_vertex(self,numbers=False,path=None):
        shader_lines = self.source.vert.split("\n")
        file_string = ""
        for string in self.glLibInternal_get_shader_strings(shader_lines,"",numbers):
            file_string += string
            file_string += "\n"
        if path == None: file = open("vertex.vert","w")
        else:            file = open(path,"w")
        file.write(file_string)
        file.close()
    def save_fragment(self,numbers=False,path=None):
        shader_lines = self.source.frag.split("\n")
        file_string = ""
        for string in self.glLibInternal_get_shader_strings(shader_lines,"",numbers):
            file_string += string
            file_string += "\n"
        if path == None: file = open("fragment.frag","w")
        else:            file = open(path,"w")
        file.write(file_string)
        file.close()
    def glLibInternal_get_shader_strings(self,shader_lines,parts,numbering):
        first_indent = len(shader_lines[1])-len(shader_lines[1].strip())
        last_rel_indent = 0
        line_num = 1
        max_num_length = len(str(len(shader_lines)))
        strings = []
        for shader_line_indent in shader_lines:
            shader_line = shader_line_indent.strip()
            indent = len(shader_line_indent)-len(shader_line)
            rel_indent = indent-first_indent
            if rel_indent != last_rel_indent:
                if shader_line in parts:
                    rel_indent = last_rel_indent
            line_num_str = str(line_num)
            string = ""
            if numbering:
                string += line_num_str + ": " + ((max_num_length-len(line_num_str))*" ")
            string += rel_indent*" "
            string += shader_line
            strings.append(string)
            line_num += 1
            last_rel_indent = rel_indent
        return strings
    def glLibInternal_get_location(self,name):
        try: return self.locations[name]
        except: self.locations[name] = glGetUniformLocation(self.program,name)
        return self.locations[name]
    def pass_texture(self,texture,number):
        glLibActiveTexture(number-1)
        active_texture = glGetIntegerv(GL_ACTIVE_TEXTURE) - GL_TEXTURE0
        if texture.type == GLLIB_TEXTURE_1D:
            glBindTexture(GL_TEXTURE_1D,texture.texture)
            glUniform1i(self.glLibInternal_get_location("tex1D_"+str(number)),active_texture)
        elif texture.type == GLLIB_TEXTURE_2D:
            glBindTexture(GL_TEXTURE_2D,texture.texture)
            glUniform1i(self.glLibInternal_get_location("tex2D_"+str(number)),active_texture)
        elif texture.type == GLLIB_TEXTURE_3D:
            glBindTexture(GL_TEXTURE_3D,texture.texture)
            glUniform1i(self.glLibInternal_get_location("tex3D_"+str(number)),active_texture)
        elif texture.type == GLLIB_TEXTURE_CUBE:
            glBindTexture(GL_TEXTURE_CUBE_MAP,texture.texture)
            glUniform1i(self.glLibInternal_get_location("texCube_"+str(number)),active_texture)
        glLibActiveTexture(0)
    def pass_float(self,name,float): glUniform1f(self.glLibInternal_get_location(name),float)
    def pass_int  (self,name,int  ): glUniform1i(self.glLibInternal_get_location(name),int)
    def pass_bool (self,name,bool ): glUniform1i(self.glLibInternal_get_location(name),bool)
    def pass_vec2 (self,name,vec2 ): glUniform2f(self.glLibInternal_get_location(name),vec2[0],vec2[1])
    def pass_vec3 (self,name,vec3 ): glUniform3f(self.glLibInternal_get_location(name),vec3[0],vec3[1],vec3[2])
    def pass_vec4 (self,name,vec4 ): glUniform4f(self.glLibInternal_get_location(name),vec4[0],vec4[1],vec4[2],vec4[3])
    def pass_mat2 (self,name,mat2 ): glUniformMatrix2fv(self.glLibInternal_get_location(name),1,False,mat2)
    def pass_mat3 (self,name,mat3 ): glUniformMatrix3fv(self.glLibInternal_get_location(name),1,False,mat3)
    def pass_mat4 (self,name,mat4 ): glUniformMatrix4fv(self.glLibInternal_get_location(name),1,False,mat4)
class glLibInternal_ShaderSource:
    def __init__(self,renderequation,uservars,pre_vertex,verttrans,post_vertex,uvtrans,extfuncvert,extfuncfrag,max2Dtextures,max3Dtextures,maxcubetextures,maxrendertargets):
        #VERTEX SHADER SOURCE GENERATION
        self.vert = ""
        self.vert += """varying vec3 vVertex;
        varying vec3 t;
        varying vec3 b;
        varying vec3 n;
        varying vec3 realnorm;
        varying vec4 ProjCoord;
        varying vec4 vertex;
        uniform sampler2D   """+"".join("tex2D_"  +str(x)+"," for x in xrange(1,max2Dtextures  +1,1))[:-1]+""";
        uniform sampler3D   """+"".join("tex3D_"  +str(x)+"," for x in xrange(1,max3Dtextures  +1,1))[:-1]+""";
        uniform samplerCube """+"".join("texCube_"+str(x)+"," for x in xrange(1,maxcubetextures+1,1))[:-1]+""";
        attribute vec4 vert_tangent;
        uniform mat4 matrix;
        """
        self.vert += uservars
        self.vert += """
        float sum(vec2 vec) { return vec.x+vec.y; }
        float sum(vec3 vec) { return vec.x+vec.y+vec.z; }
        float sum(vec4 vec) { return vec.x+vec.y+vec.z+vec.w; }
        float round(float num) {
            float fnum = floor(num);
            return (num-fnum)>0.5 ? fnum+1.0:fnum;
        }
        vec2 round(vec2 num) { return vec2(round(num.x),round(num.y)); }
        vec3 round(vec3 num) { return vec3(round(num.x),round(num.y),round(num.z)); }
        vec4 round(vec4 num) { return vec4(round(num.x),round(num.y),round(num.z),round(num.w)); }"""
        self.vert += shaderfunctions.glLibInternal_get_rotation_funcs(pre_vertex+verttrans+post_vertex)
        self.vert += extfuncvert
        self.vert += """
        void main() {
            gl_TexCoord[0] = gl_MultiTexCoord0;
            vertex = gl_Vertex;
            realnorm = gl_Normal;"""
        self.vert += pre_vertex
        self.vert += """
            n = gl_NormalMatrix*realnorm;
            t = normalize(gl_NormalMatrix*vert_tangent.xyz);
            b = cross(n,t)*vert_tangent.w;"""
        self.vert += verttrans
        self.vert += """
            vVertex = vec4(gl_ModelViewMatrix*vertex).xyz;
            ProjCoord = matrix*vertex;
            gl_Position = gl_ModelViewProjectionMatrix*vertex;"""
        self.vert += post_vertex
        self.vert += """
        }"""
        #FRAGMENT SHADER SOURCE GENERATION
        self.frag = ""
        self.frag += """varying vec3 vVertex,t,b,n,realnorm;
        varying vec4 ProjCoord,vertex;
        uniform sampler2D   """+"".join("tex2D_"  +str(x)+"," for x in xrange(1,max2Dtextures  +1,1))[:-1]+""";
        uniform sampler3D   """+"".join("tex3D_"  +str(x)+"," for x in xrange(1,max3Dtextures  +1,1))[:-1]+""";
        uniform samplerCube """+"".join("texCube_"+str(x)+"," for x in xrange(1,maxcubetextures+1,1))[:-1]+""";
        vec3 E,normal,L;
        uniform mat4 matrix2,modelmatrix,viewmatrix;"""
        self.frag += uservars
        
        self.frag += """
        float sum(vec2 vec) { return vec.x+vec.y; }
        float sum(vec3 vec) { return vec.x+vec.y+vec.z; }
        float sum(vec4 vec) { return vec.x+vec.y+vec.z+vec.w; }
        float round(float num) {
            float fnum = floor(num);
            return (num-fnum)>0.5 ? fnum+1.0:fnum;
        }
        vec2 round(vec2 num) { return vec2(round(num.x),round(num.y)); }
        vec3 round(vec3 num) { return vec3(round(num.x),round(num.y),round(num.z)); }
        vec4 round(vec4 num) { return vec4(round(num.x),round(num.y),round(num.z),round(num.w)); }
        float depth_from_depthbuffer(float depth,float near,float far) { return ((-(far*near)/((depth*(far-near))-far))-near)/(far-near); }
        vec3 normal_from_normalmap(sampler2D normalmap,vec2 uv) {
            vec3 sample = texture2D(normalmap,uv).rgb;
            vec3 tangent_norm = vec3((sample.rg-0.5)*2.0,sample.b);
            vec3 world_norm = normalize(mat3(t,b,n)*tangent_norm);
            return world_norm;
        }"""

        self.frag += shaderfunctions.glLibInternal_get_parallaxmap_funcs       (uvtrans       )
        self.frag += shaderfunctions.glLibInternal_get_subsurface_absorb_funcs (renderequation)
        self.frag += shaderfunctions.glLibInternal_get_shadow_funcs            (renderequation)
        self.frag += shaderfunctions.glLibInternal_get_cubemap_funcs           (renderequation)
        self.frag += shaderfunctions.glLibInternal_get_light_funcs             (renderequation)
        self.frag += shaderfunctions.glLibInternal_get_caustic_func            (renderequation)
        self.frag += shaderfunctions.glLibInternal_get_rotation_funcs          (renderequation)
        
        self.frag += extfuncfrag
        
        self.frag += """
        void main() {
            vec4 color = vec4(0.0,0.0,0.0,1.0);"""
        if "clamp_color" in renderequation:
            self.frag += "bool clamp_color = true;"
        if maxrendertargets > 1:
            for i in xrange(maxrendertargets):
                if "color"+str(i+2) in renderequation:
                    self.frag += "vec4 color"+str(i+2)+" = vec4(0.0,0.0,0.0,1.0);"
                    if "clamp_color"+str(i+2) in renderequation:
                        self.frag += "bool clamp_color"+str(i+2)+" = true;"
        self.frag += """
            E = normalize(-vVertex);
            vec2 uv = gl_TexCoord[0].st;
            """
        self.frag += uvtrans
        if "_color" in renderequation:
            self.frag += """
            vec4 ambient_color =  gl_FrontMaterial.ambient;
            vec4 diffuse_color =  gl_FrontMaterial.diffuse;
            vec4 specular_color = gl_FrontMaterial.specular;"""
        self.frag += """
            normal = normalize(n);"""
        for num in xrange(1,9,1):
            renderequation = renderequation.replace("light"+str(num),"gl_LightSource["+str(num-1)+"]")
        self.frag += "\n"
        self.frag += renderequation
        if "clamp_color" in renderequation:
            self.frag += "if (clamp_color) { color = clamp(color,0.0,1.0); }"
        else:
            self.frag += "color = clamp(color,0.0,1.0);"
        self.frag += """
            gl_FragData[0] = color;"""
        if maxrendertargets > 1:
            for i in xrange(maxrendertargets):
                if "color"+str(i+2) in renderequation:
                    if "clamp_color"+str(i+2) in renderequation:
                        self.frag += "if (clamp_color"+str(i+2)+") { color"+str(i+2)+" = clamp(color"+str(i+2)+",0.0,1.0); }"
                    else:
                        self.frag += "color"+str(i+2)+" = clamp(color"+str(i+2)+",0.0,1.0);"
                    self.frag += "gl_FragData["+str(i+1)+"] = color"+str(i+2)+";"
        self.frag += """
        }"""

        







