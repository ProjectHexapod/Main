from UI import logger
from pid_controller import PIDController
import ConfigParser
from os import path
from scipy import array
from math import *
from time_sources import global_time

class LimbController:
    def __init__(self, config_file="leg_model.conf", section="LimbController"):
        c = ConfigParser.ConfigParser()
        if not path.exists(path.abspath(config_file)):
            print 'Config file %s not found!'%config_file
            raise IOError
        c.read(config_file)
        
        def readFloatWithDefault( c, sec, name, val=0.0 ):
            try:
                return c.getfloat(sec,name)
            except ConfigParser.Error, mesg:
                print mesg
                print "Using default value %f for %s:%s"%(val,sec,name)
                return val
        # Default PID values
        self.kparray = array(
                [readFloatWithDefault(c, section,'yaw_p'),
                 readFloatWithDefault(c, section,'hp_p'),
                 readFloatWithDefault(c, section,'kp_p')])
        self.kiarray = array(
                [readFloatWithDefault(c, section,'yaw_i'),
                 readFloatWithDefault(c, section,'hp_i'),
                 readFloatWithDefault(c, section,'kp_i')])
        self.kdarray = array(
                [readFloatWithDefault(c, section,'yaw_d'),
                 readFloatWithDefault(c, section,'hp_d'),
                 readFloatWithDefault(c, section,'kp_d')])
        self.kffarray = array(
                [readFloatWithDefault(c, section,'yaw_ff'),
                 readFloatWithDefault(c, section,'hp_ff'),
                 readFloatWithDefault(c, section,'kp_ff')])
        self.kfaarray = array(
                [readFloatWithDefault(c, section,'yaw_fa'),
                 readFloatWithDefault(c, section,'hp_fa'),
                 readFloatWithDefault(c, section,'kp_fa')])
        self.dearray = array(
                [readFloatWithDefault(c, section,'yaw_de'),
                 readFloatWithDefault(c, section,'hp_de'),
                 readFloatWithDefault(c, section,'kp_de')])
        self.drarray = array(
                [readFloatWithDefault(c, section,'yaw_dr'),
                 readFloatWithDefault(c, section,'hp_dr'),
                 readFloatWithDefault(c, section,'kp_dr')])
        self.proparray = array(
                [readFloatWithDefault(c, section,'yaw_prop'),
                 readFloatWithDefault(c, section,'hp_prop'),
                 readFloatWithDefault(c, section,'kp_prop')])
        
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

            # JWHONG COMPENSATION FOR EXTEND VS RETRACT SURFACE AREA HACK
            # JWHONG DEADBAND HACK
            if actuator_command > 0:
                actuator_command += self.dearray[i]
            elif actuator_command < 0:
                actuator_command *= self.proparray[i]
                actuator_command -= self.drarray[i]
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
