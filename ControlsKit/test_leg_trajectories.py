from comparators import ArraysEqual, ReturnTrue
from leg_controller import LegController
from math_utils import array 
import mox
from time_sources import global_time, resetTimeSourceForTestingPurposes
from leg_trajectories import PutFootOnGround, TrapezoidalFootMove, InterpolatedFootMove
import unittest

class InterpolatedFootMoveTestCase(unittest.TestCase):
    def setUp(self):
        resetTimeSourceForTestingPurposes(global_time)
        self.mock_leg_controller = mox.MockAnything()
        
        
    def testIsDone(self):
        print "testing isDone"
        self.path = array([[0,1,1,1],[1,2,2,2],[2,9,9,9],[3,28,28,28]])
        self.path = self.path.transpose()
        self.mock_leg_controller.getFootPos().AndReturn([0,0,0])
        self.mock_leg_controller.jointAnglesFromFootPos(ReturnTrue(self.path))
        mox.Replay(self.mock_leg_controller)
        ifm = InterpolatedFootMove(self.mock_leg_controller, self.path)
        ifm.update()
        self.assertFalse(ifm.isDone())
        global_time.updateDelta(4)
        ifm.update()
        self.assertTrue(ifm.isDone())
        mox.Verify(self.mock_leg_controller)
        
    def testCubic(self):
        print "testing cubic interpolation"
        self.path = array([[0,1,1,1],[1,2,2,2],[2,9,9,9],[3,28,28,28]])
        self.path = self.path.transpose()
        self.mock_leg_controller.getFootPos().AndReturn([0,0,0])
        #target_foot_pos = array([0.,0.,0.])
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual(array([.0,.0,.0])))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual(array([.001,.001,.001])))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual(array([.008,.008,.008])))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual(array([.027,.027,.027])))
        self.mock_leg_controller.jointAnglesFromFootPos(ArraysEqual(array([.064,.064,.064])))
        mox.Replay(self.mock_leg_controller)
        ifm = InterpolatedFootMove(self.mock_leg_controller, self.path)
        print "TEST 1"
        #target_foot_pos = array([ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3])
        print "expected target_foot_pos = ", array([.0,.0,.0])
        self.assertFalse(ifm.isDone())
        ifm.update()
        global_time.updateDelta(0.1)
        print "TEST 2"
        #target_foot_pos = array([ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3])
        print "expected target_foot_pos = ", array([.001,.001,.001])
        ifm.update()
        global_time.updateDelta(0.1)
        print "TEST 3"
        #target_foot_pos = array([ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3])
        print "expected target_foot_pos = ", array([.008,.008,.008])
        ifm.update()
        global_time.updateDelta(0.1)
        print "TEST 4"
        #target_foot_pos = array([ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3])
        print "expected target_foot_pos = ", array([.027,.027,.027])
        ifm.update()
        global_time.updateDelta(0.1)
        print "TEST 5"
        #target_foot_pos = array([ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3,ifm.stop_watch.getTime()**3])
        print "expected target_foot_pos = ", array([.064,.064,.064])
        ifm.update()
        mox.Verify(self.mock_leg_controller)
        

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
