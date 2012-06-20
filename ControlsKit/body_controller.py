from limb_controller import LimbController

class BodyController:
    def __init__(self, leg_count=6):
        self.legs = [LimbController() for i in range(leg_count)]

    def update(self, leg_sensor_matrix, joint_angle_matrix):
        map(LimbController.update, *zip(self.legs, leg_sensor_matrix, joint_angle_matrix))
        return [leg.getLengthRateCommands() for leg in self.legs]

    def getLimbControllers(self):
        return self.legs