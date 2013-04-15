from SimulationKit import helpers


def isRotationMatrix(rot):
    return len(rot) == 9

    
def isHomogeneousMatrix(trans):
    return len(trans) == 16 and trans[15] == 1.0

    
def isVector3(vec):
    return len(vec) == 3

    
def getMatrixColumn(trans, i):
    assert isHomogeneousMatrix(trans)
    assert i < 4

    return trans[i::4]

    
def getMatrixRow(trans, i):
    assert isHomogeneousMatrix(trans)
    assert i < 4

    return trans[4 * i:4 * i + 4]

    
def dot(a, b):
    assert len(a) == len(b)

    result = 0.0
    for i in range(len(a)):
        result = result + a[i] * b[i]

    return result

    
def rotationMatrixToHomogeneous(rot):
    assert isRotationMatrix(rot)

    return (rot[0], rot[1], rot[2], 0.0,
            rot[3], rot[4], rot[5], 0.0,
            rot[6], rot[7], rot[8], 0.0,
            0.0, 0.0, 0.0, 1.0)

    
def multiplyMatrices(*transforms):
    assert len(transforms) > 1
    assert all(map(isHomogeneousMatrix, transforms))

    result = transforms[0]

    for i in range(1, len(transforms)):
        new = [0] * 16
        for row in range(4):
            for column in range(4):
                new[row * 4 + column] = dot(getMatrixRow(result, row), getMatrixColumn(transforms[i], column))

        result = new

    return result

    
def multiplyMatrixVector(trans, vector):
    assert isHomogeneousMatrix(trans)
    assert isVector3(vector)

    homogeneousVector = vector[0], vector[1], vector[2], 1.0

    result = [0.0] * 4
    for row in range(4):
        result[row] = dot(getMatrixRow(trans, row), homogeneousVector)

    return result[0:3]

    
def createRotation(axis, angle):
    assert isVector3(axis)

    return rotationMatrixToHomogeneous(helpers.calcRotMatrix(axis, angle))

    
def createTranslation(vector):
    assert isVector3(vector)

    result = identity()
    result[3] = vector[0]
    result[7] = vector[1]
    result[11] = vector[2]

    return result

    
def inverse(trans):
    assert isHomogeneousMatrix(trans)

    result = [0.0] * 16
    result[0] = trans[0]
    result[5] = trans[5]
    result[10] = trans[10]
    result[15] = 1.0

    result[1] = trans[4]
    result[4] = trans[1]

    result[2] = trans[8]
    result[8] = trans[2]

    result[6] = trans[9]
    result[9] = trans[6]

    result[3] = -dot(trans[0:9:4], trans[3:12:4])
    result[7] = -dot(trans[1:10:4], trans[3:12:4])
    result[11] = -dot(trans[2:11:4], trans[3:12:4])

    return result

    
def identity():
    result = [0.0] * 16

    result[0] = 1.0
    result[5] = 1.0
    result[10] = 1.0
    result[15] = 1.0

    return result
