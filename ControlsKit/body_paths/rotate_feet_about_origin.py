from ControlsKit import time_sources, leg_model, leg_paths, leg_logger
from ControlsKit.leg_paths import RotateFootAboutOrigin
from ControlsKit.math_utils import NUM_LEGS
from scipy import zeros, append, array

class RotateFeetAboutOrigin:
    """This path rotates some of the feet by a given angle about the vertical axis at the origin via a trapezoidal velocity profile
    """
    
    #TODO: check to make sure all legs are on the ground first
    
    def __init__(self, body_model, body_controller, leg_indices, delta_angle, max_velocity, acceleration):
        leg_logger.logger.info("New path.", path_name="RotateFeetAboutOrigin",
                    delat_angle=delta_angle, leg_indices = leg_indices, max_velocity=max_velocity,
                    acceleration=acceleration)
        
        self.model = body_model
        self.controller = body_controller
        self.leg_indices = leg_indices
        self.final_joint_positions = self.model.getJointAngleMatrix()
        self.feet_path = []
        self.delta_angle = delta_angle
        
        for i in self.leg_indices:
            self.feet_path = append(self.feet_path, RotateFootAboutOrigin(
                self.model,
                self.controller,
                i,
                self.delta_angle,
                max_velocity,
                acceleration))
        
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done:
            #logically and all of the isdone results from the trapezoidal joint move paths
            self.done = reduce(lambda x,y: x and y, map(RotateFootAboutOrigin.isDone, self.feet_path))
            for i in self.leg_indices:
                self.final_joint_positions[i] = self.feet_path[i].update()
            return self.final_joint_positions

