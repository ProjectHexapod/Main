from math import pi

def sign(i):
    if i >= 0:
        return 1
    return -1

def control( sim_time, hip_yaw_angle, hip_pitch_angle, knee_angle ):
    ### YOUR CODE GOES HERE ###
    if sim_time < 3:
        hip_yaw_lrate   = 0.00
        hip_pitch_lrate = 0.25*(-pi/8-hip_pitch_angle)
        knee_lrate      = 0.25*(2*pi/3-knee_angle)
    elif sim_time < 5:
        hip_yaw_lrate   = 0.25*(0-hip_yaw_angle)
        hip_pitch_lrate = 0.00
        knee_lrate      = 0.00
    else:
        hip_yaw_lrate   = 0.00
        hip_pitch_lrate = 0.00
        knee_lrate      = 0.2*(0-knee_angle)
        
    return (hip_yaw_lrate, hip_pitch_lrate, knee_lrate)
