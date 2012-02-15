from glLibLocals import *
from glLibLoadOBJ import *
from glLibLoadRAW import *
from glLibShader import *
from glLibMath import rndint
from glLibMaterials import glLibGetMaterialParam
def glLibTexFullScreenQuad(param=GLLIB_AUTO):
    if param == GLLIB_AUTO:
        param = glGetFloatv(GL_VIEWPORT)
    glBegin(GL_QUADS)
    glTexCoord2f(0,0);glVertex2f(param[0],         param[1]         )
    glTexCoord2f(1,0);glVertex2f(param[0]+param[2],param[1]         )
    glTexCoord2f(1,1);glVertex2f(param[0]+param[2],param[1]+param[3])
    glTexCoord2f(0,1);glVertex2f(param[0],         param[1]+param[3])
    glEnd()
class glLibQuad:
    def __init__(self,rect,texture=False):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        if texture != False: glLibSelectTexture(texture)
        glBegin(GL_QUADS)
        if texture != False: glTexCoord2f(0,0)
        glVertex3f(rect[0],        rect[1],        0)
        if texture != False: glTexCoord2f(1,0)
        glVertex3f(rect[0]+rect[2],rect[1],        0)
        if texture != False: glTexCoord2f(1,1)
        glVertex3f(rect[0]+rect[2],rect[1]+rect[3],0)
        if texture != False: glTexCoord2f(0,1)
        glVertex3f(rect[0],        rect[1]+rect[3],0)
        glEnd()
        glEndList()
    def draw(self):
        glCallList(self.list)
def glLibInternal_quadric(normals,normalflip,flipnormalflip,texture):
    quad = gluNewQuadric()
    if   normals == GLLIB_NONE:           gluQuadricNormals(quad,GLU_NONE)
    elif normals == GLLIB_FACE_NORMALS:   gluQuadricNormals(quad,GLU_FLAT)
    elif normals == GLLIB_VERTEX_NORMALS: gluQuadricNormals(quad,GLU_SMOOTH)
    if flipnormalflip:
        inside = GLU_OUTSIDE
        outside = GLU_INSIDE
    else:
        inside = GLU_INSIDE
        outside = GLU_OUTSIDE
    if normalflip: gluQuadricOrientation(quad,inside )
    else:          gluQuadricOrientation(quad,outside)
    if texture != False:
        glLibSelectTexture(texture)
        gluQuadricTexture(quad,GLU_TRUE)
    else:
        gluQuadricTexture(quad,GLU_FALSE)
    return quad
class glLibSphere:
    def __init__(self,size,detail,normals=GLLIB_VERTEX_NORMALS,normalflip=False,texture=False):
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        Sphere = glLibInternal_quadric(normals,normalflip,False,texture)
        try: gluSphere(Sphere,size,detail,detail)
        except: gluSphere(Sphere,size,detail[0],detail[1])
        glEndList()
    def draw(self):
        glCallList(self.list)
class glLibCylinder:
    def __init__(self,length,r1,r2,detail,cap1=False,cap2=False,normals=GLLIB_VERTEX_NORMALS,normalflip=False,texture=False):
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        Cylinder = glLibInternal_quadric(normals,normalflip,False,texture)
        try:    radialdetail,stacks = detail[0],detail[1]
        except: radialdetail,stacks = detail,1
        gluCylinder(Cylinder,r1,r2,length,radialdetail,stacks)
        if cap1 != False:
            disk1 = glLibInternal_quadric(normals,normalflip,True,texture)
            radius = 0.0
            if cap1 != True: radius = float(cap1)
            gluDisk(disk1,radius,r1,radialdetail,1)
        if cap2 != False:
            disk2 = glLibInternal_quadric(normals,normalflip,False,texture)
            radius = 0.0
            if cap2 != True: radius = float(cap2)
            glTranslatef(0,0,length)
            gluDisk(disk2,radius,r2,radialdetail,1)
            glTranslatef(0,0,-length)
        glEndList()
    def draw(self):
        glCallList(self.list)
class glLibDome:
    def __init__(self,size,detail,texture=False):
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        if texture: glLibSelectTexture(texture)
        vertical_step = 90.0/detail
        horizontal_step = 360.0/detail
        y_angle = 0.0
        for azimuth_angle in xrange(detail):
            height_low = size*sin(radians(y_angle))
            height_high = size*sin(radians(y_angle+vertical_step))
            glBegin(GL_QUAD_STRIP)
            x_angle = 0.0
            for angle in xrange(detail+1):
                if texture: glTexCoord2f(x_angle/360.0,y_angle/90.0)
                glVertex3f(size*cos(radians(x_angle))*cos(radians(y_angle)),
                           height_low,
                           size*sin(radians(x_angle))*cos(radians(y_angle)))
                if texture: glTexCoord2f(x_angle/360.0,(y_angle+vertical_step)/90.0)
                glVertex3f(size*cos(radians(x_angle))*cos(radians(y_angle+vertical_step)),
                           height_high,
                           size*sin(radians(x_angle))*cos(radians(y_angle+vertical_step)))
                x_angle += horizontal_step
            glEnd()
            y_angle += vertical_step
        glEndList()
    def draw(self):
        glCallList(self.list)
