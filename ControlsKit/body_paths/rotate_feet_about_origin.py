from ControlsKit import time_sources, leg_model, leg_paths
from ControlsKit.leg_paths import RotateFootAboutOrigin
from ControlsKit.math_utils import NUM_LEGS
from UI import logger
from scipy import zeros, append, array


class RotateFeetAboutOrigin:
    """
    This path rotates some of the feet by a given angle about the vertical axis at the origin
    via a trapezoidal velocity profile
    """
    
    #TODO: check to make sure all legs are on the ground first
    
    def __init__(self, body_model, body_controller, leg_indices, delta_angle, max_velocity, acceleration):
        logger.info("New path.",
                    path_name="RotateFeetAboutOrigin",
                    delta_angle=delta_angle,
                    leg_indices=leg_indices,
                    max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.model = body_model
        self.controller = body_controller
        self.leg_indices = leg_indices
        self.final_joint_positions = self.model.getJointAngleMatrix()
        self.foot_paths = [None for i in range(NUM_LEGS)]
        self.delta_angle = delta_angle
        
        for i in self.leg_indices:
            self.foot_paths[i] = RotateFootAboutOrigin(self.model,
                                                       self.controller,
                                                       i,
                                                       self.delta_angle,
                                                       max_velocity,
                                                       acceleration)
        
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done:
            #logically and all of the isdone results from the trapezoidal joint move paths
            activepaths = [self.foot_paths[i] for i in self.leg_indices]
            self.done = reduce(lambda x, y: x and y, map(RotateFootAboutOrigin.isDone, activepaths))
            for i in self.leg_indices:
                self.final_joint_positions[i] = self.foot_paths[i].update()
            return self.final_joint_positions
