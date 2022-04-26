import unittest
from ex_1 import my_func


class TestClass(unittest.TestCase):

    def test_ok(self):
        self.assertEqual(my_func(2, -2), 0.25)

    def test_not_equal(self):
        self.assertNotEqual(my_func(2, -2), 2)

    def test_type(self):
        self.assertEqual(my_func(2, 'text'), 'TypeError')

    def test_is_not_none(self):
        self.assertIsNotNone(my_func(2, -2))


if __name__ == '__main__':
    unittest.main()