class glLibPlane:
    def __init__(self,size,normal,texture=False,uv_repeat=1):
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        elevangle = degrees(atan2(hypot(normal[0],normal[2]),normal[1]))
        xzangle = degrees(atan2(normal[0],normal[2]))
        if texture:
            try:glLibSelectTexture(texture)
            except:pass
        glPushMatrix()
        glRotatef(xzangle,0,1,0)
        glRotatef(elevangle,1,0,0)
        glBegin(GL_QUADS)
        glNormal3f(0,1,0)
        if texture:glTexCoord2f(0,0)
        glVertex3f(-size,0,-size)
        if texture:glTexCoord2f(uv_repeat,0)
        glVertex3f( size,0,-size)
        if texture:glTexCoord2f(uv_repeat,uv_repeat)
        glVertex3f( size,0, size)
        if texture:glTexCoord2f(0,uv_repeat)
        glVertex3f(-size,0, size)
        glEnd()
        glPopMatrix()
        glEndList()
    def draw(self):
        glCallList(self.list)
class glLibObject:
    def __init__(self,path,filtering=False,mipmapping=False):
        if path.endswith(".obj"):
            self.type, \
                self.raw_vertices, self.raw_polygons, self.vertices, \
                self.normals, self.texturecoords, self.tbnvectors, \
                self.materials, \
                self.hasnormcoords, self.hastexcoords, self.hasmaterial = glLibInternal_LoadOBJFile(path,filtering,mipmapping)
        elif path.endswith(".raw"):
            self.type, \
                self.raw_vertices, self.raw_polygons, self.vertices, \
                self.normals, self.texturecoords, self.tbnvectors, \
                self.materials, \
                self.hasnormcoords, self.hastexcoords, self.hasmaterial = glLibInternal_LoadRAWFile(path)
        else:
            raise glLibError("Object type at "+path+" not recognized!")
        self.number_of_lists = len(self.vertices)
    def glLibInternal_set_mtl(self, sublist,indices, lst_amb,lst_dif,lst_spc,lst_shn):
        material = self.materials[sublist]
        if "Ka" in material:
            ambient = material["Ka"]
            if lst_amb != ambient: glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT,ambient); lst_amb = ambient
        if "Kd" in material:
            diffuse = material["Kd"]
            if lst_dif != diffuse: glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,diffuse); lst_dif = diffuse
        if "Ks" in material:
            specular = material["Ks"]
            if lst_spc != specular: glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR,specular); lst_spc = specular
        if "Ns" in material:
            shininess = material["Ns"]
            if lst_shn != shininess: glMaterialfv(GL_FRONT_AND_BACK,GL_SHININESS,shininess); lst_shn = shininess
        if "texture_Kd" in material:
            if len(indices) > sublist:
                index = indices[sublist]
                if index != None:
                    glEnable(GL_TEXTURE_2D)
                    glLibActiveTexture(index-1); glLibSelectTexture(material["texture_Kd"]); glLibActiveTexture(0)
        else:
            glDisable(GL_TEXTURE_2D)
        return lst_amb,lst_dif,lst_spc,lst_shn
    def set_material(self,material):
        texture = None
        try:
            try:
                ambient,diffuse,specular,shininess = material[0]
                materialnumbers = [int(material[1])]
                try: texture = material[2]
                except: pass
            except:
                ambient,diffuse,specular,shininess = material
                materialnumbers = range(0,len(self.materials),1)
        except:
            try:
                ambient,diffuse,specular,shininess = glLibGetMaterialParam(material[0])
                materialnumbers = [int(material[1])]
            except:
                ambient,diffuse,specular,shininess = glLibGetMaterialParam(material)
                materialnumbers = range(0,len(self.materials),1)
        for materialnumber in materialnumbers:
            self.materials[materialnumber] = {}
            if ambient   != -1: self.materials[materialnumber]["Ka"] = list(ambient)
            if diffuse   != -1: self.materials[materialnumber]["Kd"] = list(diffuse)
            if specular  != -1: self.materials[materialnumber]["Ks"] = list(specular)
            if shininess != -1: self.materials[materialnumber]["Ns"] = shininess
            if texture   != -1:
                if texture != None:
                    self.materials[materialnumber]["texture_Kd"] = texture
    def build_list(self,indices=[]):
        lst_amb=None;lst_dif=None;lst_spc=None;lst_shn=None
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        if self.hasmaterial: glPushAttrib(GL_ENABLE_BIT|GL_LIGHTING_BIT)
        for sublist in xrange(self.number_of_lists):
            if self.hasmaterial:
                lst_amb,lst_dif,lst_spc,lst_shn = self.glLibInternal_set_mtl(sublist,indices, lst_amb,lst_dif,lst_spc,lst_shn)
            glBegin(self.type)
            for index in xrange(len(self.vertices[sublist])):
                if self.hasnormcoords: glNormal3f(*self.normals[sublist][index])
                if self.hastexcoords: glTexCoord2f(*self.texturecoords[sublist][index])
                glVertex3f(*self.vertices[sublist][index])
            glEnd()
        if self.hasmaterial: glPopAttrib()
        glEndList()
    def build_vbo(self):
        self.vertex_vbos = []
        self.normal_vbos = []
        self.texcoord_vbos = []
        self.vertex_attrib_vbos = []
        for i in xrange(self.number_of_lists):
            attributenum = 0
            attributes = []
            try:    attributes.append(self.vertices[i])
            except: attributes.append([])
            try:    attributes.append(self.normals[i])
            except: attributes.append([])
            try:    attributes.append(self.texturecoords[i])
            except: attributes.append([])
            try:    attributes.append(self.tbnvectors[i])
            except: attributes.append([])
            for attribute in attributes:
                if not self.hasnormcoords and attributenum ==    1 : continue
                if not self.hastexcoords  and attributenum in [2,3]: continue
                singlelist = []
                for vertex in attribute:
                    singlelist.append(vertex)
                if   attributenum == 0: self.vertex_vbos.append(vbo.VBO(np.array(singlelist,"f")))
                elif attributenum == 1: self.normal_vbos.append(vbo.VBO(np.array(singlelist,"f")))
                elif attributenum == 2: self.texcoord_vbos.append(vbo.VBO(np.array(singlelist,"f")))
                elif attributenum == 3: self.vertex_attrib_vbos.append(vbo.VBO(self.tbnvectors[i]))
                attributenum += 1
    def draw_list(self):
        glCallList(self.list)
    def draw_vbo(self,shader=None,indices=[],withmaterials=True,withtexcoords=True,withnormals=True,withtangents=True):
        lst_amb=None;lst_dif=None;lst_spc=None;lst_shn=None
        location = -1
        if shader != None:
            glLibUseShader(shader)
            location = glGetAttribLocation(shader.program,"vert_tangent")
        glEnableClientState(GL_VERTEX_ARRAY)
        if self.hasnormcoords and withnormals: glEnableClientState(GL_NORMAL_ARRAY)
        if self.hastexcoords and withtexcoords:
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            if location != -1 and withtangents: glEnableVertexAttribArray(location)
        glPushAttrib(GL_ENABLE_BIT|GL_LIGHTING_BIT)
        for sublist in xrange(self.number_of_lists):
            if self.hasmaterial and withmaterials:
                lst_amb,lst_dif,lst_spc,lst_shn = self.glLibInternal_set_mtl(sublist,indices, lst_amb,lst_dif,lst_spc,lst_shn)
            self.vertex_vbos[0].bind()
            glVertexPointerf(self.vertex_vbos[0])
            if self.hasnormcoords and withnormals:
                self.normal_vbos[0].bind()
                glNormalPointerf(self.normal_vbos[0])
            if self.hastexcoords and withtexcoords:
                self.texcoord_vbos[0].bind()
                glTexCoordPointerf(self.texcoord_vbos[0])
            if location != -1 and withtangents:
                self.vertex_attrib_vbos[0].bind()
                glVertexAttribPointer(location,4,GL_FLOAT,GL_FALSE,0,None)
            glDrawArrays(self.type,0,len(self.vertices[sublist]))
        glPopAttrib()
        glBindBuffer(GL_ARRAY_BUFFER,0)
        if self.hastexcoords and withtexcoords:
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
            if location != -1 and withtangents: glDisableVertexAttribArray(location)
        if self.hasnormcoords and withnormals: glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
    def draw_arrays(self,shader=None,indices=[],withmaterials=True,withtexcoords=True,withnormals=True,withtangents=True):
        lst_amb=None;lst_dif=None;lst_spc=None;lst_shn=None
        if self.hasmaterial: glPushAttrib(GL_ENABLE_BIT|GL_LIGHTING_BIT)
        location = -1
        if shader != None:
            glLibUseShader(shader)
            location = glGetAttribLocation(shader.program,"vert_tangent")
        glEnableClientState(GL_VERTEX_ARRAY)
        if self.hasnormcoords and withnormals: glEnableClientState(GL_NORMAL_ARRAY)
        if self.hastexcoords and withtexcoords:
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            if location != -1 and withtangents: glEnableVertexAttribArray(location)
        for sublist in xrange(self.number_of_lists):
            if self.hasmaterial and withmaterials:
                lst_amb,lst_dif,lst_spc,lst_shn = self.glLibInternal_set_mtl(sublist,indices, lst_amb,lst_dif,lst_spc,lst_shn)
            if self.vertices[sublist] != []:
                glVertexPointer(3,GL_FLOAT,0,self.vertices[sublist])
                if self.hasnormcoords and withnormals: glNormalPointer(GL_FLOAT,0,self.normals[sublist])
                if self.hastexcoords and withtexcoords: glTexCoordPointer(2,GL_FLOAT,0,self.texturecoords[sublist])
                if location != -1 and withtangents: glVertexAttribPointer(location,4,GL_FLOAT,GL_FALSE,0,self.tbnvectors[sublist])
                glDrawArrays(GL_TRIANGLES,0,len(self.vertices[sublist]))
        if self.hastexcoords and withtexcoords:
            if location != -1 and withtangents: glDisableVertexAttribArray(location)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        if self.hasnormcoords and withnormals: glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        if self.hasmaterial: glPopAttrib()
    def __del__(self):
        try:
            buffers = []
            for vbolist in [self.vertex_vbos,self.normal_vbos,self.texcoord_vbos,self.vertex_attrib_vbos]:
                for vbo in vbolist:
                    vbo.delete()
        except:pass
