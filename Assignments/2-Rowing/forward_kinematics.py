from math import *


def footPositionFromJointAngles(hip_yaw_angle, hip_pitch_angle, knee_angle, shock_depth, robot):
    pos = (0, 0, 0)
    pos = translate(pos, (robot.CALF_L + shock_depth, 0, 0))
    pos = rotate_y(pos, -knee_angle)
    pos = translate(pos, (robot.THIGH_L, 0, 0))
    pos = rotate_y(pos, -hip_pitch_angle)
    pos = translate(pos, (robot.YAW_L, 0, 0))
    pos = rotate_z(pos, -hip_yaw_angle)
    return pos


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
