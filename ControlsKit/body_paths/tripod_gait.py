class TripodGait:
    '''
    Implements a two-phase tripod gait.
    '''

    def __init__(self, body_model, body_controller):
        self.model = body_model
        self.controller = body_controller
    
    def isDone(self):
        return True

    def update(self):
        return self.model.getJointAngleMatrix()
