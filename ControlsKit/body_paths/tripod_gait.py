from ControlsKit.math_utils import array, NUM_LEGS
from ControlsKit.body_paths import FeetVelocities

class TripodGait:
    '''
    Implements a two-phase tripod gait.
    '''

    def __init__(self, body_model):
        self.model = body_model
        self.fv_path = FeetVelocities(self.model)
        self.fv_path.setVelocities([array([0.2,0.0,0.0])] * NUM_LEGS)
    
    def isDone(self):
        return False
    def update(self):
        return self.fv_path.update()
