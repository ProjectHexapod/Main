from ControlsKit.math_utils import array, NUM_LEGS
from ControlsKit.leg_paths import FootVelocity
from ControlsKit.time_sources import global_time


def tryGetElement(sequence, index, default):
    try:
        return sequence[index]
    except:
        return default

        
class FeetVelocities:
            
    def __init__(self, body_model,
                 max_acceleration=None,
                 initial_velocities=None,
                 initial_positions=None,
                 time_source=global_time):
        # don't put a mutable as a default arg
        if None is max_acceleration:
            max_acceleration = array([20.0, 20.0, 20.0])
        
        self.model = body_model
        self.paths = []
        for i in range(NUM_LEGS):
            self.paths.append(
                FootVelocity(self.model.getLegs()[i],
                             max_acceleration=max_acceleration,
                             initial_velocity=tryGetElement(initial_velocities, i, None),
                             initial_position=tryGetElement(initial_positions, i, None),
                             time_source=tryGetElement(time_source, i, time_source)))
    
    def setMaxAcceleration(self, max_acceleration):
        for p in self.paths:
            p.setMaxAcceleration(max_acceleration)
            
    def setVelocity(self, leg_index, target_velocity):
        self.paths[leg_index].setVelocity(self.model.rotateBody2Leg(leg_index,
                                                                    target_velocity))
        
    def setVelocities(self, target_velocities):
        for i in range(NUM_LEGS):
            self.setVelocity(i, target_velocities[i])
    
    def isDone(self):
        return all(map(lambda p: p.isDone(), self.paths))
        
    def update(self):
        return map(lambda p: p.update(), self.paths)
