from ControlsKit import time_sources, leg_model, leg_paths, leg_logger
from ControlsKit.leg_paths import TrapezoidalFootMove, PutFootOnGround
from ControlsKit.math_utils import NUM_LEGS, array
from scipy import zeros, append

class GoToStandardHexagon:
    """This path aligns all the feet to a given set of angles via a trapezoidal velocity profile
    """
        
    def __init__(self, body_model, body_controller, max_velocity, acceleration):
        leg_logger.logger.info("New path.", path_name="GoToStandardHexagon",
                    max_velocity=max_velocity, acceleration=acceleration)
        
        self.model = body_model
        self.controller = body_controller
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        
        self.final_joint_positions = self.controller.getTargetJointAngleMatrix()
        self.foot_paths = [None for i in range(NUM_LEGS)]
        
        self.lifted = array([1.651, 0, 0])
        self.lowered = array([1.651,0,-1.6764])
        
        self.NONE = 0
        self.LOWER_ALL = 1
        self.EVENS = 2
        self.LOWER_EVENS = 3
        self.ODDS = 4
        self.LOWER_ODDS = 5
        self.STAND = 6
        
        self.state = self.LOWER_ALL
        
        self.on_ground = [leg.isFootOnGround() for leg in self.model.getLegs()]
        
        # Put all 6 legs in place
        for i in range(NUM_LEGS):
            if self.on_ground[i] == False:
                self.foot_paths[i]=TrapezoidalFootMove(
                    self.model.getLegs()[i],
                    self.controller.getLimbControllers()[i],
                    self.lifted,
                    self.max_velocity, self.acceleration)
        
        if not any(self.on_ground):
            self.state = self.STAND
        
        self.phase_done = False
        self.done = False        
    
    def isDone(self):
        return self.done    
    
    def update(self):
        active_paths = []
        active_index = []
        for i in range(NUM_LEGS):
            if self.foot_paths[i] != None:
                active_index.append(i)
                active_paths.append(self.foot_paths[i])

        if self.phase_done:
            if self.state == self.LOWER_ALL:
                for i in range(NUM_LEGS):
                    if self.on_ground[i] == False:
                        self.foot_paths[i]=PutFootOnGround(
                            self.model.getLegs()[i],
                            self.controller.getLimbControllers()[i],
                            self.max_velocity, self.acceleration)
                self.state = self.EVENS
                self.phase_done = False
            elif self.state == self.EVENS:
                for i in range(NUM_LEGS):
                    if not i%2:
                        self.foot_paths[i]=TrapezoidalFootMove(
                            self.model.getLegs()[i],
                            self.controller.getLimbControllers()[i],
                            self.lifted,
                            self.max_velocity, self.acceleration)
                self.state = self.LOWER_EVENS
                self.phase_done = False
            elif self.state == self.LOWER_EVENS:
                for i in range(NUM_LEGS):
                    if self.on_ground[i] == False:
                        self.foot_paths[i]=PutFootOnGround(
                            self.model.getLegs()[i],
                            self.controller.getLimbControllers()[i],
                            self.max_velocity, self.acceleration)
                self.state = self.ODDS
                self.phase_done = False
            elif self.state == self.ODDS:
                for i in range(NUM_LEGS):
                    if i%2:
                        self.foot_paths[i]=TrapezoidalFootMove(
                            self.model.getLegs()[i],
                            self.controller.getLimbControllers()[i],
                            self.lifted,
                            self.max_velocity, self.acceleration)
                self.state = self.LOWER_ODDS
                self.phase_done = False
            elif self.state == self.LOWER_ODDS:
                for i in range(NUM_LEGS):
                    if self.on_ground[i] == False:
                        self.foot_paths[i]=PutFootOnGround(
                            self.model.getLegs()[i],
                            self.controller.getLimbControllers()[i],
                            self.max_velocity, self.acceleration)
                self.state = self.STAND
                self.phase_done = False
            elif self.state == self.STAND:
                for i in range(NUM_LEGS):
                    self.foot_paths[i]=TrapezoidalFootMove(
                        self.model.getLegs()[i],
                        self.controller.getLimbControllers()[i],
                        self.lowered,
                        self.max_velocity, self.acceleration*.1)
                self.state = self.NONE
                self.phase_done = False
            elif self.state == self.NONE:
                self.done = True
                return self.final_joint_positions
        elif not self.phase_done:
            #logically and all of the isdone results from the joint move paths
            self.phase_done = all(map(lambda p: p.isDone(), active_paths))
            
        if not self.done:
            for i in active_index:
                self.final_joint_positions[i] = self.foot_paths[i].update()
            return self.final_joint_positions
