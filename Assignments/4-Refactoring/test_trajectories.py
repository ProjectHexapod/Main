from comparators import ArraysEqual
from leg_controller import LegController
from math_utils import array
import mox
from time_sources import global_time
from trajectories import PutFootOnGround, TrapezoidalFootMove
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
        self.mockLegController.jointAnglesFromFootPos([.1, 0, 0])
        mox.Replay(self.mockLegController)
        pfog = PutFootOnGround(self.mockLegController, 1)
        self.assertFalse(pfog.isDone())
        pfog.update()
        mox.Verify(self.mockLegController)

    def testUpdateNotOnGround(self):
        self.mockLegController.isFootOnGround().AndReturn(False)
        self.mockLegController.jointAnglesFromFootPos([.1, 0, 0])
        mox.Replay(self.mockLegController)
        pfog = PutFootOnGround(self.mockLegController, 1)
        global_time.updateDelta(.1)
        pfog.update()
        mox.Verify(self.mockLegController)

class TrapezoidalFootMoveTestCase(unittest.TestCase):
    def setUp(self):
        self.mockLegController = mox.MockAnything()
        self.mockLegController.getFootPos().AndReturn(array([.2, .2, .2]))

    def tearDown(self):
        mox.Verify(self.mockLegController)

    def testIsDone(self):
        mox.Replay(self.mockLegController)
        trap = TrapezoidalFootMove(self.mockLegController, array([.2, .2, 0]), 10, .1)
        self.assertFalse(trap.isDone())
        trap.done = True
        self.assertTrue(trap.isDone())

    def testUpdateBecommingDone(self):
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, 0]))
        mox.Replay(self.mockLegController)
        trap = TrapezoidalFootMove(self.mockLegController, array([.2, .2, 0]), 10, 1)
        self.assertFalse(trap.isDone())
        trap.target_foot_pos = array([.2, .2, -.1])
        trap.update()
        self.assertTrue(trap.isDone())


