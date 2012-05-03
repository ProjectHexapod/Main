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



if __name__ == "__main__":
    unittest.main()
