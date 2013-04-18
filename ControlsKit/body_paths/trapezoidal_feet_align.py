from ControlsKit import time_sources, leg_model, leg_paths, leg_logger
from ControlsKit.leg_paths import TrapezoidalJointMove
from ControlsKit.math_utils import NUM_LEGS, array
from scipy import zeros, append


class TrapezoidalFeetAlign:
    """
    This path aligns all the feet to a given set of angles via a trapezoidal velocity profile
    """
    
    #TODO: check to make sure all legs are not on the ground first
    
    def __init__(self, body_model, body_controller, final_angles, max_velocity, acceleration):
        leg_logger.logger.info("New path.",
                               path_name="TrapezoidalFeetAlign",
                               final_angles=final_angles,
                               max_velocity=max_velocity,
                               acceleration=acceleration)
        
        self.model = body_model
        self.controller = body_controller
        self.final_joint_positions = self.model.getJointAngleMatrix()
        self.feet_path = []e
        
        for i in range(NUM_LEGS):
            self.final_joint_positions[i] = final_angles
            
        for i in range(NUM_LEGS):
            self.feet_path.append(TrapezoidalJointMove(self.model.getLegs()[i],
                                                       self.controller.getLimbControllers()[i],
                                                       self.final_joint_positions[i],
                                                       max_velocity, acceleration))
            
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done:
            #logically and all of the isdone results from the trapezoidal joint move paths
            self.done = reduce(lambda x, y: x and y, map(TrapezoidalJointMove.isDone, self.feet_path))
            return [self.feet_path[i].update() for i in range(NUM_LEGS)]
