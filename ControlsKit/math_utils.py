import unittest
from math import acos, asin, atan, atan2
from scipy import array, arange, linspace, pi, cos, sin, dot
from scipy.linalg import norm


pi_2 = pi / 2.0
pi_4 = pi / 4.0

LEG_DOF = 3
NUM_LEGS = 6

# Indices for joint angles
YAW = 0
HP = 1
KP = 2

# Indices for Cartesian positions
X = 0
Y = 1
Z = 2

def saturate(x, lower_limit, upper_limit=None):
    # If only one parameter is supplied, use symmetric limits
    if upper_limit is None:
        upper_limit = lower_limit
        lower_limit = -upper_limit
    if x > upper_limit:
        return upper_limit
    elif x < lower_limit:
        return lower_limit
    else:
        return x

# Compare two arrays. Use tolerance to account for arithmetic error.
def arraysAreEqual(a, b, tolerance=1e-9):
    return max(abs(a - b)) <= tolerance
def arrayTypeEqualityFunction(a, b, msg=None):
    if not arraysAreEqual(a, b):
        raise unittest.TestCase.failureException(
                "Arrays are not equal:\n    " + str(a) + "\n    " + str(b))
def installArrayTypeEqualityFunction(test_case):
    test_case.addTypeEqualityFunc(type(array([])), arrayTypeEqualityFunction)

def normalize(vector):
    return vector / norm(vector)

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

# Determine if a gravity vector projects a point into a triangle
# Follows logic from http://www.blackpawn.com/texts/pointinpoly/default.html
def inTriangle(P, A, B, C, g = [0,0,-1]):
    # Recast 3-space in new basis vectors
    r = array(P)-array(A)
    x1 = array(B)-array(A)
    x2 = array(C)-array(A)
    x3 = -normalize(array(g))
    
    # Calculate all the relevant dot-products
    dr1 = dot(r,x1)
    dr2 = dot(r,x2)
    dr3 = dot(r,x3)
    d11 = dot(x1,x1)
    d12 = dot(x1,x2)
    d13 = dot(x1,x3)
    d22 = dot(x2,x2)
    d23 = dot(x2,x3)
    d33 = dot(x3,x3)
    
    # Recast the point P as a sum of factors of the new basis vectors (r = u*x1+v*x2+w*x3)
    u = (dr1-d12/(d22-d23*d23/d33)*(dr2-dr3*d23/d33)-d13/d33*(dr3-d23/(d22-d23*
            d23/d33)*(dr2-dr3*d23/d33)))/(d11+d12/(d22-d23*d23/d33)*(d13*d23/
            d33-d12)-d13/d33*(d13+d23/(d22-d23*d23/d33)*(d13*d23/d33-d12)))
    v = (dr2-dr3*d23/d33-u*(d12-d13*d23/d33))/(d22-d23*d23/d33)
    w = (dr3-u*d13-v*d23)/d33
    
    return (u-w*d13>0 and v-w*d23>0 and u+v-w*(d13+d23)<1)
    
