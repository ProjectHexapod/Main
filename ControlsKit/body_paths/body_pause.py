from ControlsKit import time_sources, leg_model, body_model, body_controller, leg_paths
from ControlsKit.leg_paths import Pause
from scipy import zeros, append
from ControlsKit.math_utils import NUM_LEGS, array
from UI import logger


class BodyPause:
    """
    This path pauses the hexapod body by pausing the legs
    """
    def __init__(self, body_model, body_controller, duration):
        logger.info("New path.",
                    path_name="BodyPause",
                    duration=duration)
        
        self.body = body_model
        self.body_controller = body_controller
        self.duration = duration
        self.feet_path = []
        
        current_positions = self.body.getFootPositions()
        for i in range(NUM_LEGS):
            self.feet_path = append(self.feet_path, Pause(self.body.getLegs()[i],
                                                          self.body_controller.getLimbControllers()[i],
                                                          self.duration))
            
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done:
            #logically and all of the isdone results from the pause foot path
            self.done = reduce(lambda x, y: x and y, map(Pause.isDone, self.feet_path))
            return [self.feet_path[i].update() for i in range(NUM_LEGS)]