def glLibGetNormal(t1,t2,t3,flip=False):
    v1 = [t2[0]-t1[0],t2[1]-t1[1],t2[2]-t1[2]]
    v2 = [t3[0]-t1[0],t3[1]-t1[1],t3[2]-t1[2]]
    vx = (v1[1] * v2[2]) - (v1[2] * v2[1])
    vy = (v1[2] * v2[0]) - (v1[0] * v2[2])
    vz = (v1[0] * v2[1]) - (v1[1] * v2[0])
    n = [vx, vy, vz]
    if flip:
        n = [-n[0],-n[1],-n[2]]
    return n
class glLibRectangularSolid():
    def __init__(self,size,texture=False,normalflip=False):
        self.box = glGenLists(1)
        glNewList(self.box,GL_COMPILE)
        if texture != False and type(texture)!=type([]) and texture.type == GLLIB_TEXTURE_3D:
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_TEXTURE_3D)
            glLibSelectTexture(texture)
            glBegin(GL_QUADS)
            # Right face
            if normalflip: glNormal3f( 1.0, 0.0, 0.0)
            else: glNormal3f(-1.0, 0.0, 0.0)
            glTexCoord3f(1.0, 1.0, 1.0); glVertex3f( size[0],  size[1],  size[2]);glTexCoord3f(1.0, 0.0, 1.0); glVertex3f( size[0], -size[1],  size[2]);glTexCoord3f(1.0, 0.0, 0.0); glVertex3f( size[0], -size[1], -size[2]);glTexCoord3f(1.0, 1.0, 0.0); glVertex3f( size[0],  size[1], -size[2])
            # Left Face
            if normalflip: glNormal3f(-1.0, 0.0, 0.0)
            else: glNormal3f( 1.0, 0.0, 0.0)
            glTexCoord3f(0.0, 1.0, 1.0); glVertex3f(-size[0],  size[1],  size[2]);glTexCoord3f(0.0, 1.0, 0.0); glVertex3f(-size[0],  size[1], -size[2]);glTexCoord3f(0.0, 0.0, 0.0); glVertex3f(-size[0], -size[1], -size[2]);glTexCoord3f(0.0, 0.0, 1.0); glVertex3f(-size[0], -size[1],  size[2])
            # Top Face
            if normalflip: glNormal3f( 0.0, 1.0, 0.0)
            else: glNormal3f( 0.0, -1.0, 0.0)
            glTexCoord3f(0.0, 1.0, 0.0); glVertex3f(-size[0],  size[1], -size[2]);glTexCoord3f(0.0, 1.0, 1.0); glVertex3f(-size[0],  size[1],  size[2]);glTexCoord3f(1.0, 1.0, 1.0); glVertex3f( size[0],  size[1],  size[2]);glTexCoord3f(1.0, 1.0, 0.0); glVertex3f( size[0],  size[1], -size[2])
            # Bottom Face
            if normalflip: glNormal3f( 0.0,-1.0, 0.0)
            else: glNormal3f( 0.0, 1.0, 0.0)
            glTexCoord3f(1.0, 0.0, 1.0); glVertex3f( size[0], -size[1],  size[2]);glTexCoord3f(0.0, 0.0, 1.0); glVertex3f(-size[0], -size[1],  size[2]);glTexCoord3f(0.0, 0.0, 0.0); glVertex3f(-size[0], -size[1], -size[2]);glTexCoord3f(1.0, 0.0, 0.0); glVertex3f( size[0], -size[1], -size[2])
            # Front Face
            if normalflip: glNormal3f( 0.0, 0.0,-1.0)
            else: glNormal3f( 0.0, 0.0, 1.0)
            glTexCoord3f(1.0, 1.0, 0.0); glVertex3f( size[0],  size[1], -size[2]);glTexCoord3f(1.0, 0.0, 0.0); glVertex3f( size[0], -size[1], -size[2]);glTexCoord3f(0.0, 0.0, 0.0); glVertex3f(-size[0], -size[1], -size[2]);glTexCoord3f(0.0, 1.0, 0.0); glVertex3f(-size[0],  size[1], -size[2])
            # Back Face
            if normalflip: glNormal3f( 0.0, 0.0, 1.0)
            else: glNormal3f( 0.0, 0.0,-1.0)
            glTexCoord3f(0.0, 0.0, 1.0); glVertex3f(-size[0], -size[1],  size[2]);glTexCoord3f(1.0, 0.0, 1.0); glVertex3f( size[0], -size[1],  size[2]);glTexCoord3f(1.0, 1.0, 1.0); glVertex3f( size[0],  size[1],  size[2]);glTexCoord3f(0.0, 1.0, 1.0); glVertex3f(-size[0],  size[1],  size[2])
            glEnd()
            glDisable(GL_TEXTURE_3D)
            glEnable(GL_TEXTURE_2D)
        elif texture != False:
            # Right face
            glLibSelectTexture(texture[0])
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 1.0, 0.0, 0.0)
            else: glNormal3f(-1.0, 0.0, 0.0)
            glTexCoord2f(1.0, 0.0); glVertex3f( size[0],  size[1],  size[2]);glTexCoord2f(1.0, 1.0); glVertex3f( size[0], -size[1],  size[2]);glTexCoord2f(0.0, 1.0); glVertex3f( size[0], -size[1], -size[2]);glTexCoord2f(0.0, 0.0); glVertex3f( size[0],  size[1], -size[2])
            glEnd()
            # Left Face
            glLibSelectTexture(texture[1])
            glBegin(GL_QUADS)
            if normalflip: glNormal3f(-1.0, 0.0, 0.0)
            else: glNormal3f( 1.0, 0.0, 0.0)
            glTexCoord2f(0.0, 0.0); glVertex3f(-size[0],  size[1],  size[2]);glTexCoord2f(1.0, 0.0); glVertex3f(-size[0],  size[1], -size[2]);glTexCoord2f(1.0, 1.0); glVertex3f(-size[0], -size[1], -size[2]);glTexCoord2f(0.0, 1.0); glVertex3f(-size[0], -size[1],  size[2])
            glEnd()
            # Top Face
            glLibSelectTexture(texture[2])
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 0.0, 1.0, 0.0)
            else: glNormal3f( 0.0, -1.0, 0.0)
            glTexCoord2f(0.0, 1.0); glVertex3f(-size[0],  size[1], -size[2]);glTexCoord2f(0.0, 0.0); glVertex3f(-size[0],  size[1],  size[2]);glTexCoord2f(1.0, 0.0); glVertex3f( size[0],  size[1],  size[2]);glTexCoord2f(1.0, 1.0); glVertex3f( size[0],  size[1], -size[2])
            glEnd()
            # Bottom Face
            glLibSelectTexture(texture[3])
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 0.0,-1.0, 0.0)
            else: glNormal3f( 0.0, 1.0, 0.0)
            glTexCoord2f(1.0, 1.0); glVertex3f( size[0], -size[1],  size[2]);glTexCoord2f(0.0, 1.0); glVertex3f(-size[0], -size[1],  size[2]);glTexCoord2f(0.0, 0.0); glVertex3f(-size[0], -size[1], -size[2]);glTexCoord2f(1.0, 0.0); glVertex3f( size[0], -size[1], -size[2])
            glEnd()
            # Front Face
            glLibSelectTexture(texture[4])
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 0.0, 0.0,-1.0)
            else: glNormal3f( 0.0, 0.0, 1.0)
            glTexCoord2f(1.0, 0.0); glVertex3f( size[0],  size[1], -size[2]);glTexCoord2f(1.0, 1.0); glVertex3f( size[0], -size[1], -size[2]);glTexCoord2f(0.0, 1.0); glVertex3f(-size[0], -size[1], -size[2]);glTexCoord2f(0.0, 0.0); glVertex3f(-size[0],  size[1], -size[2])
            glEnd()
            # Back Face
            glLibSelectTexture(texture[5])
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 0.0, 0.0, 1.0)
            else: glNormal3f( 0.0, 0.0,-1.0)
            glTexCoord2f(1.0, 1.0); glVertex3f(-size[0], -size[1],  size[2]);glTexCoord2f(0.0, 1.0); glVertex3f( size[0], -size[1],  size[2]);glTexCoord2f(0.0, 0.0); glVertex3f( size[0],  size[1],  size[2]);glTexCoord2f(1.0, 0.0); glVertex3f(-size[0],  size[1],  size[2])
            glEnd()
        else:
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 1.0, 0.0, 0.0)
            else: glNormal3f(-1.0, 0.0, 0.0)
            glVertex3f( size[0],  size[1],  size[2]);glVertex3f( size[0], -size[1],  size[2]);glVertex3f( size[0], -size[1], -size[2]);glVertex3f( size[0],  size[1], -size[2])
            glEnd()
            # Left Face
            glBegin(GL_QUADS)
            if normalflip: glNormal3f(-1.0, 0.0, 0.0)
            else: glNormal3f( 1.0, 0.0, 0.0)
            glVertex3f(-size[0],  size[1],  size[2]);glVertex3f(-size[0],  size[1], -size[2]);glVertex3f(-size[0], -size[1], -size[2]);glVertex3f(-size[0], -size[1],  size[2])
            glEnd()
            # Top Face
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 0.0, 1.0, 0.0)
            else: glNormal3f( 0.0, -1.0, 0.0)
            glVertex3f(-size[0],  size[1], -size[2]);glVertex3f(-size[0],  size[1],  size[2]);glVertex3f( size[0],  size[1],  size[2]);glVertex3f( size[0],  size[1], -size[2])
            glEnd()
            # Bottom Face
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 0.0,-1.0, 0.0)
            else: glNormal3f( 0.0, 1.0, 0.0)
            glVertex3f( size[0], -size[1],  size[2]);glVertex3f(-size[0], -size[1],  size[2]);glVertex3f(-size[0], -size[1], -size[2]);glVertex3f( size[0], -size[1], -size[2])
            glEnd()
            # Front Face
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 0.0, 0.0,-1.0)
            else: glNormal3f( 0.0, 0.0, 1.0)
            glVertex3f( size[0],  size[1], -size[2]);glVertex3f( size[0], -size[1], -size[2]);glVertex3f(-size[0], -size[1], -size[2]);glVertex3f(-size[0],  size[1], -size[2])
            glEnd()
            # Back Face
            glBegin(GL_QUADS)
            if normalflip: glNormal3f( 0.0, 0.0, 1.0)
            else: glNormal3f( 0.0, 0.0,-1.0)
            glVertex3f(-size[0], -size[1],  size[2]);glVertex3f( size[0], -size[1],  size[2]);glVertex3f( size[0],  size[1],  size[2]);glVertex3f(-size[0],  size[1],  size[2])
            glEnd()
        glEndList()
    def draw(self):
        glCallList(self.box)
