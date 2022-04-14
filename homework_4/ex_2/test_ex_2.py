import unittest
from ex_2 import my_fun


class TestClass(unittest.TestCase):

    def test_ok(self):
        self.assertEqual(my_fun(5, 5, '+'), 10)

    def test_not_equal(self):
        self.assertNotEqual(my_fun(5, 5, '*'), 10)

    def test_type_one(self):
        self.assertEqual(my_fun('5', 5, '+'), 'TypeError')

    def test_type_two(self):
        self.assertEqual(my_fun(5, '5', '+'), 'TypeError')

    def test_type_free(self):
        self.assertEqual(my_fun(5, 5, '%'), 'TypeError')

    def test_no_data(self):
        self.assertEqual(my_fun('', '', ''), 'TypeError')

    def test_del_by_zero(self):
        self.assertEqual(my_fun(5, 0, '/'), 'Делить на "0" нельзя!')


if __name__ == '__main__':
    unittest.main()
