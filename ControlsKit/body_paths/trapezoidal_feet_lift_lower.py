from ControlsKit import time_sources, leg_model, leg_paths
from ControlsKit.leg_paths import TrapezoidalFootMove
from ControlsKit.math_utils import NUM_LEGS, array
from UI import logger
from scipy import zeros, append

class TrapezoidalFeetLiftLower:
    """This path aligns all the feet to a given set of angles via a trapezoidal velocity profile
    """
    
    #TODO: check to make sure all legs are on the ground first
    
    def __init__(self, body_model, body_controller, leg_indices, delta_heights, max_velocity, acceleration):
        logger.info("New path.", path_name="TrapezoidalFeetLiftLower",
                    leg_indices= leg_indices, delta_height=delta_heights, 
                    max_velocity=max_velocity, acceleration=acceleration)
        
        self.leg_indices=leg_indices
        self.model = body_model
        self.controller = body_controller
        
        self.final_joint_positions = self.controller.getTargetJointAngleMatrix()#self.model.getJointAngleMatrix()
        
        self.foot_paths = [None for i in range(NUM_LEGS)]
        
        if type(delta_heights) == type(1.0):
            delta_heights = [delta_heights]*6
        
        for i in self.leg_indices:
            current_leg_pos = self.model.getLegs()[i].footPosFromLegState([self.controller.getTargetJointAngleMatrix()[i],0])#self.model.getFootPositions()[i]
            desired_leg_pos = current_leg_pos + [0,0,delta_heights[i]]

            self.foot_paths[i]=TrapezoidalFootMove(
                self.model.getLegs()[i],
                self.controller.getLimbControllers()[i],
                desired_leg_pos,
                max_velocity, acceleration)
        
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done:
            #logically and all of the isdone results from the trapezoidal joint move paths
            activepaths=[self.foot_paths[i] for i in self.leg_indices]
            self.done = reduce(lambda x,y: x and y, map(TrapezoidalFootMove.isDone, activepaths))
            for i in self.leg_indices:
                self.final_joint_positions[i] = self.foot_paths[i].update()
            return self.final_joint_positions