class glLibGrid2D:
    def __init__(self,size):
        if type(size) in [type([]),type(())]:
            self.size = list(size)
        else:
            self.size = [size,size]
        self.size_grid = self.size[0] * self.size[1]
        threedimensionalgrid = np.array(np.dstack(np.mgrid[0:self.size[0],0:self.size[1],0:1]),
                                             dtype="f")\
                                             /np.array([self.size[0]-1.0,self.size[1]-1.0,1.],dtype="f")
        twodimensionalgrid = threedimensionalgrid.reshape(self.size_grid,3)
        self.vertex_vbo = vbo.VBO(twodimensionalgrid)
    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        self.vertex_vbo.bind()
        glVertexPointerf(self.vertex_vbo)
        glDrawArrays(GL_POINTS,0,self.size_grid)
        glBindBuffer(GL_ARRAY_BUFFER,0)
        glDisableClientState(GL_VERTEX_ARRAY)
    def __del__(self):
        self.vertex_vbo.delete()
class glLibGrid2DMesh:
    def __init__(self,size,loop=[False,False]):#,meshtype=GL_TRIANGLE_STRIP):
        if type(size) in [type([]),type(())]:
            self.size = list(size)
        else:
            self.size = [size,size]
        self.size = [self.size[0]-1,self.size[1]-1]
        size = self.size
        self.loop = loop
        fsize = map(float,self.size)
        self.type = GL_TRIANGLE_STRIP#meshtype
        if self.type in [GL_TRIANGLE_STRIP,GL_QUAD_STRIP]:
            if self.loop[0]:
                zcol = np.zeros((size[0]+1)*(size[1]+1)*2)
                ypart = np.repeat(np.arange(size[1]+1.)/size[1], 2)
                ycol = np.array(list(ypart)*(size[0]+1))
                xbase = np.repeat(np.arange(size[0]+1) / fsize[0], 2*(size[1]+1))
                xadd = np.array([0., 1.]*(len(xbase)/2)) / fsize[0]
                xcol = xbase + xadd
                array = np.transpose([xcol, ycol, zcol])
            elif self.loop[1]: pass
            else:
                zcol = np.zeros(size[0]*(size[1]+1)*2)
                ypart = np.repeat(np.arange(size[1]+1.)/size[1], 2)
                ycol = np.array(list(ypart)*size[0])
                xbase = np.repeat(np.arange(size[0]) / fsize[0], 2*(size[1]+1))
                xadd = np.array([0., 1.]*(len(xbase)/2)) / fsize[0]
                xcol = xbase + xadd
                array = np.transpose([xcol, ycol, zcol])
            if self.type == GL_TRIANGLE_STRIP:
                #degenerate triangle addition
                step = 2*(self.size[1]+1)
                firstind = 2*(self.size[1]+1)-1
                first_insert = np.insert(array,        np.arange(firstind,   len(array       ), step  ), array.copy()[firstind  ::step], axis=0)
                array        = np.insert(first_insert, np.arange(firstind+2, len(first_insert), step+1), array.copy()[firstind+1::step], axis=0)
