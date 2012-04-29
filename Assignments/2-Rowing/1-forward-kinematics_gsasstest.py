from math import pi, sin, cos
from numpy import matrix

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
    
    yawVector=(robot.YAW_L,0,0);
    thighVector=(robot.THIGH_L,0,0);
    calfVector(robot.CALF_L,0,0);
    
    kneePos=pitchRotation(calfVector,knee_angle);
    hipPos=pitchRotation(thighVector+kneePos,hip_pitch_angle);
    footpos=-yawRotation(yawVector+hipPos,hip_yaw_angle);
    return (foot_x, foot_y, foot_z);

def yawRotation(vector, angle):
	#Rotates a vector around the Z axis by an angle (uses radians)
	row1=[cos(angle),-sin(angle),0];
	row2=[sin(angle),cos(angle),0];
	row3=[0,0,1];
	rotationMatrix=matrix([row1,row2,row3]);ch 
	try:
		posVector=vector*rotationMatrix;
	except ValueError:
		posVector=transpose(vector)*rotationMatrix;
	return (posVector)
def pitchRotation(vector, angle):
	#Rotates a vector around the Y axis by an angle (uses radians)
	row1=[cos(angle),0,sin(angle)];
	row2=[0,1,0];
	row3=[-sin(angle),0,cos(angle)];
	rotationMatrix=matrix([row1,row2,row3]);
	try:
		posVector=vector*rotationMatrix;
	except ValueError:
		posVector=transpose(vector)*rotationMatrix;
	return (posVector)
def rollRotation(vector, angle):
	#Rotates a vector around the X axis by an angle (uses radians)
	row1=[1,0,0];
	row2=[0,cos(angle),-sin(angle)];
	row3=[0,sin(angle),cos(angle)];
	rotationMatrix=matrix([row1,row2,row3]);
	try:
		posVector=vector*rotationMatrix;
	except ValueError:
		posVector=transpose(vector)*rotationMatrix;
	return (posVector)
