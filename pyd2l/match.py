import re
import random
from math import ceil, floor
from urllib.request import urlopen
import csv
import sys
from http.client import IncompleteRead

from bs4 import BeautifulSoup


class InvalidMatchError(Exception):
    def __init__(self, message):
        self.message = message


def parse_match(match_id):
    match_url = 'http://dota2lounge.com/match?m={}'.format(match_id)
    soup = BeautifulSoup(urlopen(match_url))
    valid_match_url = _determine_match_404(soup)
    match_details = _get_match_details(soup)
    num_bettors, num_items = map(int, re.findall('[\d]*[^\D](?=\s)', _get_bet_string(soup)))
    teams, winner, loser = _get_teams_and_winner_and_loser(soup)
    odds = _get_odds(teams, match_details)
    rewards = _get_rewards(match_details, teams)

    return Match(match_id, match_url, num_bettors, num_items, teams, winner, loser, odds, rewards, valid_match_url)


def _get_match_details(soup):
    return soup.find('section', {'class': 'box'})


def _determine_match_404(soup):
    try:
        if soup.find('h1').text == '404':
            raise InvalidMatchError('invalid URL')
    except AttributeError:
        return True


def _get_bet_string(soup):
    return soup.find('div',
                     {'class': 'gradient',
                      'style': 'float:left;width:100%;color: #DFDFDF; border-radius: 5px'}).text.strip()


def _get_teams_and_winner_and_loser(soup):
    teams = [team.getText() for team in soup.find('section', {'class': 'box'}).findAll('b')]
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


def _get_odds(teams, match_details):
    return {team: int(tag.get_text().strip('%')) for team, tag in zip(teams, match_details.findAll('i'))}


def _get_rewards(match_details, teams):
    odds = [match_details.findAll('div', {'style': "float: left; margin: 0.25em 2%;"}),
            match_details.findAll('div', {'style': "float: right; margin: 0.25em 2%;"})]

    final_rewards = {}

    for team, reward in zip(teams, odds):
        final_rewards[team] = {}
        for rarity_string in reward:
            rarity_list = list(rarity_string.strings)
            rarity_key = rarity_list.pop(0)
            rarity_dict = {int(bet): float(payoff) for payoff, bet in
                           [pay_str.split(' for ') for pay_str in rarity_list]}
            final_rewards[team][rarity_key] = rarity_dict
        if 'Keys' not in final_rewards[team].keys():
            final_rewards[team]['Keys'] = {1: 0, 2: 0, 3: 0, 4: 0}

    return final_rewards


def flatten(d):
    if type(d) in [dict, list]:
        try:
            for k, v in d.items():
                yield k
                for nested_v in flatten(v):
                    yield nested_v

        except AttributeError:
            for list_v in d:
                yield list_v
    else:
        yield d


def unflatten(match_row_csv):
    params = ['match_id', 'match_url', 'num_bettors', 'num_items', 'teams', 'winner', 'loser', 'odds', 'rewards',
              '_valid_match_url']
    csv_iter = iter(match_row_csv)
    for _ in params:
        param = next(csv_iter)
        if param in params:
            if param == 'match_id':
                match_id = int(next(csv_iter))
            elif param == 'match_url':
                match_url = next(csv_iter)
            elif param == 'num_bettors':
                num_bettors = int(next(csv_iter))
            elif param == 'num_items':
                num_items = int(next(csv_iter))
            elif param == 'teams':
                teams = [next(csv_iter), next(csv_iter)]
            elif param == 'loser':
                loser = next(csv_iter)
            elif param == 'winner':
                winner = next(csv_iter)
            elif param == '_valid_match_url':
                valid_url = bool(next(csv_iter))
            elif param == 'odds':
                o_list = [next(csv_iter) for _ in range(4)][::-1]
                o_iter = iter(o_list)
                odds = {next(o_iter): int(next(o_iter)) for _ in range(2)}
            elif param == 'rewards':
                r_list = [next(csv_iter) for _ in range(74)][::-1]
                r_iter = iter(r_list)
                rewards = {next(r_iter):
                               {next(r_iter):
                                    {int(next(r_iter)): float(next(r_iter)) for bet in range(4)} for rarity in range(4)}
                           for team in range(2)}

    return Match(match_id, match_url, num_bettors, num_items, teams, winner, loser, odds, rewards, valid_url)


def write_matches_csv(file_name, match_range):
    progress_bar_width = 100
    with open(file_name, 'w', encoding='utf-8', newline='') as target_csv:
        target_writer = csv.writer(target_csv, delimiter=',')
        for i, m_id in enumerate(match_range):
            sys.stdout.flush()
            progress = int(i // (len(match_range) / progress_bar_width))
            sys.stdout.write('\r[{}{}]{}'.format('#' * progress, ' ' * (progress_bar_width - progress), m_id))
            try:
                target_writer.writerow(list(flatten(parse_match(m_id).__dict__)))
            except (InvalidMatchError, IncompleteRead):
                pass
        sys.stdout.flush()
        sys.stdout.write('\r[{}{}]'.format('#' * progress_bar_width, ' ' * 0))


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


if __name__ == '__main__':
    match_text = [row.decode() for row in urlopen('https://raw.github.com/garth5689/pyd2l/master/match_cache.csv').readlines()]
    match_reader = csv.reader(match_text, delimiter=',')
    matches = [unflatten(row) for row in match_reader]
    print(matches)
