from scipy import array, cos, sin


# Compare two arrays. Use tolerance to account for arithmetic error.
def arraysAreEqual(a, b, tolerance=1e-9):
    return max(abs(a - b)) <= tolerance

# Rotate about the Y axis
def rotateY(vector, angle):
    c, s = cos(angle), sin(angle)
    x = c*vector[0] - s*vector[2]
    y = vector[1]
    z = s*vector[0] + c*vector[2]
    return array([x, y, z])

# Rotate about the Z axis
def rotateZ(vector, angle):
    c, s = cos(angle), sin(angle)
    x = c*vector[0] - s*vector[1]
    y = s*vector[0] + c*vector[1]
    z = vector[2]
    return array([x, y, z])

def translate(v1, v2):
    return v1 + v2
