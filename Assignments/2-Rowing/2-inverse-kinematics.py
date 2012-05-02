from math import atan2, acos, sqrt

def __main__:
    footPositionFromJointAngles(
    return

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
    
    hip_yaw_angle=atan2(foot_x,foot_y);
    foot_ground_projection_magnitude=sqrt(foot_x**2+foot_y**2);
    
    #imaginary magnitude between foot and hip for law of cosines
    #based math
    hip_to_foot_magnitude=sqrt(
    (foot_ground_projection_magnitude-robot.YAW_L)**2+foot_z**2);
    
    #deriving helper angle between projected x axis and foot->hip vector
    a1=atan2(foot_z,foot_ground_projection_magnitude);
	#deriving helper angle between thigh and foot->hip vector
    a2=law_of_cosines(robot.THIGH_L,hip_to_foot_magnitude,robot.CALF_L);
    hip_pitch_angle=a1+a2;
    
    knee_angle=law_of_cosines(robot.THIGH_L,robot.CALF_L,
	hip_to_foot_magnitude);
    
    return (hip_yaw_angle, hip_pitch_angle, knee_angle);
   
def law_of_cosines(a,b,c):
	angle=acos((a**2+b**2-c**2)/2*a*b);
	return angle;
