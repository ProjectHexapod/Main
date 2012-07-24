from UI import logger
from pid_controller import PIDController
from ConfigParser import ConfigParser
from os import path
from scipy import array
from math import *
from time_sources import global_time

class LimbController:
    def __init__(self, config_file="leg_model.conf", section="LimbController"):
        c = ConfigParser()
        if not path.exists(path.abspath(config_file)):
            print 'Config file %s not found!'%config_file
            raise IOError
        c.read(config_file)
        
        # Default PID values
        self.kparray = array(
                [c.getfloat(section,'yaw_p'),
                c.getfloat(section,'hp_p'),
                c.getfloat(section,'kp_p')])
        self.kiarray = array(
                [c.getfloat(section,'yaw_i'),
                c.getfloat(section,'hp_i'),
                c.getfloat(section,'kp_i')])
        self.kdarray = array(
                [c.getfloat(section,'yaw_d'),
                c.getfloat(section,'hp_d'),
                c.getfloat(section,'kp_d')])
        self.kffarray = array(
                [c.getfloat(section,'yaw_ff'),
                c.getfloat(section,'hp_ff'),
                c.getfloat(section,'kp_ff')])
        self.kfaarray = array(
                [c.getfloat(section,'yaw_fa'),
                c.getfloat(section,'hp_fa'),
                c.getfloat(section,'kp_fa')])
        
        self.length_rate_commands=[]
        
        self.pid_controllers=[PIDController() for i in range(len(self.kparray)) ]
        self.updateGainConstants(self.kparray,self.kiarray,self.kdarray,self.kffarray, self.kfaarray)
        self.amount_of_joints=len(self.kp)
        self.desired_vel_array = array([0,0,0])
                    
    def updateGainConstants(self, kparray, kiarray, kdarray, kffarray, kfaarray):
        self.kp = kparray
        self.ki = kiarray
        self.kd = kdarray
        self.kff= kffarray
        self.kfa= kfaarray
        
        if (len(self.kp)!=len(self.ki) or len(self.ki)!=len(self.kd) ):
            logger.error("LimbController.init: Gain array sizes mismatched!",
                        kparray=self.kp,
                        kiarray=self.ki,
                        kdarray=self.kd)
            raise ValueError("LimbController.init: Gain array sizes mismatched!")
        
        for controller, kp, ki, kd, kff, kfa in zip(self.pid_controllers, self.kp, self.ki, self.kd, self.kff, self.kfa):
            controller.updateGainConstants(kp, ki, kd, kff, kfa)
    
    def update(self, measured_pos_array, desired_pos_array):
        if hasattr(self, 'desired_pos_array'):
            # update target velocities
            for i in range(3):
                self.desired_vel_array[i] = (desired_pos_array[i]-self.desired_pos_array[i])/global_time.getDelta()
        else:
            self.desired_vel_array = array([0,0,0])
        self.desired_pos_array = desired_pos_array
        actuator_commands=[]
        if (len(self.desired_pos_array)!=self.amount_of_joints or
            len(measured_pos_array)!=self.amount_of_joints):
            logger.error("LimbController.update: position array sizes mismatched!",
                        measured_pos_array=measured_pos_array,
                        desired_pos_array=self.desired_pos_array)
            raise ValueError("LimbController.update:"+
                    " position array sizes mismatched!")
        for i in range(len(self.pid_controllers)):
            actuator_command=self.pid_controllers[i].update(
                self.desired_pos_array[i], measured_pos_array[i])
            actuator_commands.append(actuator_command)
        self.length_rate_commands=actuator_commands
    
    def getLengthRateCommands(self):            
        return self.length_rate_commands
    
    def getDesiredPosAngle(self):
        try:
            return self.desired_pos_array
        except AttributeError:
            return None
    def getDesiredYaw(self):
        return self.desired_pos_array[0]
    def getDesiredPitch(self):
        return self.desired_pos_array[1]
    def getDesiredKnee(self):
        return self.desired_pos_array[2]
    def getDesiredYawDeg(self):
        return 180*self.desired_pos_array[0]/pi
    def getDesiredPitchDeg(self):
        return 180*self.desired_pos_array[1]/pi
    def getDesiredKneeDeg(self):
        return 180*self.desired_pos_array[2]/pi
