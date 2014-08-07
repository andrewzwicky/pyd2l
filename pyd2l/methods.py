import re
from urllib.request import urlopen
import csv
import sys
import itertools
import multiprocessing

from bs4 import BeautifulSoup

from pyd2l.match import Match, InvalidMatchError


def parse_match(match_id):
    match_url = 'http://dota2lounge.com/match?m={}'.format(match_id)
    soup = BeautifulSoup(urlopen(match_url))
    valid_match_url = not match_404(soup)
    match_details = get_match_details(soup)
    num_bettors, num_items = map(int, re.findall('[\d]*[^\D](?=\s)', get_bet_string(soup)))
    teams, winner, loser = get_teams_and_winner_and_loser(soup)
    odds = get_odds(teams, match_details)
    rewards = get_rewards(match_details, teams)

    return Match(match_id, match_url, num_bettors, num_items, teams, winner, loser, odds, rewards, valid_match_url)


def get_match_details(soup):
    return soup.find('section', {'class': 'box'})


#TODO: This should include other methods of matches being invalid. i.e. #272, 1-13
def match_404(soup):
    try:
        if soup.find('h1').text == '404':
            raise InvalidMatchError('invalid URL')
    except AttributeError:
        return False


def get_bet_string(soup):
    return soup.find('div',
                     {'class': 'gradient',
                      'style': 'float:left;width:100%;color: #DFDFDF; border-radius: 5px'}).text.strip()


def get_teams_and_winner_and_loser(soup):
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


def get_odds(teams, match_details):
    return {team: int(tag.get_text().strip('%')) for team, tag in zip(teams, match_details.findAll('i'))}


def get_rewards(match_details, teams):
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
            for k, v in sorted(d.items()):
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
    match_id = match_url = num_bettors = num_items = teams = winner = loser = odds = rewards = valid_url = None
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
                odds_list = [next(csv_iter) for _ in range(4)][::-1]
                odds_iter = iter(odds_list)
                odds = {next(odds_iter): int(next(odds_iter)) for _ in range(2)}
            elif param == 'rewards':
                rewards_list = [next(csv_iter) for _ in range(74)][::-1]
                rewards_iter = iter(rewards_list)
                rewards = {next(rewards_iter):
                               {next(rewards_iter):
                                    {int(next(rewards_iter)): float(next(rewards_iter)) for bet in range(4)} for rarity
                                in range(4)}
                           for team in range(2)}

    return Match(match_id, match_url, num_bettors, num_items, teams, winner, loser, odds, rewards, valid_url)


def write_matches_csv(file_name, matches):
    progress_bar_width = 100
    with open(file_name, 'a', encoding='utf-8', newline='') as target_csv:
        target_writer = csv.writer(target_csv, delimiter=',')
        for i, match in enumerate(matches):
            sys.stdout.flush()
            progress = int(i // (len(matches) / progress_bar_width))
            sys.stdout.write('\r[{}{}]{}'.format('#' * progress, ' ' * (progress_bar_width - progress), match))
            try:
                target_writer.writerow(list(flatten(match.__dict__)))
            except InvalidMatchError:
                pass
        sys.stdout.flush()
        sys.stdout.write('\r[{}{}]'.format('#' * progress_bar_width, ' ' * 0))


if __name__ == '__main__':
    pass