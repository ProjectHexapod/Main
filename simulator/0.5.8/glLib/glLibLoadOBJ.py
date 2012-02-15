from glLibLocals import *
from glLibMath import *
from glLibTexturing import glLibTexture2D

def glLibInternal_Material(filename,filtering,mipmapping):
    contents = {}
    mtl = None
    mtlfilename = os.path.join(*filename[:-1]+[filename[-1][:-4]+".mtl"])
    for line in open(mtlfilename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError, "mtl file doesn't start with newmtl stmt"
        elif values[0] == 'map_Kd':
            surf = pygame.image.load(os.path.join(*filename[:-1]+[values[1]]))
            mtl['texture_Kd'] = glLibTexture2D(surf,GLLIB_ALL,GLLIB_RGBA,filtering,mipmapping)
        else:
            mtl[values[0]] = map(float, values[1:])
            if len(mtl[values[0]]) == 3: mtl[values[0]] = mtl[values[0]]+[1.0]
    return contents
 
def glLibInternal_LoadOBJFile(filename,filtering,mipmapping):
    vertices = []
    polygons = []
    normals = []
    texcoords = []
    faces = []

    face_type = None

    hasnormals = False
    hastexcoords = False
    hasmaterial = True

    filename = filename.split("/")
    mtllib = glLibInternal_Material(filename,filtering,mipmapping)

    material = None
    file = open(os.path.join(*filename),"r")
    for line in file.readlines():
        line = line.strip()
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if   values[0] == 'v' : vertices.append (map(float,values[1:4])); continue
        elif values[0] == 'vn': normals.append  (map(float,values[1:4])); hasnormals   = True; continue
        elif values[0] == 'vt': texcoords.append(map(float,values[1:3])); hastexcoords = True; continue
        elif values[0] == 'f' :
            facevertices = []
            facetexcoords = []
            facenormals = []
            for v in values[1:]:
                w = v.split('/')
                facevertices.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0: facetexcoords.append(int(w[1]))
                else:                             facetexcoords.append(0)
                if len(w) >= 3 and len(w[2]) > 0: facenormals.append(int(w[2]))
                else:                             facenormals.append(0)
            faces.append((facevertices,facenormals,facetexcoords,material))
            continue
        elif values[0] in ('usemtl','usemat'): material = values[1]; continue
        elif values[0] == 'mtllib': continue
    file.close()

##    currentcolor = glGetFloatv(GL_CURRENT_COLOR)
    lastmaterial = None
##    colorchanged = False
    materials = []
    
    vertexarrays = []
    normalarrays = []
    texturecoordarrays = []
    tbnvectorarrays = []
    
    vertexarray = []
    normalarray = []
    texturecoordarray = []
    tbnvectorarray = []
    for face in faces:
        vertexindices, normalindices, texcoordindices, material = face
        if face_type == None:
            if len(vertexindices) == 3: face_type = GL_TRIANGLES
            elif len(vertexindices) == 4: face_type = GL_QUADS
        else:
            if (len(vertexindices) == 3 and face_type == GL_TRIANGLES) or \
               (len(vertexindices) == 4 and face_type == GL_QUADS    ): pass
            else:
                raise glLibError("Object mixes polygon types!")
        facemtl = mtllib[material]
        currentmaterial = dict(facemtl)
        if lastmaterial != currentmaterial:
            if lastmaterial != None:
                vertexarrays.append(vertexarray)
                normalarrays.append(normalarray)
                texturecoordarrays.append(texturecoordarray)
                tbnvectorarrays.append(tbnvectorarray)
                materials.append(currentmaterial)
                vertexarray = []
                normalarray = []
                texturecoordarray = []
                tbnvectorarray = []
            lastmaterial = currentmaterial
        triangle = [[vertices[vertexindices[0]-1],vertices[vertexindices[1]-1],vertices[vertexindices[2]-1]]]
        polygons.append(triangle[0])
        if hastexcoords: triangle.append([texcoords[texcoordindices[0]-1],texcoords[texcoordindices[1]-1],texcoords[texcoordindices[2]-1]])
        if hasnormals:   triangle.append([normals[normalindices[0]-1],normals[normalindices[1]-1],normals[normalindices[2]-1]])
        if hastexcoords: tritangents = CalculateTangentArray(triangle)
        for index in xrange(3):
            vertexarray.append          (triangle[0][index])
            if hastexcoords:
                texturecoordarray.append(triangle[1][index])
                if hasnormals:
                    normalarray.append  (triangle[2][index])
            elif hasnormals:
                normalarray.append      (triangle[1][index])
            if hastexcoords:
                tbnvectorarray.append   (tritangents[index])
    vertexarrays.append(vertexarray)
    normalarrays.append(normalarray)
    texturecoordarrays.append(texturecoordarray)
    tbnvectorarrays.append(tbnvectorarray)
    materials.append(lastmaterial)
##    if colorchanged:
##        glColor4f(*currentcolor)

    tbnvectorarrays2 = []
    if hastexcoords:
        for array in tbnvectorarrays:
            nparray = np.zeros((len(array),4),'f')
            index = 0
            for element in array:
                nparray[index,0] = element[0]
                nparray[index,1] = element[1]
                nparray[index,2] = element[2]
                nparray[index,3] = element[3]
                index += 1
            tbnvectorarrays2.append(nparray.tostring())

    return face_type, \
           vertices, polygons, vertexarrays, \
           normalarrays, texturecoordarrays, tbnvectorarrays2, \
           materials, \
           hasnormals, hastexcoords, hasmaterial
def CalculateTangentArray(triangle):
    vertex1 = triangle[0][0]
    vertex2 = triangle[0][1]
    vertex3 = triangle[0][2]
    texcoord1 = triangle[1][0]
    texcoord2 = triangle[1][1]
    texcoord3 = triangle[1][2]
    x1 = vertex2[0]-vertex1[0]
    x2 = vertex3[0]-vertex1[0]
    y1 = vertex2[1]-vertex1[1]
    y2 = vertex3[1]-vertex1[1]
    z1 = vertex2[2]-vertex1[2]
    z2 = vertex3[2]-vertex1[2]
    s1 = texcoord2[0]-texcoord1[0]
    s2 = texcoord3[0]-texcoord1[0]
    t1 = texcoord2[1]-texcoord1[1]
    t2 = texcoord3[1]-texcoord1[1]
    divisor = ((s1*t2)-(s2*t1))
    if divisor == 0:
        divisor = 0.01
    r = 1.0/divisor
    sdir = ((t2*x1-t1*x2)*r,(t2*y1-t1*y2)*r,(t2*z1-t1*z2)*r)
    tdir = ((s1*x2-s2*x1)*r,(s1*y2-s2*y1)*r,(s1*z2-s2*z1)*r)
    tangents = []
    for i in xrange(3):
        n = triangle[2][i]
        t = sdir
        tangent = normalize(vec_subt(t,sc_vec(dot(n,t),n)))
        if dot(cross(n,t),tdir) < 0.0: tangent.append(-1.0)
        else:                          tangent.append( 1.0)
        tangents.append(map(float,tangent))
    return tangents
