class PutFootOnGround:
    def __init__(self, legController, velocity):
        self.leg = legController
        self.velocity = velocity

    def isDone(self):
        return False

    def update(self, time):
        return self.leg.getJointAngles()


class TrapezoidalFootMove:
    def __init__(self, leg_controller, target_foot_pos, velocity, acceleration):
        self.leg = leg_controller
        self.targetFootPos = target_foot_pos
        self.velocity = velocity
        self.acceleration = aceleration

    def isDone(self):
        return False

    def update(self, time):
        return self.leg.getJointAngles()
