import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import PRESENCE, ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from client import create_presence, process_ans


class TestClass(unittest.TestCase):

    def test_def_presense(self):
        test = create_presence()
        test[TIME] = 1.1

        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_incorrect_user(self):
        test = create_presence('User')
        test[TIME] = 1.1

        self.assertNotEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_200_ans(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_400_ans(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad request'}), '400 : Bad request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad request'})

    def test_not_equal_200(self):
        self.assertNotEqual(process_ans({RESPONSE: 200}), '400 : OK')

    def test_not_equal_400(self):
        self.assertNotEqual(process_ans({RESPONSE: 400, ERROR: 'Bad request'}), '200 : OK')

    def test_is_not_none(self):
        self.assertIsNotNone(process_ans)


if __name__ == '__main__':
    unittest.main()
