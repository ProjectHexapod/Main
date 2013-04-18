from limb_controller import LimbController


class BodyController:

    def __init__(self, leg_count=6):
        self.legs = [LimbController() for i in range(leg_count)]

    def update(self, current_angles, target_angles):
        map(LimbController.update, self.legs, current_angles, target_angles)
        self.target_angles = target_angles
        return [leg.getLengthRateCommands() for leg in self.legs]

    def getLimbControllers(self):
        return self.legs
    
    def getTargetJointAngleMatrix(self):
        return self.target_angles
