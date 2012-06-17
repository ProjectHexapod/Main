from leg_logger import logger
from pid_controller import PIDController

class LimbController:
    def __init__(self, kparray=[0,0,0], kiarray=[0,0,0], kdarray=[0,0,0]):
        self.length_rate_commands=[]
        
        self.pid_controllers=[PIDController() for i in range(len(kparray)) ]
        self.updateGainConstants(kparray,kiarray,kdarray)
        self.amount_of_joints=len(self.kp)
                    
    def updateGainConstants(self, kparray, kiarray, kdarray):
        self.kp = kparray
        self.ki = kiarray
        self.kd = kdarray
        
        if (len(self.kp)!=len(self.ki) or len(self.ki)!=len(self.kd) ):
            logger.error("LimbController.init: Gain array sizes mismatched!",
                        kparray=self.kp,
                        kiarray=self.ki,
                        kdarray=self.kd)
            raise ValueError("LimbController.init: Gain array sizes mismatched!")
        
        for controller, kp, ki, kd in zip(self.pid_controllers, self.kp, self.ki, self.kd):
            controller.updateGainConstants(kp, ki, kd)
    
    def update(self, desired_pos_array, measured_pos_array):
        actuator_commands=[]
        if (len(desired_pos_array)!=self.amount_of_joints or
            len(measured_pos_array)!=self.amount_of_joints):
            logger.error("LimbController.update: position array sizes mismatched!",
                        measured_pos_array=measured_pos_array,
                        desired_pos_array=desired_pos_array)
            raise ValueError("LimbController.update:"+
                    " position array sizes mismatched!")
        for i in range(len(self.pid_controllers)):
            actuator_command=self.pid_controllers[i].update(
                desired_pos_array[i], measured_pos_array[i])
            actuator_commands.append(actuator_command)
        self.length_rate_commands=actuator_commands
    
    def getLengthRateCommands(self):            
        return self.length_rate_commands
