import unittest
from trajectory import Trajectory
import numpy as np

class TestTrajectory(unittest.TestCase):

    def setUp(self):
        start_position = [30.,600.,-400.]
        end_position = [32., 9000., 5324.]
        self.start_position = start_position
        self.end_position = end_position
        self.start_time = 30.
        self.end_time = 126.
        robot = "Dummy data"
        self.third_time = (self.end_time - self.start_time)/3.
        self.tr = Trajectory(start_position, end_position, robot, self.start_time, self.end_time)

    def test_acceleration(self):
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
        third_time = self.third_time
        times = np.arange(self.start_time + third_time * 1.05, self.end_time - third_time*1.05, 0.01)

        derp = np.array(zip(*[self.tr.getTargetJointAngles(t) for t in times]))
        v = [x[1:] - x[0:-1] for x in derp]

        for vel in v:
            print "vel: ", abs(np.std(vel))
            self.assertLess(abs(np.std(vel)), 1e-8)

    def test_continuity(self):
        times = np.arange(self.start_time, self.end_time, 0.01)

        derp = np.array(zip(*[self.tr.getTargetJointAngles(t) for t in times]))
        v = [x[1:] - x[0:-1] for x in derp]

        for delta in v:
            print "max delta: ", np.max(np.abs(delta))
            self.assertLess(abs(np.max(np.abs(delta))), 5.)

    def test_sanity(self):
        times = [self.start_time, self.end_time]
        real = reduce(lambda x,y: x+y, [self.tr.getTargetJointAngles(t) for t in times])
        ideal = self.start_position + self.end_position
        d = [r-i for r,i in zip(real,ideal)]

        for diff in d:
            print "diff: ", abs(diff)
            self.assertLess(abs(diff), 1e-8)




if __name__ == "__main__":
    unittest.main()