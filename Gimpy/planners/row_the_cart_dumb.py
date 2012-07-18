from ControlsKit import time_sources, LegModel, LimbController
from ControlsKit.leg_paths import Pause, TrapezoidalFootMove, PutFootOnGround
from ControlsKit.math_utils import array, Z
from UI import logger

# Initialization
model = LegModel()
controller = LimbController()
path = None

S_MOVE0 = 0
S_MOVE1 = 1
S_MOVE2 = 2
S_MOVE3 = 3
PAUSE   = 4

state = S_MOVE3

points = []
points.append( (1.5, -0.3, -0.85) )
points.append( (1.5,  0.3, -0.85) )
#points.append( (1.5,  0.6,  0.00) )
#points.append( (2.1,  0.0,  0.00) )
#points.append( (1.5, -0.6,  0.00) )
#points.append( (2.1,  -0.0, -0.40) )
#points.append( (1.1,  -0.0, -0.40) )
index = 0

# Body of control loop
def update(time, yaw, hip_pitch, knee_pitch, shock_depth, command=None):
    global points, path, index
    
    
    # Update model
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(yaw, hip_pitch, knee_pitch, shock_depth)
    model.updateFootOnGround()

    # Init path. Do this after the first update.
    if path is None:
        path = Pause(model, controller, 1.0)
    
    if path.isDone():
        path = TrapezoidalFootMove(model, controller,
                                       array(points[index]),
                                       0.5, 0.4)
        index = (index+1)%len(points)
        logger.info("State changed.", state=state)

    # Evaluate path and joint control
    controller.update(model.getJointAngles(), path.update())

    # Send commands
    return controller.getLengthRateCommands()
