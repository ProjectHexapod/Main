from math import pi

def control( sim_time, hip_yaw_angle, hip_pitch_angle, knee_angle ):
    ### YOUR CODE GOES HERE ###
    if sim_time < 1.5:
	hip_yaw_target = hip_yaw_angle
	hip_pitch_target = -pi/10
	knee_target = 2*pi/3
    elif sim_time < 3:
	hip_yaw_target   = 0
	hip_pitch_target = hip_pitch_angle
	knee_target      = knee_angle
    else:
	hip_yaw_target   = hip_yaw_angle
	hip_pitch_target = hip_pitch_angle
	knee_target      = 0
    hip_yaw_lrate   = .5*(hip_yaw_target   - hip_yaw_angle)
    hip_pitch_lrate = .5*(hip_pitch_target - hip_pitch_angle)
    knee_lrate      = .5*(knee_target      - knee_angle)
    return (hip_yaw_lrate, hip_pitch_lrate, knee_lrate)