##            else:
##                #degenerate quadrilateral addition
##                step = 2*(self.size[1]+1)
##                firstind = 2*(self.size[1]+1)-1
##                first_insert  = np.insert(array,         np.arange(firstind,   len(array        ), step  ), array.copy()[firstind  ::step], axis=0)
##                second_insert = np.insert(first_insert,  np.arange(firstind+2, len(first_insert ), step+1), array.copy()[firstind+1::step], axis=0)
##                third_insert  = np.insert(second_insert, np.arange(firstind+4, len(second_insert), step+2), array.copy()[firstind+2::step], axis=0)
##                array         = np.insert(third_insert,  np.arange(firstind+6, len(third_insert ), step+3), array.copy()[firstind+3::step], axis=0)
##        if self.type == GL_QUADS:
##            array = []
##            for x in xrange(self.size[0]-1):
##                for y in xrange(self.size[1]-1):
##                    array.append([ x   /fsize[0], y   /fsize[1],0.0])
##                    array.append([(x+1)/fsize[0], y   /fsize[1],0.0])
##                    array.append([(x+1)/fsize[0],(y+1)/fsize[1],0.0])
##                    array.append([ x   /fsize[0],(y+1)/fsize[1],0.0])
        self.vertex_vbo = vbo.VBO(np.array(array,"f"))
        self.arrsize = len(array)
    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        self.vertex_vbo.bind()
        glVertexPointerf(self.vertex_vbo)
        glDrawArrays(self.type,0,self.arrsize)
        glBindBuffer(GL_ARRAY_BUFFER,0)
        glDisableClientState(GL_VERTEX_ARRAY)
    def __del__(self):
        self.vertex_vbo.delete()
