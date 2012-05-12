import unittest
from math import acos, asin, atan, atan2
from scipy import array, arange, pi, cos, sin
from scipy.linalg import norm


pi_2 = pi / 2.0
pi_4 = pi / 4.0

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
def arrayTypeEqualityFunction(a, b, msg=None):
    if not arraysAreEqual(a, b):
        raise unittest.TestCase.failureException(
                "Arrays are not equal:\n    " + str(a) + "\n    " + str(b))
def installArrayTypeEqualityFunction(test_case):
    test_case.addTypeEqualityFunc(type(array([])), arrayTypeEqualityFunction)

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

# Calculate angles from sides of a triangle
def solveTriangle(a, b, c):
    A = acos((b**2+c**2-a**2)/(2*b*c))
    B = acos((c**2+a**2-b**2)/(2*c*a))
    C = acos((a**2+b**2-c**2)/(2*a*b))
    return A, B, C
