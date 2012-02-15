from glLibLocals import *
class glLibInternal_texture:
    def __init__(self,rectangulardata,format,precision,filtering,mipmapping,colorkey,data):
        if self.type != GLLIB_TEXTURE_3D:
            if rectangulardata != GLLIB_ALL:
                self.x = rectangulardata[0]
                self.y = rectangulardata[1]
                self.width = rectangulardata[2]
                self.height = rectangulardata[3]
        else:
            self.width = rectangulardata[0]
            self.height = rectangulardata[1]
            self.depth = rectangulardata[2]
        try:self.rect = list(rectangulardata)
        except:self.rect = rectangulardata
        self.datatype = GL_UNSIGNED_BYTE
        self.format = format
        self.internalformat = format
        if precision == 8:
            if self.format == GLLIB_RGB:
                self.internalformat = GL_RGB
            elif self.format == GLLIB_RGBA:
                self.internalformat = GL_RGBA
            elif self.format == GLLIB_DEPTH:
                self.internalformat = GL_DEPTH_COMPONENT
        elif precision == 16:
            if self.format == GLLIB_RGB:
                self.internalformat = GL_RGB16F_ARB
            elif self.format == GLLIB_RGBA:
                self.internalformat = GL_RGBA16F_ARB
            elif self.format == GLLIB_DEPTH:
                self.internalformat = GL_DEPTH_COMPONENT16
        elif precision == 24:
            if self.format == GLLIB_RGB:
                self.internalformat = GL_RGB16F_ARB
            elif self.format == GLLIB_RGBA:
                self.internalformat = GL_RGBA16F_ARB
            elif self.format == GLLIB_DEPTH:
                self.internalformat = GL_DEPTH_COMPONENT24
        elif precision == 32:
            if self.format == GLLIB_RGB:
                self.internalformat = GL_RGB32F_ARB
            elif self.format == GLLIB_RGBA:
                self.internalformat = GL_RGBA32F_ARB
            elif self.format == GLLIB_DEPTH:
                self.internalformat = GL_DEPTH_COMPONENT32
        self.is_filtering = filtering
        self.is_mipmapping = mipmapping
        self.precision = precision
        self.data = data
        self.colorkey = colorkey
        self.edge_status = "Unknown"
    def filtering(self,filter_value,mipmap_value):
        if self.is_filtering != filter_value or self.is_mipmapping != mipmap_value:
            self.is_filtering = filter_value
            self.is_mipmapping = mipmap_value
            self.glLibInternal_make(recreate=True,remipmap=True)
    def glLibInternal_get_data(self,data):
        datatype = str(type(data))
        if datatype not in ["<type 'pygame.Surface'>","<type 'str'>"]:
            self.datatype = GL_FLOAT
            return data #"<type 'numpy.ndarray'>" ?
        if type(data) == type(""):
            path = ""
            split_path = data.split("\\")
            for part in split_path: path += part; path += "/"
            split_path = data.split("/")
            path = os.path.join(*split_path)
            if self.format == GLLIB_RGB:
                data = pygame.image.load(path).convert()
            else:
                data = pygame.image.load(path).convert_alpha()
        if self.rect == GLLIB_ALL:
            self.x=0;self.y=0;self.width,self.height=data.get_size()
            self.rect=[0,0,self.width,self.height]
        if self.type != GLLIB_TEXTURE_3D:
            data = data.subsurface((self.x,self.y,self.width,self.height))
        if self.colorkey != None:
            data.set_colorkey(self.colorkey)
        self.surface = data.copy()
        if data != None:
            if self.type == GLLIB_TEXTURE_3D:
                #http://www.gamedev.net/community/forums/topic.asp?topic_id=538657 for loading certain files.
                pixelcount = data.get_width()*data.get_height()
                self.width = self.height = self.depth = int(round(pixelcount**(1.0/3.0)))
                data = Numeric.empty((self.width*self.height*self.depth*3),"uint8")
                blocks = int(round((pixelcount**0.5)/self.width))
                texture3darray = pygame.surfarray.array3d(self.surface)
                for jj in range(blocks):
                    for ii in range(blocks):
                        chunk = texture3darray[(ii*self.width):((ii+1)*self.width), (jj*self.height):((jj+1)*self.height), :]
                        chunk = Numeric.ravel(chunk).astype("uint8")
                        index0 = (jj*blocks*self.width*self.height*3)+(ii*self.width*self.height*3)
                        index1 = index0+(self.width*self.height*3)
                        data[index0:index1] = chunk
                glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            else:
                if self.format == GLLIB_RGB: data = pygame.image.tostring(data,"RGB",True)
                else:                        data = pygame.image.tostring(data,"RGBA",True)
        return data
    def glLibInternal_make(self,recreate=False,remipmap=False):
        self.glLibInternal_create(self.type,self.type,self.data,re_creating=recreate,changed_mipmaps=remipmap)
    def glLibInternal_create(self,type,paramtype,data,re_creating=False,changed_mipmaps=False):
        if type in [GLLIB_TEXTURE_2D,GLLIB_TEXTURE_3D]:
            if not re_creating:
                self.texture = glGenTextures(1)
            glBindTexture(type,self.texture)
        else:
            if not self.making:
                if not re_creating:
                    self.texture = glGenTextures(1)
                glBindTexture(paramtype,self.texture)
        if self.is_mipmapping in [GLLIB_MIPMAP,GLLIB_MIPMAP_BLEND]:
            if self.is_mipmapping == GLLIB_MIPMAP_BLEND:
                if self.is_filtering == GLLIB_FILTER: mipmap_param = GL_LINEAR_MIPMAP_LINEAR
                else:                              mipmap_param = GL_NEAREST_MIPMAP_LINEAR
            elif self.is_mipmapping == GLLIB_MIPMAP:
                if self.is_filtering == GLLIB_FILTER: mipmap_param = GL_LINEAR_MIPMAP_NEAREST
                else:                              mipmap_param = GL_NEAREST_MIPMAP_NEAREST
            glTexParameterf(paramtype,GL_TEXTURE_MIN_FILTER,mipmap_param)
            glPixelStoref(GL_UNPACK_ALIGNMENT,1)
            if type != GLLIB_TEXTURE_3D:
                gluBuild2DMipmaps(type,self.format,self.width,self.height,self.format,self.datatype,data)
            else:
                gluBuild3DMipmaps(type,self.format,self.width,self.height,self.depth,self.format,self.datatype,data)
        else:
            if not re_creating or changed_mipmaps:
                if type != GLLIB_TEXTURE_3D:
                    if self.format == GLLIB_RGB: glPixelStorei(GL_UNPACK_ALIGNMENT,1)
                    glTexImage2D(type,0,self.internalformat,self.width,self.height,0,self.format,self.datatype,data)
                else:
                    glTexImage3D(type,0,self.internalformat,self.width,self.height,self.depth,0,self.format,self.datatype,data)
            if self.is_filtering == GLLIB_FILTER: glTexParameterf(paramtype,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            else:                              glTexParameterf(paramtype,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        if self.is_filtering == GLLIB_FILTER: glTexParameterf(paramtype,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        else:                              glTexParameterf(paramtype,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        glTexParameteri(paramtype,GL_TEXTURE_COMPARE_MODE,GL_NONE)
        glPixelStorei(GL_UNPACK_ALIGNMENT,4) #reset
    def anisotropy(self,value):
        if self.type in [GLLIB_TEXTURE_2D,GLLIB_TEXTURE_3D]:
            glBindTexture(self.type,self.texture)
        if value == GLLIB_MAX: value = glGetFloat(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT)
        elif value == None:    value = 1.0
        glTexParameterf(self.type,GL_TEXTURE_MAX_ANISOTROPY_EXT,value)
    def edge(self,value):
        if self.type in [GLLIB_TEXTURE_2D,GLLIB_TEXTURE_3D]:
            glBindTexture(self.type,self.texture)
        if type(value) in [type([]),type(())]:
            self.edge_status = []
            if   value[0] == GLLIB_CLAMP:         self.edge_status.append("GLLIB_CLAMP"        ); glTexParameteri(self.type,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
            elif value[0] == GLLIB_REPEAT:        self.edge_status.append("GLLIB_REPEAT"       ); glTexParameteri(self.type,GL_TEXTURE_WRAP_S,GL_REPEAT)
            elif value[0] == GLLIB_MIRROR_REPEAT: self.edge_status.append("GLLIB_MIRROR_REPEAT"); glTexParameteri(self.type,GL_TEXTURE_WRAP_S,GL_MIRRORED_REPEAT)
            if   value[1] == GLLIB_CLAMP:         self.edge_status.append("GLLIB_CLAMP"        ); glTexParameteri(self.type,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE)
            elif value[1] == GLLIB_REPEAT:        self.edge_status.append("GLLIB_REPEAT"       ); glTexParameteri(self.type,GL_TEXTURE_WRAP_T,GL_REPEAT)
            elif value[1] == GLLIB_MIRROR_REPEAT: self.edge_status.append("GLLIB_MIRROR_REPEAT"); glTexParameteri(self.type,GL_TEXTURE_WRAP_T,GL_MIRRORED_REPEAT)
            if self.type == GLLIB_TEXTURE_3D:
                if   value[2] == GLLIB_CLAMP:         self.edge_status.append("GLLIB_CLAMP"        ); glTexParameteri(self.type,GL_TEXTURE_WRAP_R,GL_CLAMP_TO_EDGE)
                elif value[2] == GLLIB_REPEAT:        self.edge_status.append("GLLIB_REPEAT"       ); glTexParameteri(self.type,GL_TEXTURE_WRAP_R,GL_REPEAT)
                elif value[2] == GLLIB_MIRROR_REPEAT: self.edge_status.append("GLLIB_MIRROR_REPEAT"); glTexParameteri(self.type,GL_TEXTURE_WRAP_R,GL_MIRRORED_REPEAT)
        else:
            if value == GLLIB_CLAMP:
                self.edge_status = "GLLIB_CLAMP"
                glTexParameteri(self.type,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
                glTexParameteri(self.type,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE)
                if self.type == GLLIB_TEXTURE_3D: glTexParameteri(self.type,GL_TEXTURE_WRAP_R,GL_CLAMP_TO_EDGE)
            elif value == GLLIB_REPEAT:
                self.edge_status = "GLLIB_REPEAT"
                glTexParameteri(self.type,GL_TEXTURE_WRAP_S,GL_REPEAT)
                glTexParameteri(self.type,GL_TEXTURE_WRAP_T,GL_REPEAT)
                if self.type == GLLIB_TEXTURE_3D: glTexParameteri(self.type,GL_TEXTURE_WRAP_R,GL_REPEAT)
            elif value == GLLIB_MIRROR_REPEAT:
                self.edge_status = "GLLIB_MIRROR_REPEAT"
                glTexParameteri(self.type,GL_TEXTURE_WRAP_S,GL_MIRRORED_REPEAT)
                glTexParameteri(self.type,GL_TEXTURE_WRAP_T,GL_MIRRORED_REPEAT)
                if self.type == GLLIB_TEXTURE_3D: glTexParameteri(self.type,GL_TEXTURE_WRAP_R,GL_MIRRORED_REPEAT)
class glLibTexture2D(glLibInternal_texture):
    def __init__(self,data,rect,format,filtering=False,mipmapping=False,colorkey=None,precision=8):
        self.type = GLLIB_TEXTURE_2D
        glLibInternal_texture.__init__(self,rect,format,precision,filtering,mipmapping,colorkey,data)
        self.data = self.glLibInternal_get_data(self.data)
        self.glLibInternal_make()
class glLibTexture3D(glLibInternal_texture):
    def __init__(self,data,rect,format,filtering=False,mipmapping=False,colorkey=None,precision=8):
        self.type = GLLIB_TEXTURE_3D
        glLibInternal_texture.__init__(self,rect,format,precision,filtering,mipmapping,colorkey,data)
        self.data = self.glLibInternal_get_data(self.data)
        self.glLibInternal_make()
class glLibTextureCube(glLibInternal_texture):
    def __init__(self,data,rect,format,filtering=False,mipmapping=False,colorkey=None):
        self.type = GLLIB_TEXTURE_CUBE
        glLibInternal_texture.__init__(self,rect,format,False,filtering,mipmapping,colorkey,data)
        self.data = [self.glLibInternal_get_data(element) for element in self.data]
        self.glLibInternal_make()
    def glLibInternal_make(self,recreate=False,remipmap=False):
##        glEnable(GL_TEXTURE_CUBE_MAP)
        self.making = False
        for face in xrange(6):
            self.glLibInternal_create(GLLIB_TEXTURE_CUBE_FACES[face],GLLIB_TEXTURE_CUBE,self.data[face],\
                                      re_creating=recreate,changed_mipmaps=remipmap)
            self.making = True
        self.making = False
##        glDisable(GL_TEXTURE_CUBE_MAP)
def glLibActiveTexture(texture_number):
    glActiveTexture(GL_TEXTURE0+texture_number);
def glLibSelectTexture(texture):
    glBindTexture(texture.type,texture.texture)
