from ControlsKit import time_sources, leg_model, leg_paths, leg_logger
from ControlsKit.leg_paths import TrapezoidalJointMove, TrapezoidalFootMove
from ControlsKit.math_utils import NUM_LEGS, array
from scipy import zeros, append

class TrapezoidalFeetLiftLower:
    """This path aligns all the feet to a given set of angles via a trapezoidal velocity profile
    """
    
    #TODO: check to make sure all legs are on the ground first
    
    def __init__(self, body_model, body_controller, leg_indices, delta_height, max_velocity, acceleration):
        leg_logger.logger.info("New path.", path_name="TrapezoidalFeetLiftLower",
                    leg_indices= leg_indices, delta_height=delta_height, 
                    max_velocity=max_velocity, acceleration=acceleration)
        
        self.model = body_model
        self.controller = body_controller
        self.foot_paths = []
        
        for i in leg_indices:
            current_leg_pos = self.model.getFootPositions()[i]
            desired_leg_pos = current_leg_pos + [0,0,delta_height]

            self.foot_paths.append(TrapezoidalFootMove(
                self.model.getLegs()[i],
                self.controller.getLimbControllers()[i],
                desired_leg_pos,
                max_velocity, acceleration) )
        
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done:
            #logically and all of the isdone results from the trapezoidal joint move paths
            self.done = reduce(lambda x,y: x and y, map(TrapezoidalJointMove.isDone, self.feet_path))
            return [self.feet_path[i].update() for i in range (NUM_LEGS)]
