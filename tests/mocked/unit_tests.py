"""
    unit_tests.py
    This file tests various unique functions in the tic tac toe game.
"""

import unittest
import unittest.mock as mock
from models import Player
from unittest.mock import patch
from app import add_player, get_top_players, update_points, DB

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
                        expected_result = test[EXPECTED_OUTPUT]
                        self.assertEqual(len(self.initial_db_mock), len(expected_result))
                        self.assertEqual(self.initial_db_mock[testIndex].username, expected_result[testIndex])
                        testIndex += 1
   
AMOUNT_INPUT = "amount"
INITIAL_PLAYERS = [
    Player(username="Mike", points=103),#0
    Player(username="Dan", points=101),#1
    Player(username="Joe", points=100),#2
    Player(username="Jess", points=98),#3
    Player(username="Paul", points=99),#4
    Player(username="Ringo", points=106),#5
    Player(username="Alex", points=101),#6
    Player(username="Darian", points=94),#7
    Player(username="Penelope", points=95),#8
    Player(username="Vicky", points=89),#9
    Player(username="Fred", points=109),#10
    Player(username="Quin", points=100),#11
    Player(username="Batman", points=102),#12
    Player(username="Pikachu", points=92),#13
    Player(username="Charizard", points=88),#14
    Player(username="Oly", points=101),#15
    Player(username="Tom", points=115),#16
    Player(username="Tim", points=1),#17
    Player(username="Rex", points=999),#18
    Player(username="Christina", points=54), #19
]

class GetTopPlayersTestCase(unittest.TestCase):
    """
    Class for testing get_top_ten in app.py
    """
    def setUp(self):
        self.success_test_params = [
            {
                AMOUNT_INPUT: 10,
                EXPECTED_OUTPUT: [
                    {'username': 'Rex', 'points': 999},
                    {'username': 'Tom', 'points': 115},
                    {'username': 'Fred', 'points': 109},
                    {'username': 'Ringo', 'points': 106},
                    {'username': 'Mike', 'points': 103},
                    {'username': 'Batman', 'points': 102},
                    {'username': 'Dan', 'points': 101},
                    {'username': 'Alex', 'points': 101},
                    {'username': 'Oly', 'points': 101},
                    {'username': 'Joe', 'points': 100},
                ]
            },
            {
                AMOUNT_INPUT: 15,
                EXPECTED_OUTPUT: [
                    {'username': 'Rex', 'points': 999},
                    {'username': 'Tom', 'points': 115},
                    {'username': 'Fred', 'points': 109},
                    {'username': 'Ringo', 'points': 106},
                    {'username': 'Mike', 'points': 103},
                    {'username': 'Batman', 'points': 102},
                    {'username': 'Dan', 'points': 101},
                    {'username': 'Alex', 'points': 101},
                    {'username': 'Oly', 'points': 101},
                    {'username': 'Joe', 'points': 100},
                    {'username': 'Quin', 'points': 100},
                    {'username': 'Paul', 'points': 99},
                    {'username': 'Jess', 'points': 98},
                    {'username': 'Penelope', 'points': 95},
                    {'username': 'Darian', 'points': 94},
                ]
            },
            {
                AMOUNT_INPUT: 20,
                EXPECTED_OUTPUT: [
                    {'username': 'Rex', 'points': 999},
                    {'username': 'Tom', 'points': 115},
                    {'username': 'Fred', 'points': 109},
                    {'username': 'Ringo', 'points': 106},
                    {'username': 'Mike', 'points': 103},
                    {'username': 'Batman', 'points': 102},
                    {'username': 'Dan', 'points': 101},
                    {'username': 'Alex', 'points': 101},
                    {'username': 'Oly', 'points': 101},
                    {'username': 'Joe', 'points': 100},
                    {'username': 'Quin', 'points': 100},
                    {'username': 'Paul', 'points': 99},
                    {'username': 'Jess', 'points': 98},
                    {'username': 'Penelope', 'points': 95},
                    {'username': 'Darian', 'points': 94},
                    {'username': 'Pikachu', 'points': 92},
                    {'username': 'Vicky', 'points': 89},
                    {'username': 'Charizard', 'points': 88},
                    {'username': 'Christina', 'points': 54},
                    {'username': 'Tim', 'points': 1},
                ]
            },
        ]
        self.initial_db_mock = INITIAL_PLAYERS
        
    def mocked_person_query_all_desc(self, orderby):
        newlist = sorted(self.initial_db_mock, key=lambda x: x.points, reverse=True)
        return newlist
        
    def test_get_top_players_success(self):
        """
        function looping through test cases
        """
        for test in self.success_test_params:
            with patch('models.Player.query') as mocked_query:
                mocked_query.order_by = self.mocked_person_query_all_desc
                actual_result = get_top_players(test[AMOUNT_INPUT])
                expected_result = test[EXPECTED_OUTPUT]
                self.assertEqual(len(actual_result), len(expected_result))
                self.assertEqual(actual_result, expected_result)
    
