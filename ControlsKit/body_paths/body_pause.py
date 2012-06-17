from ControlsKit import time_sources, leg_model, Paths, leg_logger
from ControlsKit.Paths import Pause
from scipy import zeros, append
from ControlsKit.math_utils import NUM_LEGS, array

class BodyPause:
    """This path pauses the hexapod body by pausing the legs
    """
    def __init__(self, body_model, duration):
        leg_logger.logger.info("New path.", path_name="BodyPause",
                               duration = duration)
        
        self.body = body_model
        self.duration = duration
        self.feet_path = []
        
        current_positions = self.body.getFootPositions()
        for i in range (NUM_LEGS):
            self.feet_path = append(self.feet_path, Pause(self.body.getLegs()[i], self.duration))
            
        self.done = False
    
    def isDone(self):
        return self.done    
    
    def update(self):
        if not self.done:
            #logically and all of the isdone results from the pause foot path
            self.done = reduce(lambda x,y: x and y, map(Pause.isDone, self.feet_path))
            return [self.feet_path[i].update() for i in range (NUM_LEGS)]