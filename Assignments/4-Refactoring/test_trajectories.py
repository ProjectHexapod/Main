from comparators import ArraysEqual
from leg_controller import LegController
from math_utils import array
import mox
from time_sources import global_time, resetTimeSourceForTestingPurposes
from trajectories import PutFootOnGround, TrapezoidalFootMove
import unittest


class PutFootOnGroundTestCase(unittest.TestCase):
    def setUp(self):
        resetTimeSourceForTestingPurposes(global_time)
        
        self.mock_leg_controller = mox.MockAnything()
        self.mock_leg_controller.isFootOnGround().AndReturn(False)
        self.mock_leg_controller.getFootPos().AndReturn([.1, 0., 0.])

    def testIsDone(self):
        mox.Replay(self.mock_leg_controller)
        pfog = PutFootOnGround(self.mock_leg_controller, 1)
        self.assertFalse(pfog.isDone())
        pfog.done = True
        mox.Verify(self.mock_leg_controller)

    def testUpdateOnGround(self):
        self.mock_leg_controller.isFootOnGround().AndReturn(True)
        self.mock_leg_controller.jointAnglesFromFootPos([.1, 0, 0])
        mox.Replay(self.mock_leg_controller)
        pfog = PutFootOnGround(self.mock_leg_controller, 1)
        self.assertFalse(pfog.isDone())
        pfog.update()
        mox.Verify(self.mock_leg_controller)

    def testUpdateNotOnGround(self):
        self.mock_leg_controller.isFootOnGround().AndReturn(False)
        self.mock_leg_controller.jointAnglesFromFootPos([.1, 0, 0])
        mox.Replay(self.mock_leg_controller)
        pfog = PutFootOnGround(self.mock_leg_controller, 1)
        global_time.updateDelta(.1)
        pfog.update()
        mox.Verify(self.mock_leg_controller)


class TrapezoidalFootMoveTestCase(unittest.TestCase):
    def setUp(self):
        resetTimeSourceForTestingPurposes(global_time)
        
        self.mock_leg_controller = mox.MockAnything()
        self.mock_leg_controller.getFootPos().AndReturn(array([.2, .2, .2]))

    def tearDown(self):
        mox.Verify(self.mock_leg_controller)

    def testIsDone(self):
        mox.Replay(self.mock_leg_controller)
        trap = TrapezoidalFootMove(self.mock_leg_controller,
                                   array([.2, .2, 0]), 10, .1)
        self.assertFalse(trap.isDone())
        trap.done = True
        self.assertTrue(trap.isDone())

    def testUpdateBecommingDone(self):
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, 0]))
        mox.Replay(self.mock_leg_controller)
        trap = TrapezoidalFootMove(self.mock_leg_controller,
                                   array([.2, .2, 0]), 10, 1)
        self.assertFalse(trap.isDone())
        trap.target_foot_pos = array([.2, .2, -.1])
        global_time.updateDelta(.1)
        trap.update()
        self.assertTrue(trap.isDone())

    def testLeadingEdge(self):
        # .19 here is .2 minus the time delta times the speed
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .19]))
        mox.Replay(self.mock_leg_controller)
        trap = TrapezoidalFootMove(self.mock_leg_controller,
                                   array([.2, .2, 0]), 10, 1)
        global_time.updateDelta(.1)
        trap.update()
        # the lack of visible asserts here is because the verification of the
        # mock object happens in tearDown

    def testLeadingEdgeStrait(self):
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .19]))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .17]))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .14]))
        mox.Replay(self.mock_leg_controller)
        trap = TrapezoidalFootMove(self.mock_leg_controller,
                                   array([.2, .2, 0]), 10, 1)
        global_time.updateDelta(.1)
        trap.update()
        global_time.updateDelta(.1)
        trap.update()
        global_time.updateDelta(.1)
        trap.update()

    def testPlateau(self):
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .19]))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .18]))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .17]))
        mox.Replay(self.mock_leg_controller)
        trap = TrapezoidalFootMove(self.mock_leg_controller,
                                   array([.2, .2, 0]), .1, 1)
        global_time.updateDelta(.1)
        trap.update()
        global_time.updateDelta(.1)
        trap.update()
        global_time.updateDelta(.1)
        trap.update()

    def testTriangleCase(self):
        # Speed goes up from 1 to 2
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .19]))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .17]))
        # and then back down to 1
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .16]))
        mox.Replay(self.mock_leg_controller)
        # never hitting the max speed of 10
        trap = TrapezoidalFootMove(self.mock_leg_controller,
                                   array([.2, .2, .15]), 10, 1)
        global_time.updateDelta(.1)
        trap.update()
        global_time.updateDelta(.1)
        trap.update()
        global_time.updateDelta(.1)
        trap.update()
    
    def testDoesntPassTargetFootPos(self):
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .1]))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual([.2, .2, .0]))
        mox.Replay(self.mock_leg_controller)
        
        trap = TrapezoidalFootMove(self.mock_leg_controller,
                                   array([.2, .2, 0.0]), 10.0, 10.0)
        
        global_time.updateDelta(0.1)
        trap.update()
        global_time.updateDelta(0.1)
        trap.update()


if __name__ == '__main__':
    unittest.main()
