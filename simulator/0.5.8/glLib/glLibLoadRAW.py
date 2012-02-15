from glLibLocals import *
 
def glLibInternal_LoadRAWFile(filename):
    vertices = []
    faces = []

    face_type = None

    filename = filename.split("/")
    file = open(os.path.join(*filename),"rb")

    materials = []

    for line in file.readlines():
        values = line.split()
        if not values: continue
        if len(values)==9:
            v1,v2,v3, v4,v5,v6, v7,v8,v9 = values
            face = [(v1,v2,v3), (v4,v5,v6), (v7,v8,v9)]
        if len(values)==12:
            v1,v2,v3, v4,v5,v6, v7,v8,v9, v10,v11,v12 = values
            face = [(v1,v2,v3), (v4,v5,v6), (v7,v8,v9), (v10,v11,v12)]
        faces.append(face)
        if face_type == None:
            if len(face) == 3: face_type = GL_TRIANGLES
            elif len(face) == 4: face_type = GL_QUADS
        else:
            if (len(face) == 3 and face_type == GL_TRIANGLES) or \
               (len(face) == 4 and face_type == GL_QUADS    ): pass
            else:
                raise glLibError("Object mixes polygon types!")
        for vertex in face:
            vertices.append(map(float,vertex))
    file.close()

    return face_type, \
           vertices, faces, [vertices], \
           [[]], [[]], [[]], \
           [], \
           False, False, False

    

