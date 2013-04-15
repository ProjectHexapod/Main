#TODO test integral windup

import joint_control

import mox
import unittest
from comparators import Gt, Lt


class TestJointController(unittest.TestCase):


    def setUp(self):
        self.mockJoint = mox.MockAnything()
        self.control = joint_control.JointController(self.mockJoint)
        self.control.prev_time = 0

    def test_update_joint_noop(self):
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(0)
        mox.Replay(self.mockJoint)
        self.assertEquals(0, self.control.updateJoint(0, .1))
        mox.Verify(self.mockJoint)

    def test_update_joint_small_positive_error(self):
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(Gt(0))
        mox.Replay(self.mockJoint)
        self.assertEquals(.1, self.control.updateJoint(.1, .1))
        mox.Verify(self.mockJoint)

    def test_update_joint_small_negative_error(self):
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(Lt(0))
        mox.Replay(self.mockJoint)
        
        #this kludge is to get around issues with expressing -.1 in floating point
        self.assertTrue(abs(-.1 - self.control.updateJoint(-.1, .1)) < .005)

        mox.Verify(self.mockJoint)

    def test_update_joint_p_term(self):
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(Lt(2))
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(Gt(2))
        mox.Replay(self.mockJoint)
        self.control.updateJoint(.1, .1)
        # create a new joint_control so that the integral term doesn't interfere with the test
        self.control = joint_control.JointController(self.mockJoint)
        self.control.prev_time = 0
        self.control.updateJoint(2, .1)
        mox.Verify(self.mockJoint)

    def test_update_joint_d_term(self):
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(Gt(1))
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(Lt(1))
        mox.Replay(self.mockJoint)
        self.control.updateJoint(.1, .1)
        self.control = joint_control.JointController(self.mockJoint)
        self.control.prev_time = 0
        self.control.prev_error = .2
        self.control.updateJoint(.1, .1)
        mox.Verify(self.mockJoint)

    def test_update_joint_i_term(self):
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(Lt(3))
        self.mockJoint.getAngle().AndReturn(0)
        self.mockJoint.setLengthRate(Gt(3))
        mox.Replay(self.mockJoint)
        self.control.ki = 100
        self.control.updateJoint(.1, .1)
        self.control.prev_error = 0  
        self.control.updateJoint(.1, .2)
        mox.Verify(self.mockJoint)

    def test_high_target_value(self):
        def run():
            self.control.updateJoint(10, .1)
        self.assertRaises(ValueError, run)

if __name__ == "__main__":
    unittest.main()
