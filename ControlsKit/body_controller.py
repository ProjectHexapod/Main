from ConfigParser import ConfigParser
from leg_controller import LegController
from math_utils import NUM_LEGS


class BodyController:
    def __init__(self, config_file="body_controller.conf", section="BodyController"):
        c = ConfigParser()
        c.read(config_file)
        
        #leg0_offset_x = c.getfloat(section, "leg0_offset_x")
        
        self.legs = [LegController(config_file, "GenericLeg"),
                     LegController(config_file, "GenericLeg"),
                     LegController(config_file, "GenericLeg"),
                     LegController(config_file, "GenericLeg"),
                     LegController(config_file, "GenericLeg"),
                     LegController(config_file, "GenericLeg")]
        assert len(self.legs) == NUM_LEGS
        
    def setSensorReadings(self, leg_sensor_matrix, imu_orientation, imu_angular_rates):
        for i,leg in zip(range(NUM_LEGS), self.legs):
            leg.setSensorReadings(*leg_sensor_matrix[i])
            leg.updateFootOnGround()
        self.imu_orientation = imu_orientation
        self.imu_angular_rates = imu_angular_rates
    
    def setDesiredJointAngles(self, joint_angle_matrix):
        for i,leg in zip(range(NUM_LEGS), self.legs):
            leg.setDesiredJointAngles(joint_angle_matrix[i])
            if not self.legsAreColliding():
                leg.updateLengthRateCommands()
    
    def getLengthRateCommands(self):
        return map(LegController.getLengthRateCommands, self.legs)

    def legsAreColliding(self):
        """ Get bounding boxes for the lower section of each of the six legs, and check them for
            intersection with the bounding boxes for the upper and lower sections of the
            neighboring legs.
        """
        # TODO: write me
        return False
