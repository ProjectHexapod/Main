from ControlsKit import time_sources
from ControlsKit.math_utils import normalize, norm, arraysAreEqual
from UI import logger

class DumbFootMove:
    """
    This move just tries to move directly to the end position.  You must ensure
    that the end position is controlled in a reasonable way to avoid huge
    swings.
    
    """
    def __init__(self, leg_model, limb_controller, target_pos):
        logger.info("New trajectory.", traj_name="DumbFootMove",
                    final_foot_pos=final_foot_pos)
        
        self.model = leg_model
        self.controller = limb_controller
        self.target_foot_pos = target_foot_pos

    def isDone(self):
        return False

    def update(self):
        return self.model.jointAnglesFromFootPos(self.target_foot_pos, 0)
