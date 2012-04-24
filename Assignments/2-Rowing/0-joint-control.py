from math import pi

def controlJoint( target_angle, joint, robot ):
    # YOUR ASSIGNMENT: 
    # 
    # Given the target angle on the joint, command a sane linear velocity
    # to make the joint hit the target angle.
    # You should think about not introducing sudden moveemnts in to the system
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
    return act_vel
