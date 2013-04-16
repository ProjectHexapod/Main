from ControlsKit import time_sources, BodyModel, BodyController
from SimulationKit.helpers import *
from math import *

controller = BodyController()
model = BodyModel()

# Convenience multipliers...
deg2rad    = pi / 180
psi2pascal = 6894.76
inch2meter = 2.54e-2
pound2kilo = 0.455
gallon2cmps = 1 / 15850.4


def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates, command=None):
    global path, state, controller, model
    
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    x_scale         = 1.0
    y_scale         = 0.0
    z_scale         = 0.5
    rot_scale       = 0.0
    step_t          = 2.6
    swing_f         = 0.70
    down_f          = 0.15
    up_f            = 0.15
    stride_length   = 1.70    # length of a stride, m
    neutral_r_outer = inch2meter * 65
    neutral_r_inner = inch2meter * 70
    body_h          = inch2meter * 60
    max_rot         = pi / 3
    foot_lift_h     = 0.55    # how high to lift feet in m

    foot_positions = []

    def linearInterp(lo_val, hi_val, n, lo_n=0.0, hi_n=1.0):
        dval = hi_val - lo_val
        dn = hi_n - lo_n
        n -= lo_n
        return lo_val + dval * (n / dn)

    def sineInterp(lo_val, hi_val, n, lo_n=0.0, hi_n=1.0):
        dval = hi_val - lo_val
        dn = hi_n - lo_n
        n -= lo_n
        return lo_val + dval * (-.5 * cos(pi * n / dn) + 0.5)

    # gait_t is the place we are in within the gait cycle (complete 2-phase
    # motion)
    gait_phase = (time / (2 * step_t)) % 1
    # step_t is the time within the step
    step_phase = 2 * (gait_phase % 0.5)

    x_off_stance = y_off_stance = linearInterp(
        (-0.5 + down_f + up_f) * stride_length,
        (+0.5) * stride_length,
        step_phase,
        0.0,
        1.0)
    rot_stance = linearInterp(
        (-0.5 + down_f + up_f) * max_rot,
        (+0.5) * max_rot,
        step_phase,
        0.0,
        1.0)
    z_off_stance = 0.0

    if step_phase < swing_f:
        # Not transition
        x_off_swing  = y_off_swing = linearInterp(
            (+0.5) * stride_length,
            (-0.5) * stride_length,
            step_phase,
            0.0,
            swing_f)
        rot_swing = linearInterp(
            (+0.5) * max_rot,
            (-0.5) * max_rot,
            step_phase,
            0.0,
            swing_f)
        z_off_swing = foot_lift_h
    elif step_phase < swing_f + down_f:
        x_off_swing  = y_off_swing = linearInterp(
            (-0.5) * stride_length,
            (-0.5 + down_f) * stride_length,
            step_phase,
            swing_f,
            swing_f + down_f)
        rot_swing = linearInterp(
            (+0.5) * max_rot,
            (-0.5) * max_rot,
            step_phase,
            swing_f,
            swing_f + down_f)
        # foot down
        z_off_swing  = sineInterp(
            foot_lift_h,
            0,
            step_phase,
            swing_f,
            swing_f + down_f)
    else:
        # foot up
        x_off_swing  = y_off_swing = linearInterp(
            (-0.5 + down_f) * stride_length,
            (-0.5 + down_f + up_f) * stride_length,
            step_phase,
            swing_f + down_f,
            1)
        rot_swing = linearInterp(
            (+0.5) * max_rot,
            (-0.5) * max_rot,
            step_phase,
            swing_f + down_f,
            1)
        z_off_swing  = 0.0
        z_off_stance  = sineInterp(
            0,
            foot_lift_h,
            step_phase,
            swing_f + down_f,
            1)
    for i in range(6):
        # Neutral position in the leg coordinate frame
        if i in (1, 4):
            neutral_pos = (neutral_r_inner, 0, -body_h)
        else:
            neutral_pos = (neutral_r_outer, 0, -body_h)
        leg_offset = model.getHipOffset(i)
        # leg_offset holds (x_off, y_off, theta_off) of the hip
        tmp = rotateAxisAngle(neutral_pos, (0, 0, 1), leg_offset[2])
        # We need an (x,y,z) offset.  Assume z to be zero
        leg_offset[2] = 0.0
        x, y, z = add3(tmp, leg_offset)
        if (i % 2) ^ (gait_phase > step_phase):
            x -= x_off_swing * x_scale
            y -= y_off_swing * y_scale
            z += z_off_swing * z_scale
            # apply rotation offsets
            x, y = rot2((x, y), rot_scale * rot_swing)
        else:
            x -= x_off_stance * x_scale
            y -= y_off_stance * y_scale
            z += z_off_stance * z_scale
            # apply rotation offsets
            x, y = rot2((x, y), rot_scale * rot_stance)
        p = (x, y, z)
        foot_positions.append(p)
    legs = model.getLegs()
    
    joint_angles = []
    for i in range(6):
        foot_pos_in_leg_frame = model.transformBody2Leg(i, foot_positions[i])
        joint_angles.append(legs[i].jointAnglesFromFootPos(foot_pos_in_leg_frame, 0))
    return controller.update(model.getJointAngleMatrix(), joint_angles)
