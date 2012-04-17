
def control( sim_time, hip_yaw_angle, hip_pitch_angle, knee_angle ):
    ### YOUR CODE GOES HERE ###
    hip_yaw_lrate   = 0.01
    hip_pitch_lrate = 0.00
    knee_lrate      = 0.00
    return (hip_yaw_lrate, hip_pitch_lrate, knee_lrate)
