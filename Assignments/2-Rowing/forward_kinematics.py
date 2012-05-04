from math import *

def footPositionFromJointAngles( hip_yaw_angle, hip_pitch_angle, knee_angle, shock_depth, robot ):
    pos = (0, 0, 0)
    pos = translate(pos, (robot.CALF_L, 0, 0))
    pos = rotate_y(pos, -knee_angle)
    pos = translate(pos, (robot.THIGH_L, 0, 0))
    pos = rotate_y(pos, -hip_pitch_angle)
    pos = translate(pos, (robot.YAW_L, 0, 0))
    pos = rotate_z(pos, -hip_yaw_angle)
    pos = translate(pos, (0, 0, -shock_depth))
    return pos

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
