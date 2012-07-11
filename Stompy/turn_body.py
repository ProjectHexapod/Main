from ControlsKit import time_sources, BodyModel, logger, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from ControlsKit.body_paths import RotateFeetAboutOrigin, BodyPause, TrapezoidalFeetAlign, TrapezoidalFeetLiftLower
from scipy import zeros

controller = BodyController()
model = BodyModel()
path = None

PAUSE = 0
ORIENT = 1
CCLOCKWISE = 2
CLOCKWISE = 3
HALF_TURN = 4
HALF_RAISE = 5
RAISE_FIRST_TRIPOD = 6
RAISE_SECOND_TRIPOD = 7
state = ORIENT

LIFT_TRIPOD_024=[1,-1,1,-1,1,-1]
LIFT_TRIPOD_135=[-i for i in LIFT_TRIPOD_024]
delta_angle = .3
lift_height = .4

class RotateComposite:
    def __init__(self,delta_angle):
        self.evens = RotateFeetAboutOrigin(model, controller, [0,2,4], delta_angle, 2, 1)
        self.odds = RotateFeetAboutOrigin(model, controller, [1,3,5], -delta_angle, 2, 1)    
    def isDone(self):
        return(self.evens.isDone() and self.odds.isDone())
    def update(self):
        even_commands = self.evens.update()
        odd_commands = self.odds.update()
        total_commands = [even_commands[0],odd_commands[1],even_commands[2],odd_commands[3],even_commands[4],odd_commands[5],]
        return(total_commands)
        
class LiftComposite:
    def __init__(self,height):
        self.evens = TrapezoidalFeetLiftLower(model, controller, [0,2,4], height, 2, 1)        
        self.odds = TrapezoidalFeetLiftLower(model, controller, [1,3,5], -height, 2, 1)
    def isDone(self):
        return(self.evens.isDone() and self.odds.isDone())
    def update(self):
        even_commands = self.evens.update()
        odd_commands = self.odds.update()
        total_commands = [even_commands[0],odd_commands[1],even_commands[2],odd_commands[3],even_commands[4],odd_commands[5],]
        return(total_commands)



def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates, command=None):
    global path, state
    
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    target_angle_matrix = zeros((NUM_LEGS, LEG_DOF))
    
    #THIS IS WHERE WE CALL ON THE PATH TO DO MATH AND PRODUCE joint_angle_matrix (6x3 matrix)
    if path is None:
        path = BodyPause(model, controller, .1)
        state = ORIENT
        
    if path.isDone():
        if state == ORIENT:
            path = TrapezoidalFeetAlign(model, controller, [0, -.5,  2], 2, 1)
            state = HALF_RAISE
        elif state == HALF_RAISE:
            path = LiftComposite(-lift_height/2)
            state = HALF_TURN
        elif state == HALF_TURN:
            path = RotateComposite(-delta_angle/2)
            state = RAISE_FIRST_TRIPOD      
        elif state == RAISE_FIRST_TRIPOD:
            path = LiftComposite(lift_height)
            state = CLOCKWISE
        elif state == CLOCKWISE:
            path = RotateComposite(delta_angle)
            state = RAISE_SECOND_TRIPOD
        elif state == RAISE_SECOND_TRIPOD:
            path = LiftComposite(-lift_height)
            state = CCLOCKWISE
        elif state == CCLOCKWISE:
            path = RotateComposite(-delta_angle)
            state = RAISE_FIRST_TRIPOD
        elif state == PAUSE:
            path = BodyPause(model, controller, 10)

        logger.info("State changed.", state=state)
    
    # Evaluate path and joint control
    target_angle_matrix  = path.update()

    # Send commands
    return controller.update(model.getJointAngleMatrix(), target_angle_matrix)
