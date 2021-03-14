"""
    unit_tests.py
    This file tests various unique functions in the tic tac toe game.
"""

import unittest
import unittest.mock as mock
from models import Player
from unittest.mock import patch
from app import add_player, update_board, check_whos_ready, DB

USERNAME_INPUT = "username"
EXPECTED_OUTPUT = "expected"

INITIAL_USERNAME = 'Mike'
initial_player = Player(username=INITIAL_USERNAME)



class AddPlayerTestCase(unittest.TestCase):
    """
    Class for testing remove_function in app.py
    """
    def setUp(self):
        self.success_test_params = [
            {
                USERNAME_INPUT: 'Joe',
                EXPECTED_OUTPUT: [initial_player.username,'Joe']
            },
            {
                USERNAME_INPUT: 'Dan',
                EXPECTED_OUTPUT: [initial_player.username,'Joe', 'Dan']
            },
            {
                USERNAME_INPUT: 'Alex',
                EXPECTED_OUTPUT: [initial_player.username,'Joe', 'Dan', 'Alex']
            },
        ]
        

        self.initial_db_mock = [initial_player]
            
    def mocked_db_session_add(self, username):
        self.initial_db_mock.append(username)

    def mocked_db_session_commit(self):
        pass
        
    def test_add_player_success(self):
        """
        function looping through test cases
        """
        testIndex = 1
        for test in self.success_test_params:
            with patch('app.DB.session.add', self.mocked_db_session_add):
                    with patch('app.DB.session.commit', self.mocked_db_session_commit):
                        add_player(test[USERNAME_INPUT])
                        print(self.initial_db_mock)
                        expected_result = test[EXPECTED_OUTPUT]
                        print(expected_result)
                        self.assertEqual(len(self.initial_db_mock), len(expected_result))
                        self.assertEqual(self.initial_db_mock[testIndex].username, expected_result[testIndex])
                        testIndex += 1
                        
class AddPlayerTestCase(unittest.TestCase):
    """
    Class for testing remove_function in app.py
    """
    def setUp(self):
        self.success_test_params = [
            {
                USERNAME_INPUT: 'Joe',
                EXPECTED_OUTPUT: [initial_player.username,'Joe']
            },
            {
                USERNAME_INPUT: 'Dan',
                EXPECTED_OUTPUT: [initial_player.username,'Joe', 'Dan']
            },
            {
                USERNAME_INPUT: 'Alex',
                EXPECTED_OUTPUT: [initial_player.username,'Joe', 'Dan', 'Alex']
            },
        ]
        self.initial_db_mock = [initial_player]
            
    def mocked_db_session_add(self, username):
        self.initial_db_mock.append(username)

    def mocked_db_session_commit(self):
        pass
        
    def test_add_player_success(self):
        """
        function looping through test cases
        """
        testIndex = 1
        for test in self.success_test_params:
            with patch('app.DB.session.add', self.mocked_db_session_add):
                    with patch('app.DB.session.commit', self.mocked_db_session_commit):
                        add_player(test[USERNAME_INPUT])
                        print(self.initial_db_mock)
                        expected_result = test[EXPECTED_OUTPUT]
                        print(expected_result)
                        self.assertEqual(len(self.initial_db_mock), len(expected_result))
                        self.assertEqual(self.initial_db_mock[testIndex].username, expected_result[testIndex])
                        testIndex += 1
                

if __name__ == '__main__':
    unittest.main()