VICTOR_INPUT = "victor_name"
LOSER_INPUT = "loser_name"
EXPECTED_OUTPUT = "expected"

                
class UpdatePointsTestCase(unittest.TestCase):
    """
    Class for testing update_points in app.py
    """
    def setUp(self):
        self.success_test_params = [
            {
                VICTOR_INPUT: 'Rex',
                LOSER_INPUT: 'Tom',
                EXPECTED_OUTPUT: [
                    {'username': 'Rex', 'points': 1000},
                    {'username': 'Tom', 'points': 114},
                    {'username': 'Fred', 'points': 109},
                    {'username': 'Ringo', 'points': 106},
                    {'username': 'Mike', 'points': 103},
                    {'username': 'Batman', 'points': 102},
                    {'username': 'Dan', 'points': 101},
                    {'username': 'Alex', 'points': 101},
                    {'username': 'Oly', 'points': 101},
                    {'username': 'Joe', 'points': 100},
                    {'username': 'Quin', 'points': 100},
                    {'username': 'Paul', 'points': 99},
                    {'username': 'Jess', 'points': 98},
                    {'username': 'Penelope', 'points': 95},
                    {'username': 'Darian', 'points': 94},
                    {'username': 'Pikachu', 'points': 92},
                    {'username': 'Vicky', 'points': 89},
                    {'username': 'Charizard', 'points': 88},
                    {'username': 'Christina', 'points': 54},
                    {'username': 'Tim', 'points': 1},
                ]
            },
            {
                VICTOR_INPUT: 'Mike',
                LOSER_INPUT: 'Vicky',
                EXPECTED_OUTPUT: [
                    {'username': 'Rex', 'points': 999},
                    {'username': 'Tom', 'points': 115},
                    {'username': 'Fred', 'points': 109},
                    {'username': 'Ringo', 'points': 106},
                    {'username': 'Mike', 'points': 104},
                    {'username': 'Batman', 'points': 102},
                    {'username': 'Dan', 'points': 101},
                    {'username': 'Alex', 'points': 101},
                    {'username': 'Oly', 'points': 101},
                    {'username': 'Joe', 'points': 100},
                    {'username': 'Quin', 'points': 100},
                    {'username': 'Paul', 'points': 99},
                    {'username': 'Jess', 'points': 98},
                    {'username': 'Penelope', 'points': 95},
                    {'username': 'Darian', 'points': 94},
                    {'username': 'Pikachu', 'points': 92},
                    {'username': 'Vicky', 'points': 88},
                    {'username': 'Charizard', 'points': 88},
                    {'username': 'Christina', 'points': 54},
                    {'username': 'Tim', 'points': 1},
                ]
            },
            {
                VICTOR_INPUT: 'Tim',
                LOSER_INPUT: 'Rex',
                EXPECTED_OUTPUT: [
                    {'username': 'Rex', 'points': 998},
                    {'username': 'Tom', 'points': 115},
                    {'username': 'Fred', 'points': 109},
                    {'username': 'Ringo', 'points': 106},
                    {'username': 'Mike', 'points': 103},
                    {'username': 'Batman', 'points': 102},
                    {'username': 'Dan', 'points': 101},
                    {'username': 'Alex', 'points': 101},
                    {'username': 'Oly', 'points': 101},
                    {'username': 'Joe', 'points': 100},
                    {'username': 'Quin', 'points': 100},
                    {'username': 'Paul', 'points': 99},
                    {'username': 'Jess', 'points': 98},
                    {'username': 'Penelope', 'points': 95},
                    {'username': 'Darian', 'points': 94},
                    {'username': 'Pikachu', 'points': 92},
                    {'username': 'Vicky', 'points': 89},
                    {'username': 'Charizard', 'points': 88},
                    {'username': 'Christina', 'points': 54},
                    {'username': 'Tim', 'points': 2},
                ]
            },
        ]
        self.initial_db_mock = INITIAL_PLAYERS
    
    def mocked_db_query_filter_first(self):
        return self.initial_db_mock
        
    def test_update_points_success(self):
        """
        function looping through test cases
        """
        for test in self.success_test_params:
            with patch('app.DB.session.query.filter_by.first', self.mocked_db_query_filter_first):
                actual_result = update_points(test[VICTOR_INPUT], test[LOSER_INPUT])
                print(actual_result)
                expected_result = test[EXPECTED_OUTPUT]
                # print(actual_result)
                # print(expected_result)
                

if __name__ == '__main__':
    unittest.main()
