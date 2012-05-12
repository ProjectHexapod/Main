from scipy import array, arange, pi, cos, sin


LEG_DOF = 3

# Indices for joint angles
YAW = 0
HP = 1
KP = 2

# Indices for Cartesian positions
X = 0
Y = 1
Z = 2


# Compare two arrays. Use tolerance to account for arithmetic error.
def arraysAreEqual(a, b, tolerance=1e-9):
    return max(abs(a - b)) <= tolerance

# Rotate about the X axis
def rotateX(vector, angle):
    c, s = cos(angle), sin(angle)
    x = vector[0]
    y = c*vector[1] - s*vector[2]
    z = s*vector[1] + c*vector[2]
    return array([x, y, z])

# Rotate about the Y axis
def rotateY(vector, angle):
    c, s = cos(angle), sin(angle)
    x = c*vector[0] + s*vector[2]
    y = vector[1]
    z = -s*vector[0] + c*vector[2]
    return array([x, y, z])

# Rotate about the Z axis
def rotateZ(vector, angle):
    c, s = cos(angle), sin(angle)
    x = c*vector[0] - s*vector[1]
    y = s*vector[0] + c*vector[1]
    z = vector[2]
    return array([x, y, z])
