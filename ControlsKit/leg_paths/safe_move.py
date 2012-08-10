from ControlsKit import time_sources, leg_logger
from ControlsKit.math_utils import normalize, norm, arraysAreEqual
from ControlsKit.leg_paths import TrapezoidalFootMove, TrapezoidalJointMove

class SafeMove:
    """This is foot movement that combines up to two trapezoidal foot moves and up to one trapezoidal joint move to move the foot
        safely without fear of dragging on the ground.
        NOTE: The Z-plane is the highest horizontal plane that ensures a convex volume below it. 
        This is the boundary of where TrapFootMove is guaranteed to work, so we switch to TrapJointMove above it.
        It should be found via side-angle-side of the knee and calf links and the angle they make most folded up.
        We use only vertical motions below the Z-plane, as there is a high likelihood of hitting the ground.
    """
    def __init__(self, leg_model, limb_controller, final_foot_pos, max_velocity, acceleration, z_plane=-0.67865):
        leg_logger.logger.info("New path.", path_name="TrapezoidalFootMove",
                    final_foot_pos=final_foot_pos, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.model = leg_model
        self.controller = limb_controller
        self.final_foot_pos = final_foot_pos
        self.final_joint_angles = self.model.jointAnglesFromFootPos(final_foot_pos, shock_depth=0.0)
        self.max_vel = max_velocity
        self.vel = 0.0
        self.acc = acceleration
        self.z_plane = z_plane
        self.initial_foot_pos = self.model.footPosFromLegState([self.controller.getDesiredPosAngle(), 0])
        self.initial_joint_angles = self.controller.getDesiredPosAngle()
        self.target_angles = self.initial_joint_angles
        
        self.projected_initial = [self.initial_foot_pos[0], self.initial_foot_pos[1], z_plane]
        self.projected_final = [self.final_foot_pos[0], self.final_foot_pos[1], max(self.final_foot_pos[2],z_plane)]
        
        self.done = False
        
        self.LIFT = 1
        self.TRANSLATE = 2
        self.LOWER = 3
        self.state = self.LIFT
        
        self.path = TrapezoidalFootMove(self.model, self.controller, self.projected_initial, self.max_vel, self.acc)
        
        if self.initial_foot_pos[2] > self.z_plane:
            self.state = self.TRANSLATE
            self.path = TrapezoidalJointMove(self.model, self.controller, self.model.jointAnglesFromFootPos(self.projected_final), self.max_vel, self.acc)
    
    def isDone(self):
        return self.done

    def update(self):
        if not self.isDone():
            self.target_angles = self.path.update()
            self.done = self.path.isDone()
        
        if self.isDone():
            if self.state == self.LIFT:
                self.state = self.TRANSLATE
                self.path = TrapezoidalJointMove(self.model, self.controller, self.model.jointAnglesFromFootPos(self.projected_final), self.max_vel, self.acc)
                self.done = False
            elif self.state == self.TRANSLATE and self.final_foot_pos[2] < self.z_plane:
                self.state = self.LOWER
                self.path = TrapezoidalFootMove(self.model, self.controller, self.final_foot_pos, self.max_vel, self.acc)
                self.done = False
        
        
        return self.target_angles
