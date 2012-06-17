from leg_logger import logger
from pid_controller import PidController

class LimbController:
    def __init__(self, kparray, kiarray, kdarray):
        self.kp = kparray
        self.ki = kiarray
        self.kd = kdarray
        
        if (len(self.kp)!=len(self.ki) or len(self.ki)!=len(self.kd) ):
            logger.error("LimbController.init: Gain array sizes mismatched!",
                        kparray=self.kp,
                        kiarray=self.ki,
                        kdarray=self.kd)
            raise ValueError("LimbController.init: Gain array sizes mismatched!")
        else:
            self.amount_of_joints=len(self.kp)
        
        self.pid_controllers=[PIDController(kp,ki,kd) for kp, ki, kd
                    in zip(self.kp, self.ki, self.kd) ]
                    
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
        return actuator_commands
