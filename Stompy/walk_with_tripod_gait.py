from ControlsKit import time_sources, BodyModel, BodyController
from ControlsKit.body_paths import TrapezoidalFeetAlign, TripodGait
from UI import logger

controller = BodyController()
model = BodyModel()
path = None


ORIENT = 1
WALK = 2
DONE = 3
state = ORIENT


def update(time, leg_sensor_matrix, imu_orientation, imu_accelerations, imu_angular_rates, command=None):
    global path, state
    
    time_sources.global_time.updateTime(time)
    model.setSensorReadings(leg_sensor_matrix, imu_orientation, imu_angular_rates)
    
    if path is None or path.isDone():
        if state == ORIENT:
            path = TrapezoidalFeetAlign(model, controller, [0, -.7,  2], 2, 1)
            state = WALK
        elif state == WALK:
            path = TripodGait(model)
            state = DONE
        logger.info("State changed.", state=state)
    
    return controller.update(model.getJointAngleMatrix(), path.update())
