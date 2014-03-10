import unittest
from unittest.mock import patch
import pickle

from pyd2l.methods import get_match_details, match_404, get_bet_string, get_teams_and_winner_and_loser, get_odds, \
    get_rewards, flatten, unflatten
from pyd2l.match import InvalidMatchError


class PyD2LMethodsTest(unittest.TestCase):
    def setUp(self):
        with open('soup_1899_pickle.pkl', 'rb') as soup_pickle: self.soup = pickle.load(soup_pickle)
        with open('soup_1899_details_pickle.pkl', 'rb') as details_pickle: self.test_details = pickle.load(
            details_pickle)
        with open('test_Match_1899_pickle.pkl', 'rb') as test_Match_pickle: self.test_match = pickle.load(
            test_Match_pickle)
        self.flattened_1899 = ['match_id', 1899, 'num_bettors', 17007, 'rewards', 'Fnatic.eu', 'Keys', 1, 1.8, 2, 3.7,
                               3, 5.5, 4, 7.4, 'Commons', 1, 1.5, 2, 3.0, 3, 4.6, 4, 6.1, 'Uncommons', 1, 1.5, 2, 3.1,
                               3, 4.6, 4, 6.2, 'Rares', 1, 2.0, 2, 4.0, 3, 6.0, 4, 7.9, 'LGD.cn', 'Keys', 1, 0.5, 2,
                               1.0, 3, 1.5, 4, 2.0, 'Commons', 1, 0.6, 2, 1.3, 3, 1.9, 4, 2.6, 'Uncommons', 1, 0.6, 2,
                               1.3, 3, 1.9, 4, 2.5, 'Rares', 1, 0.5, 2, 1.0, 3, 1.5, 4, 2.0, 'odds', 'Fnatic.eu', 36,
                               'LGD.cn', 64, 'winner', 'LGD.cn', 'teams', 'LGD.cn', 'Fnatic.eu', '_valid_match_url',
                               True, 'match_url', 'http://dota2lounge.com/match?m=1899', 'loser', 'Fnatic.eu',
                               'num_items', 55449]

    def test_get_match_details(self):
        self.assertEqual(self.test_details, get_match_details(self.soup))

    def test_match_404(self):
        self.assertEqual(match_404(self.soup), False)

        with open('soup_404_pickle.pkl', 'rb') as soup_pickle:
            soup_404 = pickle.load(soup_pickle)
            with self.assertRaises(InvalidMatchError):
                match_404(soup_404)

    def test_get_bet_string(self):
        self.assertEqual(get_bet_string(self.soup), '17007 people placed 55449 items.')

    def test_get_teams_and_winner_and_loser(self):
        self.assertEqual(get_teams_and_winner_and_loser(self.soup), (['LGD.cn', 'Fnatic.eu'], 'LGD.cn', 'Fnatic.eu'))

    def test_get_odds(self):
        self.assertEqual(get_odds(['LGD.cn', 'Fnatic.eu'], self.test_details), {'LGD.cn': 64, 'Fnatic.eu': 36})

    def test_get_rewards(self):
        rewards = {'LGD.cn': {'Commons': {1: 0.6, 2: 1.3, 3: 1.9, 4: 2.6},
                              'Keys': {1: 0.5, 2: 1.0, 3: 1.5, 4: 2.0},
                              'Rares': {1: 0.5, 2: 1.0, 3: 1.5, 4: 2.0},
                              'Uncommons': {1: 0.6, 2: 1.3, 3: 1.9, 4: 2.5}},
                   'Fnatic.eu': {'Commons': {1: 1.5, 2: 3.0, 3: 4.6, 4: 6.1},
                                 'Keys': {1: 1.8, 2: 3.7, 3: 5.5, 4: 7.4},
                                 'Rares': {1: 2.0, 2: 4.0, 3: 6.0, 4: 7.9},
                                 'Uncommons': {1: 1.5, 2: 3.1, 3: 4.6, 4: 6.2}}}
        self.assertEqual(get_rewards(self.test_details, ['LGD.cn', 'Fnatic.eu']), rewards)

    def test_flatten(self):
        self.assertEqual(set(flatten(self.test_match.__dict__)), set(self.flattened_1899))

    def test_unflatten(self):
        self.assertEqual(unflatten(self.flattened_1899).__dict__, self.test_match.__dict__)


class MatchTest(unittest.TestCase):
    def setUp(self):
        # with patch('pyd2l.methods.urlopen') as urlopen_patch:
        #     urlopen_patch.return_value = open('Dota 2 Lounge - LGD.cn vs Fnatic.eu - Match 1899.html')
        #     self.test_match = parse_match(1899)
        with open('test_Match_1899_pickle.pkl', 'rb') as test_Match_pickle: self.test_match = pickle.load(
            test_Match_pickle)

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
