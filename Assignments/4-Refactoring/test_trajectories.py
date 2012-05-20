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
        global_time.updateDelta(.1)
        trap.update()
        self.assertTrue(trap.isDone())

    def testLeadingEdge(self):
        # .19 here is .2 minus the time delta times the speed
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .19]))
        mox.Replay(self.mockLegController)
        trap = TrapezoidalFootMove(self.mockLegController, array([.2, .2, 0]), 10, 1)
        global_time.updateDelta(.1)
        trap.update()
        # the lack of visible asserts here is because the verification of the mock object happens in tearDown

    def testLeadingEdgeStrait(self):
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .19]))
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .17]))
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .14]))
        mox.Replay(self.mockLegController)
        trap = TrapezoidalFootMove(self.mockLegController, array([.2, .2, 0]), 10, 1)
        trap.update()
        trap.update()
        trap.update()

    def testPlateau(self):
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .19]))
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .18]))
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .17]))
        mox.Replay(self.mockLegController)
        trap = TrapezoidalFootMove(self.mockLegController, array([.2, .2, 0]), .1, 1)
        trap.update()
        trap.update()
        trap.update()

    def testTriangleCase(self):
        # Speed goes up from 1 to 2
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .19]))
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .17]))
        # and then back down to 1
        self.mockLegController.jointAnglesFromFootPos(ArraysEqual([.2, .2, .16]))
        mox.Replay(self.mockLegController)
        # never hitting the max speed of 10
        trap = TrapezoidalFootMove(self.mockLegController, array([.2, .2, .15]), 10, 1)
        trap.update()
        trap.update()
        trap.update()
        






