from ControlsKit import time_sources, LegController, leg_trajectories, leg_logger
from math_utils import NUM_LEGS

class TrapezoidalSitStand:
    """This trajectory moves the hexapod body straight up or down with a trapezoidal velocity profile
    """
    
    def __init__(self, body_controller, final_height, max_velocity, acceleration):
        
        logger.info("New trajectory.", traj_name="TrapezoidalSitStand",
                    final_height=final_height, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.body = body_controller()
        
        current_positions = self.body.getFootPositions()
        for i in range (NUM_LEGS):
            self.target_foot_positions[0,i] = final_height
        
        for i in range (NUM_LEGS):
            self.tfm[i] = TrapezoidalFootMove(self.body.getLegs(i), target_foot_positions(i), max_velocity, acceleration)
            
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done():
            #logically and all of the 
            self.done = reduce(lambda x,y: x and y, map(TrapezoidalFootMove.isDone, self.tfm))
            
            return [self.tfm[i].update() for i in range (NUM_LEGS)]