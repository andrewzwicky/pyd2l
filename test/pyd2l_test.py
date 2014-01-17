import unittest
from unittest.mock import patch
from pyd2l.match import Match, InvalidMatchError


class MatchTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.test_match = Match(1899)

    def test_d2lpage_init(self):
        self.assertEquals(self.test_match.match_id, 1899)

    def test_invalid_match(self):
        self.assertRaisesRegexp(InvalidMatchError, 'invalid URL' , Match, -1)
        self.assertRaisesRegexp(InvalidMatchError, 'no winner recorded in match', Match, 526)

    def test_determine_url_from_id(self):
        self.assertEqual(self.test_match._determine_match_url(), 'http://dota2lounge.com/match?m=1899')

    def test_correct_print(self):
        self.assertEqual(self.test_match.__str__(), 'id:1899 LGD.cn vs. Fnatic.eu')

    def test_correct_repr(self):
        self.assertEqual(self.test_match.__repr__(), '1899')

    def test_true_match_returns_correct_validity(self):
        self.assertEqual(self.test_match._determine_match_404(), True)

    def test_gets_correct_bet_string(self):
        self.assertEqual(self.test_match._get_bet_string(), '17007 people placed 55449 items.')

    def test_correct_num_bettors_counted(self):
        self.assertEqual(self.test_match.num_bettors, 17007)

    def test_correct_num_items_counted(self):
        self.assertEqual(self.test_match.num_items, 55449)

    def test_correct_teams(self):
        self.assertEqual(self.test_match.teams, ['LGD.cn', 'Fnatic.eu'])

    def test_correct_winner(self):
        self.assertEqual(self.test_match.winner, 'LGD.cn')

    def test_correct_loser(self):
        self.assertEqual(self.test_match.loser, 'Fnatic.eu')

    def test_gets_correct_odds(self):
        self.assertEqual(self.test_match._get_odds(), {'LGD.cn': 64, 'Fnatic.eu': 36})

    def test_correct_rewards(self):
        rewards = {'LGD.cn': {'Commons': {1: 0.6, 2: 1.3, 3: 1.9, 4: 2.6},
                              'Keys': {1: 0.5, 2: 1.0, 3: 1.5, 4: 2.0},
                              'Rares': {1: 0.5, 2: 1.0, 3: 1.5, 4: 2.0},
                              'Uncommons': {1: 0.6, 2: 1.3, 3: 1.9, 4: 2.5}},
                   'Fnatic.eu': {'Commons': {1: 1.5, 2: 3, 3: 4.6, 4: 6.1},
                                 'Keys': {1: 1.8, 2: 3.7, 3: 5.5, 4: 7.4},
                                 'Rares': {1: 2.0, 2: 4.0, 3: 6.0, 4: 7.9},
                                 'Uncommons': {1: 1.5, 2: 3.1, 3: 4.6, 4: 6.2}}}

        self.assertEqual(self.test_match._get_rewards(), rewards)

    def test_is_valid_match(self):
        self.assertEqual(self.test_match.is_valid_match(), True)

    def test_favorite(self):
        self.assertEqual(self.test_match.favorite(), 'LGD.cn')

    def test_calculate_rewards(self):
        self.assertEqual(self.test_match.calculate_reward('LGD.cn'), 2.0)

    def test_loss_reward(self):
        self.assertEqual(self.test_match.calculate_reward(self.test_match.loser), -4)

    def test_raw_rewards(self):
        self.assertEqual(self.test_match.calculate_reward(self.test_match.winner, num_bet=3), 1.5)

    def test_calculate_reward_rounded_ceil(self):
        with patch('pyd2l.match.random') as mock_random:
            mock_random.random.return_value = 0.9
            self.assertEqual(self.test_match.calculate_reward(self.test_match.winner, num_bet=3, reward_round=True),
                             2.0)

    def test_calculate_reward_rounded_floor(self):
        with patch('pyd2l.match.random') as mock_random:
            mock_random.random.return_value = 0.1
            self.assertEqual(self.test_match.calculate_reward(self.test_match.winner, num_bet=3, reward_round=True),
                             1.0)

    def test_random_team_choice(self):
        with patch('pyd2l.match.random') as mock_random:
            mock_random.random.return_value = 0.9
            mock_random.choice.return_value = 'LGD.cn'
            self.assertEqual(
                self.test_match.calculate_reward([self.test_match.winner, self.test_match.loser][0], num_bet=3,
                                                 reward_round=True), 2.0)
