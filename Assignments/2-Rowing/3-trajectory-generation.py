from math import pi

class Trajectory:
    def __init__( self, target_foot_pos, robot, start_sim_t, end_sim_t ):
	# YOUR ASSIGNMENT: 
	# 
	# The higher level code will request a trajectory in the form of a
	# start position, end position and time to traverse between them
	#
	# It is your job to provide target joint angles at regular intervals that will accomplish this task
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
	pass
    def getTargetJointAngles( self, sim_t ):
	return (hip_yaw, hip_pitch, knee_pitch)
