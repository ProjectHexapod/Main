from math import pi

class Trajectory:
    def __init__( self, start_foot_pos, target_foot_pos, robot, start_sim_t, end_sim_t ):
        self.start_sim_t = start_sim_t
        self.start_foot_pos = start_foot_pos
        net_time = end_sim_t - start_sim_t

        self.position_change = [t-s for t,s in zip(target_foot_pos, start_foot_pos)]
        average_velocity = [x/net_time for x in self.position_change]
        self.max_velocity = [(3./2) * x for x in average_velocity]
        self.acceleration = [x/(net_time / 3.) for x in self.max_velocity]
        self.time_cutoffs = [(end_sim_t - start_sim_t) * x + start_sim_t for x in [1/3.,2/3.,1.]]
        self.net_time = net_time



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

    def getTargetJointAngles( self, sim_t ):
        delta_pos = []
        t = sim_t - self.start_sim_t
        if sim_t <= self.time_cutoffs[0]:
            delta_pos = [t**2 * 0.5 * a for a in self.acceleration]
        elif sim_t <= self.time_cutoffs[1]:
            t -= self.net_time/3.
            delta_pos = [pd/4. + vm * t for pd,vm in zip(self.position_change, self.max_velocity)]
        elif sim_t <= self.time_cutoffs[2]:
            t -= 2.*self.net_time/3.
            delta_pos = [3.*pd/4. + t*vm - t**2 * a/2. for pd,vm,a in zip(self.position_change,
                self.max_velocity, self.acceleration)]

        foot_pos = [sp+ep for sp,ep in zip(self.start_foot_pos, delta_pos)]
        return foot_pos






