from math import pi

def footPositionFromJointAngles( foot_x, foot_y, foot_z, robot ):
    # YOUR ASSIGNMENT: 
    # return the position of the foot in cartesion coordinates relative
    # to the origin of the leg given the angles of the leg joints.
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
    return (hip_yaw_angle, hip_pitch_angle, knee_angle)
    
