# coding=utf-8
import unittest
from decorators.decorator import *
import time


class TestDecorator(unittest.TestCase):
    def test_timeout(self):
        @timeout(1)
        def test_timeout_no_params():
            time.sleep(2)
            self.assertTrue()

        test_timeout_no_params()

        @timeout(1)
        def test_timeout_with_params(*args, **kwargs):
            self.assertEqual(args, (1, 2, 3))
            self.assertEqual(kwargs, {'a': 1, 'b': 2})

        test_timeout_with_params(1, 2, 3, a=1, b=2)


if __name__ == '__main__':
    unittest.main()
