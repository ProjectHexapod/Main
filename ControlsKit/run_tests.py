import unittest
import os


def load_tests(loader, standard_tests, pattern):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    package_tests = loader.discover(this_dir)
    standard_tests.addTests(package_tests)
    return standard_tests


if __name__ == '__main__':
    unittest.main()