##class glLibGrid3D:
##    def __init__(self,size):
##        if type(size) in [type([]),type(())]:
##            self.size = list(size)
##        else:
##            self.size = [size,size,size]
##        fsize = map(float,self.size)
##
##        x_col = np.repeat(np.repeat(np.arange(2*self.size[2]),self.size[0]),self.size[2])
##        y_col = np.repeat(np.tile  (np.arange(2*self.size[2]),self.size[1]),self.size[2])
##        z_col = np.tile(np.arange(self.size[2]),2*self.size[0]*self.size[2])
##        array = np.transpose([x_col,y_col,z_col])
##        array = np.array(array,"float")
####        array = array/np.array([])
##        self.vertex_vbo = vbo.VBO(np.array(array,"f"))
##        
##        array = np.tile(np.concatenate((np.tile([0,1],self.size[2]),[2,2])),self.size[0]*self.size[1])
##        print len(array)
##        self.vertex_attrib_vbo = vbo.VBO(np.array(array,"f"))
##        
##        self.arrsize = len(array)
##    def draw(self):
##        glEnableClientState(GL_VERTEX_ARRAY)
##        self.vertex_vbo.bind()
##        glVertexPointerf(self.vertex_vbo)
##        glDrawArrays(self.type,0,self.arrsize)
##        glBindBuffer(GL_ARRAY_BUFFER,0)
##        glDisableClientState(GL_VERTEX_ARRAY)
##    def __del__(self):
##        self.vertex_vbo.delete()
class glLibDoubleGrid3DMesh:
    def __init__(self,size):#,loop=[False,False]):#,meshtype=GL_TRIANGLE_STRIP):
        if type(size) in [type([]),type(())]:
            self.size = list(size)
        else:
            self.size = [size,size,size]
        fsize = map(float,self.size)
        self.type = GL_TRIANGLE_STRIP

        x_col = np.repeat(np.repeat(np.arange(self.size[0]),self.size[1]*self.size[2]),         2)
        y_col = np.repeat(np.tile(np.repeat(np.arange(self.size[1]),self.size[2]),self.size[0]),2)
        z_col = np.repeat(np.tile(np.arange(self.size[2]),self.size[0]*self.size[1]),           2)
        vertex_array = np.transpose([x_col,y_col,z_col])
        raw_data_length = len(vertex_array) #sans degenerate triangles
        step = 2*(self.size[2])
        firstind = 2*(self.size[2])-1
        first_insert = np.insert(vertex_array, np.arange(firstind,   len(vertex_array), step  ), vertex_array.copy()[firstind  ::step], axis=0)
        vertex_array = np.insert(first_insert, np.arange(firstind+2, len(first_insert), step+1), vertex_array.copy()[firstind+1::step], axis=0)
        vertex_array = vertex_array[:-1]
        
