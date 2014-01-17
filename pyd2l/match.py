import re
from urllib.request import urlopen
import random
from math import ceil, floor

from bs4 import BeautifulSoup

class InvalidMatchError(Exception):
    def __init__(self, message):
        self.message = message

class Match(object):
    def __init__(self, match_id):
        self.match_id = match_id
        self.match_url = self._determine_match_url()
        self._soup = self._get_match_soup()
        self._valid_match_url = self._determine_match_404()
        self._match_details = self._get_match_details()
        self.num_bettors, self.num_items = map(int, re.findall('[\d]*[^\D](?=\s)', self._get_bet_string()))
        self.teams, self.winner, self.loser = self._get_teams_and_winner_and_loser()
        self.odds = self._get_odds()
        self.rewards = self._get_rewards()

    def __str__(self):
        if self.is_valid_match():
            return 'id:{} {} vs. {}'.format(self.match_id, *self.teams)

    def __repr__(self):
        return str(self.match_id)

    def _determine_match_url(self):
        return 'http://dota2lounge.com/match?m={}'.format(self.match_id)

    def _get_match_soup(self):
        return BeautifulSoup(urlopen(self.match_url))

    def _get_match_details(self):
        return self._soup.find('section', {'class': 'box'})

    def _determine_match_404(self):
        try:
            if self._soup.find('h1').text == '404':
                raise InvalidMatchError('invalid URL')
        except AttributeError:
            return True

    def _get_bet_string(self):
        return self._soup.find('div',
                               {'class': 'gradient',
                                'style': 'float:left;width:100%;color: #DFDFDF; border-radius: 5px'}).text.strip()

    def _get_teams_and_winner_and_loser(self):
        teams = [team.getText() for team in
                 self._soup.find('section', {'class': 'box'}).findAll('b')]
        winner = False
        loser = False
        for number, team in enumerate(teams):
            if ' (win)' in team:
                teams[number] = teams[number].replace(' (win)', '')
                winner = teams[number]

                loser = teams[number - 1]
        if not loser and not winner:
            raise InvalidMatchError('no winner recorded in match')
        else:
            return teams, winner, loser

    def _get_odds(self):
        return {team: int(tag.get_text().strip('%')) for team, tag in zip(self.teams, self._match_details.findAll('i'))}

    def _get_rewards(self):

        team_a_odds = self._match_details.findAll('div', {'style': "float: left; margin: 0.25em 2%;"})
        team_b_odds = self._match_details.findAll('div', {'style': "float: right; margin: 0.25em 2%;"})

        rewards = dict()

        rewards[self.teams[0]] = {
            list(rewards.strings)[0]: {int(i.split(' ')[2]): float(i.split(' ')[0]) for i in list(rewards.strings)[1:5]}
            for
            rewards in team_a_odds}
        rewards[self.teams[1]] = {
            list(rewards.strings)[0]: {int(i.split(' ')[2]): float(i.split(' ')[0]) for i in list(rewards.strings)[1:5]}
            for
            rewards in team_b_odds}

        return rewards

    def is_valid_match(self):
        return all([self._valid_match_url, self.winner])

    def favorite(self):
        return max(self.odds, key=self.odds.get)

    def calculate_reward(self, team, rarity='Rares', num_bet=4, reward_round=False):
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