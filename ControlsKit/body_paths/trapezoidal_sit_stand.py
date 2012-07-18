from ControlsKit import time_sources, leg_model, leg_paths
from ControlsKit.leg_paths import TrapezoidalFootMove
from ControlsKit.math_utils import NUM_LEGS, array
from scipy import zeros, append
from UI import logger

class TrapezoidalSitStand:
    """This path moves the hexapod body straight up or down with a trapezoidal velocity profile
    """
    
    #TODO: check to make sure all legs are on the ground first
    
    def __init__(self, body_model, body_controller, final_height, max_velocity, acceleration):
        logger.info("New path.", path_name="TrapezoidalSitStand",
                    final_height=final_height, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.model = body_model
        self.controller = body_controller
        self.final_foot_positions = self.model.getFootPositions()
        self.feet_path = []
        
        for i in range (NUM_LEGS):
            self.final_foot_positions[i][2] = final_height
        for i in range (NUM_LEGS):
            self.feet_path = append(self.feet_path, TrapezoidalFootMove(
                self.model.getLegs()[i],
                self.controller.getLimbControllers()[i],
                self.final_foot_positions[i],
                max_velocity, acceleration))
        
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done:
            #logically and all of the isdone results from the trapezoidal foot move paths
            self.done = reduce(lambda x,y: x and y, map(TrapezoidalFootMove.isDone, self.feet_path))
            return [self.feet_path[i].update() for i in range (NUM_LEGS)]
