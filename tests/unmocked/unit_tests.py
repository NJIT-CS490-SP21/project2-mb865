'''
    unit_tests.py
    This file tests various unique functions in the tic tac toe game.
'''
import unittest
from app import remove_player, update_board, check_whos_ready

PLAYER_INPUT = "players"
SID_INPUT = "sid"
EXPECTED_OUTPUT = "players"

class RemovePlayerTestCase(unittest.TestCase):
    """
    Class for testing remove_function in app.py
    """
    def setUp(self):
        self.success_test_params = [
            {
                PLAYER_INPUT: [['Mike', 'abc']],
                SID_INPUT: 'abc',
                EXPECTED_OUTPUT: []
            },
            {
                PLAYER_INPUT: [
                    ['Mike', 'abc'],
                    ['John', '123op'],
                    ['Joe', 'poszxd123']
                ],
                SID_INPUT: '123op',
                EXPECTED_OUTPUT: [
                    ['Mike', 'abc'],
                    ['Joe', 'poszxd123']
                ]
            },
            {
                PLAYER_INPUT: [
                    ['Mike', 'abc'],
                    ['Nick', 'p3975xdfdqw123'],
                    ['Darian', '58456f4ds'],
                    ['Joe', 'poszxd123']
                ],
                SID_INPUT: 'p3975xdfdqw123',
                EXPECTED_OUTPUT: [
                    ['Mike', 'abc'],
                    ['Darian', '58456f4ds'],
                    ['Joe', 'poszxd123']
                ]
            },
        ]


    def test_remove_player_success(self):
        """
        function looping through test cases
        """
        for test in self.success_test_params:
            actual_result = remove_player(test[PLAYER_INPUT], test[SID_INPUT])
            expected_result = test[EXPECTED_OUTPUT]
            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result, expected_result)

BOARD_INPUT = "board"
MOVE_INDEX_INPUT = "index"
SYMBOL_INPUT = "symbol"
EXPECTED_OUTPUT = "board"


class UpdateBoardTestCase(unittest.TestCase):
    """
    Class for testing update_board in app.py
    """
    def setUp(self):
        self.success_test_params = [
            {
                BOARD_INPUT: ['', '', '', '', '', '', '', '', ''],
                MOVE_INDEX_INPUT: 8,
                SYMBOL_INPUT: 'X',
                EXPECTED_OUTPUT: ['', '', '', '', '', '', '', '', 'X']
            },
            {
                BOARD_INPUT: ['X', '', 'O', '', 'O', '', '', 'X', 'X'],
                MOVE_INDEX_INPUT: 5,
                SYMBOL_INPUT:'O',
                EXPECTED_OUTPUT: ['X', '', 'O', '', 'O', 'O', '', 'X', 'X']
            },
            {
                BOARD_INPUT: ['', '', 'X', '', '', 'O', '', '', 'X'],
                MOVE_INDEX_INPUT: 0,
                SYMBOL_INPUT: 'O',
                EXPECTED_OUTPUT: ['O', '', 'X', '', '', 'O', '', '', 'X']
            },
        ]


    def test_update_board_success(self):
        """
        function looping through test cases
        """
        for test in self.success_test_params:
            actual_result = update_board(test[BOARD_INPUT],
                                         test[MOVE_INDEX_INPUT],
                                         test[SYMBOL_INPUT])
            expected_result = test[EXPECTED_OUTPUT]
            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result, expected_result)

PLAY_AGAIN_CHECK_INPUT = "play_again_check"
USER_TYPE_INPUT = "user_type"
EXPECTED_OUTPUT = "play_again_check"

class CheckWhosReadyTestCase(unittest.TestCase):
    """
    Class for testing check_whos_ready in app.py
    """
    def setUp(self):
        self.success_test_params = [
            {
                PLAY_AGAIN_CHECK_INPUT: ['not ready', 'not ready'],
                USER_TYPE_INPUT: 'X',
                EXPECTED_OUTPUT: ['ready', 'not ready']
            },
            {
                PLAY_AGAIN_CHECK_INPUT: ['ready', 'not ready'],
                USER_TYPE_INPUT: 'O',
                EXPECTED_OUTPUT: ['ready', 'ready']
            },
            {
                PLAY_AGAIN_CHECK_INPUT: ['not ready', 'ready'],
                USER_TYPE_INPUT: 'X',
                EXPECTED_OUTPUT: ['ready', 'ready']
            }
        ]


    def test_check_whos_ready_success(self):
        """
        function looping through test cases
        """
        for test in self.success_test_params:
            actual_result = check_whos_ready(test[PLAY_AGAIN_CHECK_INPUT], test[USER_TYPE_INPUT])
            expected_result = test[EXPECTED_OUTPUT]
            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()
