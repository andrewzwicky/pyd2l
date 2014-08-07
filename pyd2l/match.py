import random
from math import ceil, floor

class InvalidMatchError(Exception):
    def __init__(self, message):
        self.message = message


class Match(object):
    def __init__(self, match_id, match_url, num_bettors, num_items, teams, winner, loser, odds, rewards,
                 valid_url):
        self.match_id = match_id
        self.match_url = match_url
        self.num_bettors = num_bettors
        self.num_items = num_items
        self.teams = teams
        self.winner = winner
        self.loser = loser
        self.odds = odds
        self.rewards = rewards
        self._valid_match_url = valid_url

    def __str__(self):
        if self.is_valid_match():
            return 'id:{} {} vs. {}'.format(self.match_id, *self.teams)

    def __repr__(self):
        return str(self.match_id)

    def is_valid_match(self):
        return all([self._valid_match_url, self.winner])

    def favorite(self):
        return max(self.odds, key=self.odds.get)

    def underdog(self):
        return min(self.odds, key=self.odds.get)

    def calculate_reward(self, team, rarity='Rares', num_bet=4, reward_round=True):
        if team == self.winner:
            raw_reward = self.rewards[team][rarity][num_bet]
            if reward_round:
                if raw_reward % 1 < random.random():
                    return ceil(raw_reward)
                else:
                    return floor(raw_reward)
            else:
                return raw_reward
        else:
            return -num_bet
