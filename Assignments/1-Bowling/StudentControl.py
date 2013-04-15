#!/usr/bin/env python


def control(sim_time, hip_yaw_angle, hip_pitch_angle, knee_angle):
    ### YOUR CODE GOES HERE ###
    import math
    hip_yaw_lrate   = 0.00
    hip_pitch_lrate = 0.00
    knee_lrate      = 0.00

#    if knee_angle > 0+0.1:
#        knee_lrate = -0.1
#    elif knee_angle < 0-0.1:
#        knee_lrate = 0.1

    h1 = 1.1
    l1 = 0.11
    l2 = 1.372
    l3 = 1.283
    foot_pos_z = l2 * math.sin(-1 * hip_pitch_angle) + l3 * math.cos((3.14 / 2) + knee_angle + hip_pitch_angle) + h1
    foot_pos_r = l2 * math.cos(hip_pitch_angle) + l3 * math.sin((3.14 / 2) - knee_angle - hip_pitch_angle)
    foot_pos_a = hip_yaw_angle

    target_z = 0
    target_r = 0
    target_a = 2.289
#    target_b = 0.500
    target_b = 0
    target_c = 0
    gain_a = -0.2
    gain_b = -0.2
    gain_c = -0.2

    P1x = 0
    P1y = 1.1

#    knee_lrate = gain_a*(knee_angle - target_a)
#    hip_pitch_lrate = gain_b*(hip_pitch_angle - target_b)
#    hip_yaw_lrate = gain_c*(hip_yaw_angle - target_c)

    if sim_time > 2 and sim_time < 4:
        target_a = 0
        target_b = -0.5
        target_c = 0
        gain_a = -5
        gain_b = -2
        gain_c = -0.5

        P1x = 0
        P1y = 1.1

    knee_lrate = gain_a * (knee_angle - target_a)
    hip_pitch_lrate = gain_b * (hip_pitch_angle - target_b)
    hip_yaw_lrate = gain_c * (hip_yaw_angle - target_c)

#    print "hip_yaw_angle = ", hip_yaw_angle, "  hip_pitch_angle = ", hip_pitch_angle, "  knee_angle = ", knee_angle
    print "z = ", foot_pos_z, "  r = ", foot_pos_r
    print "\n"

    return (hip_yaw_lrate, hip_pitch_lrate, knee_lrate)