##        vertex_attrib_array = np.tile([0,1],raw_data_length/2)
##        step = 2*(self.size[2])
##        firstind = 2*(self.size[2])
##        first_insert        = np.insert(vertex_attrib_array,np.arange(firstind,   len(vertex_attrib_array), step  ), 2, axis=0)
##        vertex_attrib_array = np.insert(first_insert,       np.arange(firstind+1, len(first_insert       ), step+1), 2, axis=0)
##        vertex_attrib_array = vertex_attrib_array.reshape((-1,1))
##        vertex_attrib_array = np.array(vertex_attrib_array,"f")
        vertex_attrib_array = np.concatenate(( np.tile([0,1],self.size[2]), np.tile([1,0],self.size[2]) ))
##        print len(vertex_attrib_array),self.size[2],raw_data_length
##        vertex_attrib_array = np.concatenate(( np.tile([0,1],self.size[2]), np.tile([1,0],raw_data_length/2-self.size[2]) ))
##        print len(vertex_attrib_array)
        tile = raw_data_length/(4.0*self.size[2])
        vertex_attrib_array = np.tile(vertex_attrib_array,floor(tile))
        if tile-float(floor(tile)) != 0.0: vertex_attrib_array = np.concatenate(( vertex_attrib_array, np.tile([0,1],self.size[2]) ))
        step = 2*(self.size[2])
        firstind = 2*(self.size[2])
