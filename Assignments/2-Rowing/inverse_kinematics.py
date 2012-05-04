from math import atan2, acos, sqrt, sin, cos
from numpy import matrix, transpose, resize

def jointAnglesFromFootPosition( foot_x, foot_y, foot_z, robot ):
    #Given the (X,Y,Z) position of a three-jointed foot relative to an
    #"origin" mount point, derives requisite knee angles.
    #
    # Robot link lengths are in:
    # robot.YAW_L  
    # robot.THIGH_L
    # robot.CALF_L
    # Joint angles are positive in the direction of cylinder expansions.
    # Looking from above, positive hip yaw swings the leg clockwise
    # Positive hip pitch and knee pitch curl the leg under the robot
    
    #make a vector describing foot position relative to mount point.
    foot_vector=matrix([foot_x,foot_y,foot_z]);
    
    #Calculates yaw angle for hip (via atan, as leg is always in a plane
    #passing through the reference origin)
    hip_yaw_angle=atan2(foot_x,foot_y);
    
    #projects leg into a plane which is tangent to the hip vector
    #note to self: a good check for this is that the new y-component
    #will be 0
    foot_ground_projection=yawRotation(
        foot_vector,hip_yaw_angle,matrix([0,0,0]));
    
    #get magnitude of vector from hip pitch joint to foot
    #note that to do this, you must subtract the length between
    #the two hip joints from the projection length
    hip_to_foot_magnitude=sqrt(
    (foot_ground_projection[0,0]-robot.YAW_L)**2+
        foot_ground_projection[2,0]**2);
    
    #deriving helper angle between projected x axis and foot->hip vector
    a1=atan2(foot_ground_projection[2,0],foot_ground_projection[0,0]);
	#deriving helper angle between thigh and foot->hip vector
    a2=law_of_cosines(robot.THIGH_L,hip_to_foot_magnitude,robot.CALF_L);
    hip_pitch_angle=a1+a2;
    
    knee_angle=law_of_cosines([robot.THIGH_L,robot.CALF_L,
	hip_to_foot_magnitude]);
    
    return (hip_yaw_angle, hip_pitch_angle, knee_angle);
   
def law_of_cosines(sides):
	#Given a vector describing three sides of a triangle, 
	#returns a vector of the values of angles opposite respective sides
	angles=[]
	for i in range(0,3):
		a=sides[(i+2)%3];
		b=sides[(i+1)%3];
		c=sides[i]
		angles[i]=acos((a**2+b**2-c**2)/2*a*b);
	return angles;

def yawRotation(vector, angle, offset):
	#Rotates a vector around the Z axis by an angle (uses radians)
	#Returns a column vector of length 3
	offset=toRowVector(offset);
	
	#generate a homogenous rotation matrix based off of desired angle
	#and offset
	row1=[cos(angle),-sin(angle),0,offset[0,0]];
	row2=[sin(angle),cos(angle),0,offset[0,1]];
	row3=[0,0,1,offset[0,2]];
	row4=[0,0,0,1];
	rotationMatrix=matrix([row1,row2,row3,row4]);
	
	#Rotation and translation calculated via homogenous transform
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

def rollRotation(vector, angle, offset):
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
	translationMatrix=matrix([row1,row2,row3,row4]);
	
	homogenous=translationMatrix*toHomogenous(vector);
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
		rowVector=vector;
	if rowVector.shape[0]!=1:
		raise ValueError("Vector is not 1-dimensional,"+
		" impossible to convert to row vector.")
	return rowVector;

def toHomogenous(vector):
	vector=toColVector(vector);
	homogenous=resize(vector,[4,1]);
	homogenous[3,0]=1
	return homogenous;
