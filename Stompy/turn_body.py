from ControlsKit import time_sources, BodyModel, BodyController
from ControlsKit.math_utils import NUM_LEGS, LEG_DOF
from ControlsKit.body_paths import RotateFeetAboutOrigin, BodyPause, TrapezoidalFeetAlign, TrapezoidalFeetLiftLower
from UI import logger
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
RAISE_EVEN_TRIPOD = 6
RAISE_ODD_TRIPOD = 7
state = ORIENT

delta_angle = .5 # Choose a number less than 0.9 radians
lift_height = .2 # Choose a number greater than .15 meters

class RotateComposite:
    def __init__(self, delta_angle):
        self.delta_angle = delta_angle
        self.evens = RotateFeetAboutOrigin(model, controller, [0,2,4], delta_angle, 2, 5)
        self.odds = RotateFeetAboutOrigin(model, controller, [1,3,5], -delta_angle, 2, 5)    
    def isDone(self):
        return(self.evens.isDone() and self.odds.isDone())
    def update(self):
        even_commands = self.evens.update()
        odd_commands = self.odds.update()
        total_commands = [even_commands[0],odd_commands[1],even_commands[2],odd_commands[3],even_commands[4],odd_commands[5],]
        return(total_commands)
        
class LiftComposite:
    def __init__(self, height):
        self.height = height
        self.evens = TrapezoidalFeetLiftLower(model, controller, [0,2,4], height, 2, 5)        
        self.odds = TrapezoidalFeetLiftLower(model, controller, [1,3,5], -height, 2, 5)
    def isDone(self):
        return(self.evens.isDone() and self.odds.isDone())
    def update(self):
        if (self.height < 0 and self.evens.isDone()) or (self.height > 0 and not self.odds.isDone()):
            return(self.odds.update())
        else:
            return(self.evens.update())


def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates, command=None):
    global path, state
    
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    target_angle_matrix = zeros((NUM_LEGS, LEG_DOF))
    
    if path is None:
        path = BodyPause(model, controller, .1)
        state = ORIENT
        
    if path.isDone():
        if state == ORIENT: # Put the feet in some reasonable location that they might have started from
            path = TrapezoidalFeetAlign(model, controller, [0, -.5,  2], 2, 1)
            state = HALF_RAISE
        elif state == HALF_RAISE: # Raise one tripod half the total travel
            path = LiftComposite(-lift_height/2)
            state = HALF_TURN
        elif state == HALF_TURN: # Rotate half the total rotation
            path = RotateComposite(-delta_angle/2)
            state = RAISE_EVEN_TRIPOD      
        elif state == RAISE_EVEN_TRIPOD: # Raise a tripod
            path = LiftComposite(lift_height)
            state = CLOCKWISE
        elif state == CLOCKWISE: # Rotate one direction
            path = RotateComposite(delta_angle)
            state = RAISE_ODD_TRIPOD
        elif state == RAISE_ODD_TRIPOD: # Raise the other tripod
            path = LiftComposite(-lift_height)
            state = CCLOCKWISE
        elif state == CCLOCKWISE: # Rotate the other direction
            path = RotateComposite(-delta_angle)
            state = RAISE_EVEN_TRIPOD
        elif state == PAUSE: # Set state to PAUSE if you need to debug something
            path = BodyPause(model, controller, 10)

        logger.info("State changed.", state=state)
    
    # Evaluate path and joint control
    target_angle_matrix  = path.update()

    # Send commands
    return controller.update(model.getJointAngleMatrix(), target_angle_matrix)
