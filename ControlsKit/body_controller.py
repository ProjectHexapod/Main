from leg_controller import LegController
from math_utils import NUM_LEGS


class BodyController:
    def __init__(self):
        self.legs = [LegController(), LegController(), LegController(), LegController(), LegController(), LegController()]
        assert len(self.legs) == NUM_LEGS
        
    def setBodyState(self, leg_sensor_matrix, orientation, angular_rates):
        for i,leg in zip(range(NUM_LEGS), self.legs):
            leg.setLegState(*leg_sensor_matrix[i])
            leg.updateFootOnGround()
        self.orientation = orientation
        self.angular_rates = angular_rates
    
    def setDesiredJointAngles(self, joint_angle_matrix):
        for i,leg in zip(range(NUM_LEGS), self.legs):
            leg.setDesiredJointAngles(joint_angle_matrix[i])
            leg.updateLengthRateCommands()
    
    def getLengthRateCommands(self):
        return map(LegController.getLengthRateCommands, self.legs)
