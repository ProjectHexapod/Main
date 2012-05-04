from math import pi, sin, cos
from numpy import matrix, transpose, resize

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
    
    yawVector=matrix([robot.YAW_L,0,0]);
    thighVector=matrix([robot.THIGH_L,0,0]);
    calfVector=matrix([robot.CALF_L,0,0]);
    
    kneePos=pitchRotation(calfVector,knee_angle,matrix[0,0,0]);
    hipPos=pitchRotation(thighVector,hip_pitch_angle,kneePos);
    #Negated because we've been calculating the vector from foot to robot
    footpos=-yawRotation(yawVector,hip_yaw_angle,hipPos);
    
    foot_x=footpos[0,0];
    foot_y=footpos[1,0];
    foot_z=footpos[2,0];
    return (foot_x, foot_y, foot_z);

def yawRotation(vector, angle, offset):
	#Rotates a vector around the Z axis by an angle (uses radians)
	offset=toRowVector(offset);
	
	row1=[cos(angle),-sin(angle),0,offset[0,0]];
	row2=[sin(angle),cos(angle),0,offset[0,1]];
	row3=[0,0,1],offset[0,2];
	row4=[0,0,0,1];
	rotationMatrix=matrix([row1,row2,row3,row4]);
	
	homogenous=rotationMatrix*toHomogenous(vector);
	posVector=homogenous[0:3,0];
	return (posVector);

def pitchRotation(vector, angle, offset):
	#Rotates a vector around the Y axis by an angle (uses radians)
	offset=toRowVector(offset);
	
	row1=[cos(angle),0,sin(angle),offset[0,0]];
	row2=[0,1,0,offset[0,1]];
	row3=[-sin(angle),0,cos(angle),offset[0,2]];
	row4=[0,0,0,1]
	rotationMatrix=matrix([row1,row2,row3,row4]);
	
	homogenous=rotationMatrix*toHomogenous(vector);
	posVector=homogenous[0:3,0];
	return (posVector)

def rollRotation(vector, angle):
	#Rotates a vector around the X axis by an angle (uses radians)
	offset=toRowVector(offset);
	
	row1=[1,0,0,offset[0,0]];
	row2=[0,cos(angle),-sin(angle),offset[0,1]];
	row3=[0,sin(angle),cos(angle),offset[0,2]];
	row4=[0,0,0,1];
	rotationMatrix=matrix([row1,row2,row3,row4]);
	
	homogenous=rotationMatrix*toHomogenous(vector);
	posVector=homogenous[0:3,0];
	return (posVector);

def Translation(vector, offset):
	#Performs a purely translational transform on a vector
	offset=toColVector(offset);
	
	row1=[1,0,0,offset[0,0]];
	row2=[0,1,0,offset[1,0]];
	row3=[0,0,1,offset[2,0]];
	row4=[0,0,0,1];
	homogenous=rotationMatrix*toHomogenous(vector);
	posVector=homogenous[0:3,0];
	return (posVector);

def toColVector(vector):
	if vector.shape[1]!=1:
		colVector=transpose(vector);
	else:
		colVector=vector;
	if colVector.shape[1]!=1:
		raise ValueError("Vector is not 1-dimensional,"+
		" impossible to convert to column vector.")
	return colVector;

def toRowVector(vector):
	if vector.shape[0]!=1:
		rowVector=transpose(vector);
	else:
		colVector=vector;
	if rowVector.shape[0]!=1:
		raise ValueError("Vector is not 1-dimensional,"+
		" impossible to convert to row vector.")
	return rowVector;

def toHomogenous(vector):
	vector=toColVector(vector);
	homogenous=resize(vector,[4,1]);
	homogenous[3,0]=1
	return homogenous;
