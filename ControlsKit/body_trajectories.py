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
        self.body. #get current foot positions
        self.target_foot_positions = #store target foot positions 
        
        for i in range NUM_LEGS:
            tfm = [(TrapezoidalFootMove(self.body.getLegs(i), target_foot_positions(i), max_velocity, acceleration)]
            
    def update()