import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import process_client_message


class TestServer(unittest.TestCase):

    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    ok_dict = {RESPONSE: 200}

    def test_ok_check(self):
        test_data = {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertEqual(process_client_message(test_data), self.ok_dict)

    def test_no_action(self):
        test_data = {TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertEqual(process_client_message(test_data), self.err_dict)

    def test_no_time(self):
        test_data = {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertEqual(process_client_message(test_data), self.err_dict)

    def test_no_user(self):
        test_data = {ACTION: PRESENCE, TIME: 1.1}
        self.assertEqual(process_client_message(test_data), self.err_dict)

    def test_unknown_user(self):
        test_data = {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'User'}}
        self.assertEqual(process_client_message(test_data), self.err_dict)


if __name__ == '__main__':
    unittest.main()
