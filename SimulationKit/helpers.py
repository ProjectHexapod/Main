from math import *
import time, platform

getSysTime = None
if platform.system() == "Windows":
    getSysTime = time.clock
else:
    getSysTime = time.time

def maxForce(bore_in, pressure_psi=2000.0):
    return pi * (bore_in/2.0 * 0.0254)**2 * (pressure_psi * 6894.76)

def thetaFromABC( a, b, c ):
    return acos( (a*a + b*b - c*c) / (2.0*a*b) )

def cFromThetaAB( theta, a, b ):
    return sqrt( a*a + b*b - 2.0*a*b*cos(theta) )

def calcAngularError( a1, a2 ):
    """Given two angles in radians what is 
	the difference between them?"""
    error = (a1%(2*pi))-(a2%(2*pi))
    if error > pi:
        error -= 2*pi
    elif error <= -1*pi:
        error += 2*pi
    return error

def rot2( p, r ):
    """ Rotate 2D point p by angle r """
    s = sin(r)
    c = cos(r)
    return (c*p[0]-s*p[1],s*p[0]+c*p[1])

def sub2( p1, p2 ):
    return (p1[0]-p2[0],p1[1]-p2[1])

def len2( p ):
    return sqrt( p[0]*p[0] + p[1]*p[1] )

def norm2( p ):
    l = len2(p)
    return (p[0]/l, p[1]/l)

def sign(x):
    """Returns 1.0 if x is positive, -1.0 if x is negative or zero."""
    if x > 0.0: return 1.0
    else: return -1.0

def len3(v):
    """Returns the length of 3-vector v."""
    return sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def neg3(v):
    """Returns the negation of 3-vector v."""
    return (-v[0], -v[1], -v[2])

def add3(a, b):
    """Returns the sum of 3-vectors a and b."""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def sub3(a, b):
    """Returns the difference between 3-vectors a and b."""
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def mul3(v, s):
    """Returns 3-vector v multiplied by scalar s."""
    return (v[0] * s, v[1] * s, v[2] * s)

def div3(v, s):
    """Returns 3-vector v divided by scalar s."""
    return (v[0] / s, v[1] / s, v[2] / s)

def dist3(a, b):
    """Returns the distance between point 3-vectors a and b."""
    return len3(sub3(a, b))

def norm3(v):
    """Returns the unit length 3-vector parallel to 3-vector v."""
    l = len3(v)
    if (l > 0.0): return (v[0] / l, v[1] / l, v[2] / l)
    else: return (0.0, 0.0, 0.0)

def dot3(a, b):
    """Returns the dot product of 3-vectors a and b."""
    return (a[0] * b[0] + a[1] * b[1] + a[2] * b[2])

def cross(a, b):
    """Returns the cross product of 3-vectors a and b."""
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0])

def project3(v, d):
    """Returns projection of 3-vector v onto unit 3-vector d."""
    return mul3(v, dot3(norm3(v), d))

def acosdot3(a, b):
    """Returns the angle between unit 3-vectors a and b."""
    x = dot3(a, b)
    if x < -1.0: return pi
    elif x > 1.0: return 0.0
    else: return acos(x)

def rotate3(m, v):
    """Returns the rotation of 3-vector v by 3x3 (row major) matrix m."""
    return (v[0] * m[0] + v[1] * m[1] + v[2] * m[2],
        v[0] * m[3] + v[1] * m[4] + v[2] * m[5],
        v[0] * m[6] + v[1] * m[7] + v[2] * m[8])

def invert3x3(m):
    """Returns the inversion (transpose) of 3x3 rotation matrix m."""
    return (m[0], m[3], m[6], m[1], m[4], m[7], m[2], m[5], m[8])

def zaxis(m):
    """Returns the z-axis vector from 3x3 (row major) rotation matrix m."""
    return (m[2], m[5], m[8])

def calcRotMatrix(axis, angle):
    """
    Returns the row-major 3x3 rotation matrix defining a rotation around axis by
    angle.
    """
    cosTheta = cos(angle)
    sinTheta = sin(angle)
    t = 1.0 - cosTheta
    return (
        t * axis[0]**2 + cosTheta,
        t * axis[0] * axis[1] - sinTheta * axis[2],
        t * axis[0] * axis[2] + sinTheta * axis[1],
        t * axis[0] * axis[1] + sinTheta * axis[2],
        t * axis[1]**2 + cosTheta,
        t * axis[1] * axis[2] - sinTheta * axis[0],
        t * axis[0] * axis[2] - sinTheta * axis[1],
        t * axis[1] * axis[2] + sinTheta * axis[0],
        t * axis[2]**2 + cosTheta)

def rotateAxisAngle(v, ax, ang):
    m = calcRotMatrix( ax, ang )
    return rotate3( m, v )

def makeOpenGLMatrix(r, p):
    """
    Returns an OpenGL compatible (column-major, 4x4 homogeneous) transformation
    matrix from ODE compatible (row-major, 3x3) rotation matrix r and position
    vector p.
    """
    return (
        r[0], r[3], r[6], 0.0,
        r[1], r[4], r[7], 0.0,
        r[2], r[5], r[8], 0.0,
        p[0], p[1], p[2], 1.0)

def getBodyRelVec(b, v):
    """
    Returns the 3-vector v transformed into the local coordinate system of ODE
    body b.
    """
    return rotate3(invert3x3(b.getRotation()), v)

def mul3x3Matrices( matrix1, matrix2 ):
    """Multiply matrices, assume 3x3 row major"""
    new_matrix = [0 for i in range(9)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                new_matrix[3*i+j] += matrix1[3*i+k]*matrix2[3*k+j]
    return new_matrix

def mul4x4Matrices( matrix1, matrix2 ):
    """Multiply matrices, assume 4x4 column major"""
    new_matrix = [0 for i in range(16)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                new_matrix[i+4*j] += matrix1[i+4*k]*matrix2[k+4*j]
    return new_matrix
