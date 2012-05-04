from math import *
from numpy import matrix, transpose, resize

def jointAnglesFromFootPosition( pos, shock_depth, robot ):
    pos = translate(pos, (0, 0, shock_depth))
    hip_yaw_target = -atan2(pos[1], pos[0])
    pos = rotate_z(pos, hip_yaw_target)
    pos = translate(pos, (-robot.YAW_L, 0, 0))
    pitch = -atan2(pos[2], pos[0])
    pos = rotate_y(pos, pitch)
    aL, aC, aT = solve_triangle(pos[0], robot.CALF_L, robot.THIGH_L)
    hip_pitch_target = pitch - aC
    knee_target = pi - aL
    return hip_yaw_target, hip_pitch_target, knee_target
   
# Cartesian to polar
def c2p(x, y):
    l = sqrt(x**2 + y**2)
    a = atan2(y, x)
    return l, a

# polar to Cartesian
def p2c(l, a):
    x = l * cos(a)
    y = l * sin(a)
    return x, y

# rotate about the Y axis
def rotate_y(vector, angle):
    l, a = c2p(vector[0], vector[2])
    x, z = p2c(l, a + angle)
    return x, vector[1], z

# rotate about the Z axis
def rotate_z(vector, angle):
    l, a = c2p(vector[0], vector[1])
    x, y = p2c(l, a + angle)
    return x, y, vector[2]

def translate(v1, v2):
    x = v1[0] + v2[0]
    y = v1[1] + v2[1]
    z = v1[2] + v2[2]
    return x, y, z

# calculate angles from sides of a triangle
def solve_triangle(a, b, c):
    A = acos((b**2+c**2-a**2)/(2*b*c))
    B = acos((c**2+a**2-b**2)/(2*c*a))
    C = acos((a**2+b**2-c**2)/(2*a*b))
    return A, B, C
