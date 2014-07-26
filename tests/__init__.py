import os.path
import sys
import unittest


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def get_tests():
    start_dir = os.path.dirname(__file__)
    return unittest.TestLoader().discover(".", pattern="test*.py")
