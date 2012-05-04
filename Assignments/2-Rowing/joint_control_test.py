import joint_control

import mox
import unittest

class TestJointController(unittest.TestCase):
    def setUp(self):
        self.control = joint_control.JointController()
        self.control.prev_time = 0

    def test_update_joint_noop(self):
        mockJoint = mox.MockAnything()
        mockJoint.getAngle().AndReturn(0)
        mox.Replay(mockJoint)
        self.assertEquals(0, self.control.updateJoint(0, mockJoint, None, .1))
        mox.Verify(mockJoint)

    def test_update_joint_small_positive_error(self):
        mockJoint = mox.MockAnything()
        mockJoint.getAngle().AndReturn(0)
        mox.Replay(mockJoint)
        self.assertTrue(0 < self.control.updateJoint(.1, mockJoint, None, .1))
        mox.Verify(mockJoint)

    def test_update_joint_small_negative_error(self):
        mockJoint = mox.MockAnything()
        mockJoint.getAngle().AndReturn(0)
        mox.Replay(mockJoint)
        self.assertTrue(0 > self.control.updateJoint(-.1, mockJoint, None, .1))
        mox.Verify(mockJoint)

    def test_update_joint_p_term(self):
        mockJoint = mox.MockAnything()
        mockJoint.getAngle().AndReturn(0)
        mockJoint.getAngle().AndReturn(0)
        mox.Replay(mockJoint)
        smallResult = self.control.updateJoint(.1, mockJoint, None, .1)
        # create a new joint_control so that the integral term doesn't interfere with the test
        self.control = joint_control.JointController()
        self.control.prev_time = 0
        largeResult = self.control.updateJoint(10, mockJoint, None, .1)
        self.assertTrue(smallResult < largeResult)
        mox.Verify(mockJoint)

    def test_update_joint_d_term(self):
        mockJoint = mox.MockAnything()
        mockJoint.getAngle().AndReturn(0)
        mockJoint.getAngle().AndReturn(0)
        mox.Replay(mockJoint)
        zeroPrevError = self.control.updateJoint(.1, mockJoint, None, .1)
        self.control = joint_control.JointController()
        self.control.prev_time = 0
        self.control.prev_error = .05
        somePrevError = self.control.updateJoint(.1, mockJoint, None, .1)
        self.assertTrue(zeroPrevError > somePrevError)
        mox.Verify(mockJoint)

    def test_update_joint_i_term(self):
        mockJoint = mox.MockAnything()
        mockJoint.getAngle().AndReturn(0)
        mockJoint.getAngle().AndReturn(0)
        mox.Replay(mockJoint)
        firstFlow = self.control.updateJoint(.1, mockJoint, None, .1)
        secondFlow = self.control.updateJoint(.1, mockJoint, None, .2)
        print firstFlow, " ", secondFlow, " ", self.control.iterm
        self.assertTrue(firstFlow < secondFlow)

if __name__ == "__main__":
    unittest.main()
