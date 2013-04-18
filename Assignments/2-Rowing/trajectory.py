__author__ = "Benjamin Hitov"

AV_MAX_VEL_RATIO = 3. / 2


class Trajectory:

    
    def __init__(self, start_foot_pos, target_foot_pos, robot, start_sim_t, end_sim_t):
        """
        Computes a path between two points as a function of time.
        Velocity increases at a constant rate for the first third
        of the allotted time, stays constant for the second third,
        then decreases back to zero during the final third.
        """
        self.start_sim_t = start_sim_t
        self.start_foot_pos = start_foot_pos
        self.target_foot_pos = target_foot_pos
        net_time = end_sim_t - start_sim_t

        #Compute delta between start and end vectors
        self.position_change = [target - start for target, start in zip(target_foot_pos, start_foot_pos)]
        average_velocity = [x / net_time for x in self.position_change]

        self.max_velocity = [AV_MAX_VEL_RATIO * v for v in average_velocity]

        # We accelerate from 0 to max_velocity in one third of net_time,
        # so acceleration = max_velocity / (one third net_time)
        self.acceleration = [x / (net_time / 3.) for x in self.max_velocity]

        # Precompute the time cutoffs in thirds
        self.time_cutoffs = [(end_sim_t - start_sim_t) * x + start_sim_t for x in [1 / 3., 2 / 3., 1.]]
        self.net_time = net_time


    # Does not actually calculate angles
    # function name left the same for compatibility
    def getTargetJointAngles(self, sim_t):
        """
        Positions are calculated using the kinematics formula x = x_0 + vt + 1/2 a t^2
        """

        # First, we compute only the change in position relative to the starting point
        delta_pos = []
        t = sim_t - self.start_sim_t

        # Constant acceleration, 0 initial velocity
        if sim_t <= self.time_cutoffs[0]:
            delta_pos = [(t ** 2) * 0.5 * a for a in self.acceleration]

        # Constant velocity, 0 acceleration
        elif sim_t <= self.time_cutoffs[1]:
            t -= self.net_time / 3.
            delta_pos = [pd / 4. + vm * t for pd, vm in zip(self.position_change, self.max_velocity)]

        # Initial velocity of max_velocity, constant negative acceleration
        elif sim_t <= self.time_cutoffs[2]:
            t -= 2. * self.net_time / 3.
            delta_pos = [3. * pd / 4. + t * vm - t ** 2 * a / 2. for pd, vm, a in zip(self.position_change,
                                                                                      self.max_velocity,
                                                                                      self.acceleration)]

        else:
            return self.target_foot_pos

        # Add the starting position to the position delta
        foot_pos = [sp + ep for sp, ep in zip(self.start_foot_pos, delta_pos)]
        return foot_pos

    # Same function as getTargetJointAngles, but with a sensical name
    def getTargetFootPosition(self, *args, **kwargs):
        return self.getTargetJointAngles(*args, **kwargs)
