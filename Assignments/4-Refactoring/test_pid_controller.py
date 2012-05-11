import unittest

from pid_controller import PidController


class PidControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.pid = PidController(0.0, 0.0, 0.0)
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

