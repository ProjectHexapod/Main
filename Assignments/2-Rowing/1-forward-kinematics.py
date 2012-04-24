from math import pi

def jointAnglesFromFootPosition( hip_yaw_angle, hip_pitch_angle, knee_angle, robot ):
    # YOUR ASSIGNMENT: 
    # return the angles of the joints in a leg given the position of
    # the foot relative to the origin of the leg.
    # 
    # The origin of the leg is where the leg is attached to the cart,
    # at the root of the hip yaw joint.
    # 
    # All lengths are in meters, all angles in radians
    #
    # Robot link lengths are in:
    # robot.YAW_L  
    # robot.THIGH_L
    # robot.CALF_L
    # Joint angles are positive in the direction of cylinder expansions.
    # Looking from above, positive hip yaw swings the leg clockwise
    # Positive hip pitch and knee pitch curl the leg under the robot

    ### YOUR CODE GOES HERE ###
    return (foot_x, foot_y, foot_z)
