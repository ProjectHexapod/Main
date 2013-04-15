from math import *
from numpy import matrix, transpose, resize


def jointAnglesFromFootPosition(pos, shock_depth, robot):
    hip_yaw_target = -atan2(pos[1], pos[0])
    pos = rotate_z(pos, hip_yaw_target)
    pos = translate(pos, (-robot.YAW_L, 0, 0))
    pitch = -atan2(pos[2], pos[0])
    pos = rotate_y(pos, pitch)
    aL, aC, aT = solve_triangle(pos[0], robot.CALF_L + shock_depth, robot.THIGH_L)
    hip_pitch_target = pitch - aC
    knee_target = pi - aL
    return hip_yaw_target, hip_pitch_target, knee_target


# rotate about the Y axis
def rotate_y(vector, angle):
    c, s = cos(angle), sin(angle)
    x = c * vector[0] - s * vector[2]
    y = vector[1]
    z = s * vector[0] + c * vector[2]
    return x, y, z


# rotate about the Z axis
def rotate_z(vector, angle):
    c, s = cos(angle), sin(angle)
    x = c * vector[0] - s * vector[1]
    y = s * vector[0] + c * vector[1]
    z = vector[2]
    return x, y, z


def translate(v1, v2):
    x = v1[0] + v2[0]
    y = v1[1] + v2[1]
    z = v1[2] + v2[2]
    return x, y, z


# calculate angles from sides of a triangle
def solve_triangle(a, b, c):
    A = acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
    B = acos((c ** 2 + a ** 2 - b ** 2) / (2 * c * a))
    C = acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
    return A, B, C
