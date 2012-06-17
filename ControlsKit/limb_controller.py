from leg_logger import logger
from pid_controller import PIDController

class LimbController:
    def __init__(self, kparray, kiarray, kdarray):
        self.kp = kparray
        self.ki = kiarray
        self.kd = kdarray
        
        if (self.kp.size!=self.ki.size or self.ki.size!=self.kd.size):
            logger.error("LimbController.init: Gain array sizes mismatched!",
                        kparray=self.kp,
                        kiarray=self.ki,
                        kdarray=self.kd)
            raise ValueError("LimbController.init: Gain array sizes mismatched!")
        else:
            self.arraysize=self.kp.size
        
        self.pid_controllers=[PIDController(kp,ki,kd) for kp, ki, kd
                    in zip(self.kp, self.ki, self.kd) ]
                    
    def update(self, desired_pos_array, measured_pos_array):
        if (desired_pos_array.size!=self.arraysize or
            measured_pos_array.size!=self.arraysize):
            logger.error("LimbController.update: position array sizes mismatched!",
                        measured_pos_array=measured_pos_array,
                        desired_pos_array=desired_pos_array)
            raise ValueError("LimbController.update:"+
                    " position array sizes mismatched!")
        for i in len(self.pid_controllers):
            self.pid_controllers[i].update(desired_pos_array[i], 
                                            measured_pos_array[i])
