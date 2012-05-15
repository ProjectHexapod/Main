from behaviors import PutFootOnGround
from behaviors import TrapezoidalFootMove
from leg_controller import LegController
import math_utils
import mox
from time_sources import global_time
import unittest

class PutFootOnGroundTestCase(unittest.TestCase):
    def setUp(self):
        self.mockLegController = mox.MockAnything()
        self.mockLegController.isFootOnGround().AndReturn(False)
        self.mockLegController.getFootPos().AndReturn([.1, 0., 0.])

    def testIsDone(self):
        mox.Replay(self.mockLegController)
        pfog = PutFootOnGround(self.mockLegController, 1)
        self.assertFalse(pfog.isDone())
        pfog.done = True
        mox.Verify(self.mockLegController)

    def testUpdateOnGround(self):
        self.mockLegController.isFootOnGround().AndReturn(True)
        self.mockLegController.jointAnglesFromFootPos([.1, 0, -.1])
        mox.Replay(self.mockLegController)
        pfog = PutFootOnGround(self.mockLegController, 1)
        self.assertFalse(pfog.isDone())
        pfog.update()
        mox.Verify(self.mockLegController)

    def testUpdateNotOnGround(self):
        self.mockLegController.isFootOnGround().AndReturn(False)
        self.mockLegController.jointAnglesFromFootPos([.1, 0, -.1])
        mox.Replay(self.mockLegController)
        pfog = PutFootOnGround(self.mockLegController, 1)
        global_time.updateDelta(.1)
        pfog.update()
        mox.Verify(self.mockLegController)

class TrapezoidalFootMoveTestCase(unittest.TestCase):
    def setUp(self):
        self.mockLegController = mox.MockAnything()