##        first_insert        = np.insert(vertex_attrib_array,np.arange(firstind,   len(vertex_attrib_array), step  ), 2, axis=0)
##        vertex_attrib_array = np.insert(first_insert,       np.arange(firstind+1, len(first_insert       ), step+1), 2, axis=0)
        first_insert        = np.insert(vertex_attrib_array,np.arange(firstind,  len(vertex_attrib_array),step  ),vertex_attrib_array.copy()[firstind  ::step], axis=0)
        vertex_attrib_array = np.insert(first_insert,       np.arange(firstind+2,len(first_insert       ),step+1),vertex_attrib_array.copy()[firstind+2::step], axis=0)
        vertex_attrib_array = vertex_attrib_array.reshape((-1,1))
        vertex_attrib_array = np.array(vertex_attrib_array,"f")

##        vertex_array = np.concatenate((vertex_array,vertex_attrib_array.reshape((-1,1))),axis=1)
        vertex_array = vertex_array/np.array([self.size[0]-1.0,self.size[1]-1.0,self.size[2]-1.0])

        self.arrsize = len(vertex_array)

##        print vertex_array
##        print len(vertex_array), len(vertex_attrib_array)
##        print np.concatenate((vertex_array,vertex_attrib_array.reshape((-1,1))),axis=1)
        
        self.vertex_vbo = vbo.VBO(np.array(vertex_array,"f"))
        self.vertex_attrib_vbo = vbo.VBO(vertex_attrib_array)
        
    def draw(self,shader=None,var=None):
        if shader != None:
            try:location = glGetAttribLocation(shader.program,var)
            except:pass
        glEnableClientState(GL_VERTEX_ARRAY)
        if shader != None:
            try:glEnableVertexAttribArray(location)
            except:pass
        self.vertex_vbo.bind()
        glVertexPointerf(self.vertex_vbo)
        if shader != None:
            try:
                self.vertex_attrib_vbo.bind()
                glVertexAttribPointer(location,1,GL_FLOAT,GL_FALSE,0,None)
            except:pass
        glDrawArrays(self.type,0,self.arrsize)
        glBindBuffer(GL_ARRAY_BUFFER,0)
        if shader != None:
            try:glDisableVertexAttribArray(location)
            except:pass
        glDisableClientState(GL_VERTEX_ARRAY)
    def __del__(self):
        self.vertex_vbo.delete()
