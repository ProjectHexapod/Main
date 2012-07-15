from ConfigParser import ConfigParser
from leg_model import LegModel
from UI import logger
from math_utils import NUM_LEGS, rotateZ
from scipy import array, pi
import os.path as path

class BodyModel:
    def __init__(self, config_file="body_model.conf", section="BodyModel"):
        c = ConfigParser()
        if not path.exists(config_file):
            print 'Config file %s not found!'%config_file
            raise IOError 
        c.read(config_file)
        self.legs = [LegModel() for i in range(NUM_LEGS)]
        
        # Leg Offsets
        self.LEG0_OFFSET_X = c.getfloat(section, "leg0_offset_x")
        self.LEG0_OFFSET_Y = c.getfloat(section, "leg0_offset_y")
        self.LEG0_THETA = c.getfloat(section, "leg0_theta")
        self.LEG1_OFFSET_X = c.getfloat(section, "leg1_offset_x")
        self.LEG1_OFFSET_Y = c.getfloat(section, "leg1_offset_y")
        self.CHASSIS_BOTTOM_Z = c.getfloat(section, "chassis_bottom_z")

    def setSensorReadings(self, leg_sensor_matrix, imu_orientation, imu_angular_rates):
        for i in range(NUM_LEGS):
            self.legs[i].setSensorReadings(*leg_sensor_matrix[i])
            self.legs[i].updateFootOnGround()
        self.imu_orientation = imu_orientation
        self.imu_angular_rates = imu_angular_rates

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
    
    def transformLeg2Body(self, leg_index, leg_coord):
        """ Takes in CARTESIAN coordinates in leg space and returns a CARTESIAN
            array of xyz in the body frame
        """
        hip_offset = self.getHipOffset(leg_index)
        rotated = rotateZ(leg_coord, hip_offset[2])
        body_coord = rotated+array([hip_offset[0], hip_offset[1], 0])
        return body_coord
        
    def rotateBody2Leg(self, leg_index, body_coord):
        """ Takes in CARTESIAN coordinates in body space and returns a CARTESIAN
            array of xyz that has been rotated such that is is aligned with that
            leg's coordinate frame
        """
        hip_offset = self.getHipOffset(leg_index)
        leg_aligned_coord = rotateZ(body_coord, -hip_offset[2])
        return leg_aligned_coord
    def transformBody2Leg(self, leg_index, body_coord):
        """ Takes in CARTESIAN coordinates in body space and returns a CARTESIAN
            array of xyz in that leg's coordinate frame
        """
        hip_offset = self.getHipOffset(leg_index)
        translated = array(body_coord)-array([hip_offset[0], hip_offset[1], 0])
        leg_coord = self.rotateBody2Leg(leg_index, translated)
        return leg_coord
    
    def getHipOffset(self,leg_index):
        """ Takes an index, returns a three-vector of X,Y and Theta offsets
        """
        if leg_index == 0:
            hip_offset = array([self.LEG0_OFFSET_X, self.LEG0_OFFSET_Y, self.LEG0_THETA])
        elif leg_index == 1:
            hip_offset = array([self.LEG1_OFFSET_X, self.LEG1_OFFSET_Y, pi/2])
        elif leg_index == 2:
            hip_offset = array([-self.LEG0_OFFSET_X, self.LEG0_OFFSET_Y, pi-self.LEG0_THETA])
        elif leg_index == 3:
            hip_offset = array([-self.LEG0_OFFSET_X, -self.LEG0_OFFSET_Y, -pi+self.LEG0_THETA])
        elif leg_index == 4:
            hip_offset = array([-self.LEG1_OFFSET_X, -self.LEG1_OFFSET_Y, -pi/2])
        elif leg_index == 5:
            hip_offset = array([self.LEG0_OFFSET_X, -self.LEG0_OFFSET_Y, -self.LEG0_THETA])
        else:
            raise ValueError ("BodyModel.getHipOffset: Leg index out of bounds.")
        return hip_offset
            
