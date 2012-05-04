import unittest
from trajectory import Trajectory
import numpy as np


class MetaTestTrajectory(object):
    """
    Contains test functions to be used with injected data from the
    build_tests function.
    """

    def test_acceleration(self):
        """
        Test that acceleration is constant during the first third last
        third of the trajectory interval.
        """
        third_time = self.third_time
        times = np.arange(self.start_time + third_time*0.05, self.end_time - third_time * 2.05, 0.01 )

        def thing(times):
            derp = np.array(zip(*[self.tr.getTargetJointAngles(t) for t in times]))
            v = [x[1:] - x[0:-1] for x in derp]
            a = [vx[1:] - vx[0:-1] for vx in v]
            return a

        a = thing(times)
        print "Make sure this is a list: ", type(a)
        times = np.arange(self.start_time + 2.05 * third_time, self.end_time - third_time * 0.05, 0.01)
        a+= thing(times)

        for acc in a:
            print abs(np.std(acc))
            self.assertLess(abs(np.std(acc)), 1e-8)

    def test_velocity(self):
        """
        Test that velocity is constant during the second third of the
        trajectory interval.
        """
        third_time = self.third_time
        times = np.arange(self.start_time + third_time * 1.05, self.end_time - third_time*1.05, 0.01)

        derp = np.array(zip(*[self.tr.getTargetJointAngles(t) for t in times]))
        v = [x[1:] - x[0:-1] for x in derp]

        for vel in v:
            print "vel: ", abs(np.std(vel))
            self.assertLess(abs(np.std(vel)), 1e-8)

    def test_continuity(self):
        """
        Test that consecutive points are within a reasonable distance from one another.
        """
        times = np.arange(self.start_time, self.end_time, 0.01)

        derp = np.array(zip(*[self.tr.getTargetJointAngles(t) for t in times]))
        v = [x[1:] - x[0:-1] for x in derp]

        for delta in v:
            print "max delta: ", np.max(np.abs(delta))
            self.assertLess(abs(np.max(np.abs(delta))), self.continuity_limit)

    def test_sanity(self):
        """
        Test that start and end points are computed correctly.
        """

        print "END TIME: ", self.end_time
        times = [self.start_time, self.end_time]
        real = reduce(lambda x,y: x+y, [self.tr.getTargetJointAngles(t) for t in times])
        ideal = self.start_position + self.end_position
        d = [r-i for r,i in zip(real,ideal)]

        for diff in d:
            print "diff: ", abs(diff)
            self.assertLess(abs(diff), 1e-8)

def setUpCreator(data):
    class setUpHolder(object):
        def setUp(self):
            start_position = data['start_position']
            end_position = data['end_position']
            self.start_position = start_position
            self.end_position = end_position
            self.start_time = data['start_time']
            self.end_time = data['end_time']
            self.continuity_limit = data['continuity_limit']
            robot = "Dummy data"
            self.third_time = (self.end_time - self.start_time)/3.
            self.tr = Trajectory(start_position, end_position, robot, self.start_time, self.end_time)
    return setUpHolder



# All tests will be run once each with each data set
# Continuity limit is a constant used in the test_continuity function, it is
# the maximum allowed distance between two consecutive points that are
# 0.01 seconds apart
data = [
    {
        'start_position'    : [0.,0.,0.],
        'end_position'      : [100., 0., 0.],
        'start_time'        : 0.,
        'end_time'          : 100.,
        'continuity_limit'  : 5.
    }, {
        'start_position'    : [-743., 83., 200.],
        'end_position'      : [20., 8000.41, 200.],
        'start_time'        : 139.,
        'end_time'          : 153.2,
        'continuity_limit'  : 20.
    }, {
        'start_position'    : [300., 600., 400.],
        'end_position'      : [32., 9000., 5342.],
        'start_time'        : 30.,
        'end_time'          : 126.,
        'continuity_limit'  : 5.
    }, {
        'start_position'    : [30., 0., -2509.],
        'end_position'      : [0., 0., 0.,],
        'start_time'        : 300.,
        'end_time'          : 5000.,
        'continuity_limit'  : 5.
#    }, {
# Uncomment and add more test cases if desired



}]

def build_tests():
    current_module = __import__(__name__)
    for i in range(len(data)):
        print "Creating test: " + str(i)
        test_name = "TestTrajectory" + str(i)
        if not hasattr(current_module, test_name):
            test_class_instance = type(test_name, (setUpCreator(data[i]),
                                            MetaTestTrajectory, unittest.TestCase), {})
            setattr(current_module, test_name, test_class_instance)

build_tests()


if __name__ == "__main__":
    unittest.main()