from ConfigParser import ConfigParser
from leg_model import LegModel
from leg_logger import logger
from math_utils import NUM_LEGS  # abuah? why is the leg count a math util?
import os.path as path

class BodyModel:
    def __init__(self, config_file="../ControlsKit/body_model.conf", section="BodyModel"):
        c = ConfigParser()
        if not path.exists(config_file):
            print 'Config file %s not found!'%config_file
            raise IOError 
        c.read(config_file)
        # FIXME: This references the wrong config file.
        # It's commented out right now to get it working,
        # I am not sure what the author's intent here was.
        # JHW Wed 06 Jun 2012 04:24:57 PM EDT
        #self.legs = [LegController(config_file, "GenericLeg") for i in range(NUM_LEGS)]
        self.legs = [LegModel() for i in range(NUM_LEGS)]

    def setSensorReadings(self, leg_sensor_matrix, imu_orientation, imu_angular_rates):
        for i in range(NUM_LEGS):
            self.legs[i].setSensorReadings(*leg_sensor_matrix[i])
            self.legs[i].updateFootOnGround()
        self.imu_orientation = imu_orientation
        self.imu_angular_rates = imu_angular_rates
    
##MOVE TO PATH
    #def setDesiredJointAngles(self, joint_angle_matrix):
    #    for i in range(NUM_LEGS):
    #        self.legs[i].setDesiredJointAngles(joint_angle_matrix[i])
    #        if not self.legsAreColliding():
    #            self.legs[i].updateLengthRateCommands()
    #    
    #def getLengthRateCommands(self):
    #    return map(LegModel.getLengthRateCommands, self.legs)

    def getLegs(self):
        return self.legs

    def getJointAngleMatrix(self):
        return [self.legs[i].getJointAngles() for i in range(NUM_LEGS)]
    
    def getFootPositions(self):
        return [self.legs[i].getFootPos() for i in range(NUM_LEGS)]

    def legsAreColliding(self):
        """ Get bounding boxes for the lower section of each of the six legs, and check them for
            intersection with the bounding boxes for the upper and lower sections of the
            neighboring legs.
        """
        collision = False
        # TODO: write me
        if collision:
            logger.critical("COLLISION")
        return collision
